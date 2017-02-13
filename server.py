"""Teacher app."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)

from model import connect_to_db, db

import ka_oauth


app = Flask(__name__)

app.secret_key = 'alkjsghfwalejfhbsaldfhuewhif'

app.jinja_env.undefined = StrictUndefined


##### LOGIN, REGISTER, AUTHORIZE, LOGOUT #####

@app.route('/')
def index():
    """Display homepage.

    Homepage contains links to Register and Login pages."""

    return render_template('homepage.html')


@app.route('/login')
def show_login_page():
    """Display login form."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def log_user_in():
    """Handle login form.

    Put user_id into session and redirect to homepage."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter(User.email == email).first()

    if user:
        if password == user.password:
            session['logged_in_user'] = user.user_id
            ka_oauth.run_tests(session)
            flash('Logged in.')
            return redirect('/classes')
        else:
            flash('Invalid password.')
            return redirect('/login')
    else:
        flash('This email does not have an account.')
        return redirect('/login')


@app.route('/register')
def show_register_page():
    """Display registration form."""

    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register_user():
    """Handle registration form.

    Add user to database and put user_id into session."""

    ka_oauth.run_tests(session)

    response = session['khan_user'].get('/api/v1/user')
    response = response.json()

    user_id = response['user_id']
    email = response['email']
    password = response['username'][:3] + '123'
    nickname = response['nickname'].split(' ')
    f_name, l_name = nickname
    khan_username = response['username']
    num_students = response['students_count']

    user = User(user_id=user_id,
                email=email,
                password=password,
                f_name=f_name,
                l_name=l_name,
                khan_username=khan_username,
                num_students=num_students)

    db.session.add(user)
    db.session.commit()

    session['logged_in_user'] = user.user_id

    flash('Account created.')
    return redirect('/classes')

    # email = request.form.get('email')
    # password = request.form.get('password')
    # f_name = request.form.get('f_name')
    # l_name = request.form.get('l_name')
    # zipcode = request.form.get('zipcode')
    # district = request.form.get('district')

    # user = db.session.query(User).filter(User.email == email).first()

    # if user:
    #     flash('This email is already registered. Please log in.')
    #     return redirect('/login')
    # else:
    #     new_user = User(email=email, password=password,
    #                     f_name=f_name, l_name=l_name,
    #                     zipcode=zipcode, district=district)
    #     db.session.add(new_user)
    #     db.session.commit()

    #     session['logged_in_user'] = new_user.user_id

    #     flash('Account created.')
    #     return redirect('/classes')


@app.route('/authorize')
def show_authorize_form():
    """Display Khan Academy authorization page."""

    return render_template('authorize.html')


@app.route('/logout')
def log_user_out():
    """Remove user_id from session and redirect to homepage."""

    del session['logged_in_user']

    flash('Logged out')
    return redirect('/')


##### CLASSROOMS, EXAMS #####

@app.route('/classes')
def show_classes_list():
    """Display list of classes taught by user."""

    # email = request.form.get('email')
    if session.get('logged_in_user') and session.get('khan_user'):
        user_id = session['logged_in_user']
        khan_id = session['khan_user']

        user = db.session.query(User).filter(User.user_id == user_id).first()
        print user

        response = khan_id.get('/api/v1/classes', params=params)
        response = response.json()

        classrooms = db.session.query(Classroom).join(User)\
                                                .filter(User.user_id == user_id).all()
        print classrooms

        return render_template('class-list.html',
                               user=user,
                               classrooms=classrooms)
    else:
        return render_template('unauthorized-attempt.html')


@app.route('/classes/add-class')
def show_new_class_form():
    """Display form to add new class."""

    subjects_tup = db.session.query(Subject.name).all()
    subjects = []

    for subject in subjects_tup:
        subject = subject[0]
        subjects.append(subject)

    return render_template('add-class.html',
                           subjects=subjects)


@app.route('/classes/add-class', methods=['POST'])
def add_new_class():
    """Handle form to add new class and redirect to classes page."""

    user_id = session['logged_in_user']

    name = request.form.get('class-name')
    subject = request.form.get('subject')

    subject_code = db.session.query(Subject.subject_code).filter(Subject.name == subject).first()

    new_class = Classroom(name=name,
                          user_id=user_id,
                          subject_code=subject_code)

    db.session.add(new_class)
    db.session.commit()

    return redirect('/classes')


@app.route('/classes/<class_id>')   # note: returns string of a number
def show_class(class_id):
    """Display individual class data.

    Includes list of existing exams, visual analytic, and New Exam button."""

    classroom = db.session.query(Classroom).filter(Classroom.class_id == class_id).first()
    exams = db.session.query(Exam).filter(Exam.class_id == class_id).all()

    return render_template('class-individual.html',
                           classroom=classroom,
                           exams=exams)


@app.route('/classes/<class_id>/add-exam')
def show_new_exam_form(class_id):
    """Display form to add new exam under specified class."""

    return render_template('add-exam.html',
                           class_id=class_id)


@app.route('/classes/<class_id>/add-exam', methods=['POST'])
def add_new_exam(class_id):
    """Handle form to add new exam under specified class."""

    name = request.form.get('exam-name')
    total_points = request.form.get('total-points')

    exam = Exam(name=name,
                class_id=class_id,
                total_points=total_points)
    db.session.add(exam)
    db.session.commit()

    return redirect(url_for('show_class', class_id=class_id))


@app.route('/classes/<class_id>/<exam_id>')
def show_exam(class_id, exam_id):
    """Display individual exam data.

    Includes list of exam scores, visual analytic, and Add Score button."""

    exam = db.session.query(Exam).filter(Exam.exam_id == exam_id).first()
    examresults = db.session.query(ExamResult).filter(ExamResult.exam_id == exam_id).all()

    return render_template('exam-individual.html',
                           class_id=class_id,
                           exam=exam,
                           examresults=examresults)


@app.route('/classes/<class_id>/<exam_id>/add-score')
def show_new_score_form(class_id, exam_id):
    """Display form to add new exam score under specified class."""

    students = db.session.query(Student).filter(Student.class_id == class_id).all()
    exam = db.session.query(Exam).filter(Exam.exam_id == exam_id).first()

    return render_template('add-score.html',
                           class_id=class_id,
                           students=students,
                           exam=exam)


@app.route('/classes/<class_id>/<exam_id>/add-score', methods=['POST'])
def add_new_score(class_id, exam_id):
    """Handle form to add new exam score under specified class."""

    student_name = request.form.get('student-name')
    score = request.form.get('score')

    student_name = student_name.split(" ")
    f_name, l_name = student_name
    student = db.session.query(Student).filter((Student.f_name == f_name) &
                                               (Student.l_name == l_name)).first()
    student_id = student.student_id

    examresult = ExamResult(exam_id=exam_id,
                            student_id=student_id,
                            score=score)
    db.session.add(examresult)
    db.session.commit()

    return redirect(url_for('show_exam', class_id=class_id, exam_id=exam_id))


#####

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
