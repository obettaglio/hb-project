"""Teacher app."""

from jinja2 import StrictUndefined
from flask import Flask, jsonify, render_template, redirect, request, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)
from model import connect_to_db, db
from passlib.hash import argon2
import rauth
import os
import random
import string
from datetime import datetime


app = Flask(__name__)

app.secret_key = 'alkjsghfwalejfhbsaldfhuewhif'

app.jinja_env.undefined = StrictUndefined

CONSUMER_KEY = os.environ['KHAN_CONSUMER_KEY']
CONSUMER_SECRET = os.environ['KHAN_CONSUMER_SECRET']

CALLBACK_BASE = '0.0.0.0'
SERVER_URL = 'http://www.khanacademy.org'

DEFAULT_API_RESOURCE = '/api/v1/user'
VERIFIER = None


##### LOGIN, REGISTER, AUTHORIZE, LOGOUT #####

@app.route('/')
def index():
    """Display homepage.

    Homepage contains links to Register and Login pages."""

    if not session.get('logged_in_user'):
        return render_template('homepage.html')

    else:
        user_email = session['logged_in_user']
        user = db.session.query(User).filter(User.user_email == user_email).first()
        user_f_name = user.f_name

        classrooms = db.session.query(Classroom).filter(Classroom.user_email == user_email).all()

        subject_dict = {}
        subjects = db.session.query(Subject.subject_code, Subject.name).all()
        for subject in subjects:
            subject_dict[subject[0]] = subject[1]
        print subject_dict

        return render_template('homepage-user.html',
                               user_f_name=user_f_name,
                               classrooms=classrooms,
                               subject_dict=subject_dict)

        # else:
        #     return render_template('homepage-user-empty.html',
        #                            user_f_name=user_f_name)


@app.route('/login')
def show_login_page():
    """Display login form."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def log_user_in():
    """Handle login form.

    Put user_email into session and redirect to homepage."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter(User.user_email == email).first()

    if user:
        if argon2.verify(password, user.password):
            session['logged_in_user'] = user.user_email
            if 'oauth_params' in session:
                oauth_params = session['oauth_params']
                if 'access_token' in oauth_params:
                    flash('Logged in.')
                    return redirect('/')
                else:
                    # no tokens, redo oauth
                    pass
            else:
                return redirect('/')
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

    Redirect user to Khan Academy's authorization page, and set callback URL."""

    # create an OAuth1Service using rauth
    app.service = rauth.OAuth1Service(name='test',
                                      consumer_key=CONSUMER_KEY,
                                      consumer_secret=CONSUMER_SECRET,
                                      request_token_url=SERVER_URL + '/api/auth2/request_token',
                                      access_token_url=SERVER_URL + '/api/auth2/access_token',
                                      authorize_url=SERVER_URL + '/api/auth2/authorize',
                                      base_url=SERVER_URL + '/api/auth2')

    # 1. get request token
    app.request_token, app.secret_request_token = app.service.get_request_token(
        params={'oauth_callback': 'http://localhost:5000/khan-authorize'})

    # 2. authorize request token
    authorize_url = app.service.get_authorize_url(app.request_token)

    return redirect(authorize_url)


@app.route('/khan-authorize')
def authorize_khan_user():
    """Handle Khan Academy authorization form.

    Put access tokens in session, add user to database, and display success message."""

    #  read verifier param value from url
    verifier = request.args.get('oauth_verifier')

    # 3. get access token
    oauth_session = app.service.get_auth_session(app.request_token, app.secret_request_token,
                                                 params={'oauth_verifier': verifier})

    session['oauth_params'] = {'access_token': oauth_session.access_token,
                               'access_token_secret': oauth_session.access_token_secret}

    # 4. make authenticated API call
    # import pdb
    # pdb.set_trace()
    params = {}
    response = oauth_session.get("http://www.khanacademy.org/api/v1/user", params=params)
    user_dict = response.json()

    def generate_password():
        """Generate 8-character alphanumeric password."""

        chars = string.letters + string.digits
        length = 8
        password = ''.join(random.choice(chars) for _ in range(length))
        return password

    user_email = user_dict['email']
    password = generate_password()
    pwd_hash = argon2.hash(password)
    nickname = user_dict['nickname'].split(' ')
    f_name, l_name = nickname
    khan_username = user_dict['username']
    num_students = user_dict['students_count']

    user = User(user_email=user_email,
                password=pwd_hash,
                f_name=f_name,
                l_name=l_name,
                khan_username=khan_username,
                num_students=num_students)

    db.session.add(user)
    db.session.commit()

    flash('Account created successfully! Please log in.\nTemporary password: ' + password)
    return redirect('/login')


@app.route('/logout')
def log_user_out():
    """Remove user_email from session and redirect to homepage."""

    del session['logged_in_user']

    flash('Logged out')
    return redirect('/')


##### CLASSROOMS, EXAMS #####

@app.route('/classroom')
def show_single_class():
    """Display class taught by user.

    Include list of existing exams, link to student roster, visual data, and Add Exam button."""

    user_email = session['logged_in_user']
    user = db.session.query(User).filter(User.user_email == user_email).first()
    user_f_name = user.f_name

    class_id = request.args.get('class_id')
    classroom = db.session.query(Classroom).filter(Classroom.class_id == class_id).first()

    # ensure user can access requested classroom
    if classroom.user_email == user_email:
        exams = db.session.query(Exam).filter(Exam.class_id == class_id).all()

        return render_template('classroom.html',
                               user_f_name=user_f_name,
                               classroom=classroom,
                               exams=exams)

    else:
        return render_template('unauthorized-attempt.html')


@app.route('/create-class')
def show_create_class_form():
    """Display form to create a class."""

    user_email = session['logged_in_user']
    user = db.session.query(User).filter(User.user_email == user_email).first()
    user_f_name = user.f_name

    subjects_tup = db.session.query(Subject.name).all()
    subjects = []

    for subject in subjects_tup:
        subject = subject[0]
        subjects.append(subject)

    return render_template('create-class.html',
                           user_f_name=user_f_name,
                           subjects=subjects)


@app.route('/create-class', methods=['POST'])
def create_class():
    """Handle form to create a class and redirect to user homepage."""

    user_email = session['logged_in_user']

    name = request.form.get('class_name')
    subject = request.form.get('subject')
    start_date = request.form.get('start_date')

    if type(start_date) != datetime:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    subject_code = db.session.query(Subject.subject_code).filter(Subject.name == subject).first()[0]

    new_class = Classroom(name=name,
                          user_email=user_email,
                          subject_code=subject_code,
                          start_date=start_date)

    db.session.add(new_class)
    db.session.commit()

    ## HOW TO PASS NEW_CLASS_ID INTO CREATE-CLASS TO BE USED IN STUDENT-ROSTER? ##
    # user_class_ids = db.session.query(Classroom.class_id).filter(Classroom.user_email == user_email)\
    #                                                      .order_by(Classroom.class_id).all()
    # new_class_id = user_class_ids[-1][0]

    return 'Created class.'


@app.route('/classroom/student-roster')
def show_student_roster():
    """Display student roster for class taught by user."""

    user_email = session['logged_in_user']
    user = db.session.query(User).filter(User.user_email == user_email).first()
    user_f_name = user.f_name

    class_id = request.args.get('class_id')
    classroom = db.session.query(Classroom).filter(Classroom.class_id == class_id).first()

    if classroom.user_email == user_email:

        students = db.session.query(Student).filter(Student.class_id == class_id).order_by(Student.l_name).all()

        return render_template('student-roster.html',
                               user_f_name=user_f_name,
                               classroom=classroom,
                               students=students)

    else:
        return render_template('unauthorized-attempt.html')


@app.route('/classroom/add-student', methods=['POST'])
def add_student_to_roster():
    """Handle form to add student to class roster."""

    # user_email = session['logged_in_user']
    class_id = request.form.get('class_id')

    f_name = request.form.get('f_name')
    l_name = request.form.get('l_name')
    student_email = request.form.get('student_email')
    khan_username = request.form.get('khan_username')

    student_email_tup = (student_email,)
    student_emails_list = db.session.query(Student.student_email).all()

    if student_email_tup not in student_emails_list:
        new_student = Student(student_email=student_email,
                              f_name=f_name,
                              l_name=l_name,
                              khan_username=khan_username,
                              class_id=class_id)

        db.session.add(new_student)
        db.session.commit()

        full_name = f_name + " " + l_name
        new_student_dict = {'full_name': full_name,
                            'student_email': student_email,
                            'khan_username': khan_username}

    else:
        # update student's class_id using SQLAlchemy
        db.session.execute(update(Student, values={Student.class_id: class_id}))
        db.session.commit()

    return jsonify(new_student_dict)


@app.route('/classroom/exam')
def show_exam():
    """Display individual exam data.

    Includes list of exam scores, visual analytic, and Add Score button."""

    user_email = session['logged_in_user']
    user = db.session.query(User).filter(User.user_email == user_email).first()
    user_f_name = user.f_name

    class_id = request.args.get('class_id')
    classroom = Classroom.query.filter(Classroom.class_id == class_id).first()

    if classroom.user_email == user_email:

        students = db.session.query(Student).filter(Student.class_id == class_id).order_by(Student.l_name).all()

        exam_id = request.args.get('exam_id')
        exam = db.session.query(Exam).filter(Exam.exam_id == exam_id).first()
        examresults = db.session.query(ExamResult).filter(ExamResult.exam_id == exam_id).all()

        new_examresults = {}

        for examresult in examresults:
            student_email = examresult.student_email
            student_name = db.session.query(Student.f_name, Student.l_name).filter(Student.student_email == student_email).first()
            student_name = student_name[0] + " " + student_name[1]
            new_examresults[student_email] = {'student_name': student_name,
                                              'exam_score': examresult.score}

        examresults = new_examresults.values()

        return render_template('exam-individual.html',
                               user_f_name=user_f_name,
                               classroom=classroom,
                               exam=exam,
                               examresults=examresults,
                               students=students)

    else:
        return render_template('unauthorized-attempt.html')


@app.route('/classroom/add-exam', methods=['POST'])
def add_new_exam():
    """Handle form to add new exam under specified class."""

    # user_email = session['logged_in_user']
    class_id = request.form.get('class_id')
    name = request.form.get('exam_name')
    timestamp = request.form.get('timestamp')
    total_points = request.form.get('total_points')

    if type(timestamp) != datetime:
        timestamp = datetime.strptime(timestamp, '%Y-%m-%d')

    new_exam = Exam(name=name,
                    class_id=class_id,
                    total_points=total_points,
                    timestamp=timestamp)

    db.session.add(new_exam)
    db.session.commit()

    exam_id = new_exam.exam_id

    new_exam_dict = {'exam_id': exam_id,
                     'exam_name': name,
                     'class_id': class_id,
                     'total_points': total_points,
                     'timestamp': timestamp}

    return jsonify(new_exam_dict)


@app.route('/classroom/add-score', methods=['POST'])
def add_new_score():
    """Handle form to add new score for specified exam."""

    # user_email = session['logged_in_user']
    exam_id = request.form.get('exam_id')
    student_email = request.form.get('student_email')
    score = request.form.get('score')

    examresult = ExamResult(exam_id=exam_id,
                            student_email=student_email,
                            score=score)

    db.session.add(examresult)
    db.session.commit()

    student_name = db.session.query(Student.f_name, Student.l_name).filter(Student.student_email == student_email).first()
    student_name = student_name[0] + " " + student_name[1]

    new_examresult_dict = {'student_name': student_name,
                           'score': score}

    return jsonify(new_examresult_dict)


##### JSON, D3 #####

@app.route('/classroom-line-d3')
def show_classroom_line_d3_new():
    """Display d3 line chart."""

    class_id = request.args.get('class_id')

    return render_template('classroom-line-d3.html',
                           class_id=class_id)


@app.route('/classroom-line-data.json')
def jsonify_classroom_line_data():
    """Query database for data filtering by exam_id. Return data for line chart as JSON.

    Data consists of examresult and videoresult details listed by exam:
        avg_score, avg_num_videos."""

    class_id = request.args.get('class_id')
    classroom = db.session.query(Classroom).filter(Classroom.class_id == class_id).first()
    exams = db.session.query(Exam).filter(Exam.class_id == class_id).order_by(Exam.timestamp).all()

    students_query = db.session.query(Student.student_email).filter(Student.class_id == class_id)
    num_students = students_query.count()

    completed_exams = []

    results = []

    for exam in exams:
        exam_id = exam.exam_id
        exam_name = exam.name
        exam_timestamp = exam.timestamp

        if completed_exams == []:
            start_date = classroom.start_date
        else:
            prev_exam = completed_exams[-1]
            start_date = prev_exam.timestamp

        total_points = db.session.query(Exam.total_points).filter(Exam.exam_id == exam_id).first()[0]
        exam_scores = db.session.query(ExamResult.score).filter(ExamResult.exam_id == exam_id).all()

        exam_percentages = []

        for exam_score in exam_scores:
            exam_score = exam_score[0]
            exam_percentage = (float(exam_score) / total_points) * 100
            exam_percentages.append(exam_percentage)

        avg_score = float(sum(exam_percentages) / len(exam_percentages))

        num_videoresults = db.session.query(VideoResult).filter((VideoResult.timestamp > start_date) &
                                                                (VideoResult.timestamp < exam_timestamp)).count()
        avg_num_videoresults = float(num_videoresults / num_students)

        # num_exerciseresults = db.session.query(ExerciseResult).filter(ExerciseResult.timestamp < exam_timestamp).count()
        # avg_num_exerciseresults = num_exerciseresults / num_students

        results.append({'examName': exam_name,
                        'avgScore': avg_score,
                        'avgNumVideos': avg_num_videoresults})

        completed_exams.append(exam)

    return jsonify(results)


@app.route('/exam-bar-d3')
def show_exam_bar_new_d3():
    """Display d3 stacked/grouped bar chart."""

    exam_id = request.args.get('exam_id')

    return render_template('exam-bar-d3.html',
                           exam_id=exam_id)


@app.route('/exam-bar-data.json')
def jsonify_exam_bar_data():
    """Query database for data filtering by exam_id. Return data for new bar chart as JSON.

    Data consists of examresult and videoresult details listed by video_name:
        num_students separated by grade_range."""

    exam_id = request.args.get('exam_id')
    exam_topic = db.session.query(Exam.topic).filter(Exam.exam_id == exam_id).first()[0]
    exam_video_ids = db.session.query(Video.video_id).filter(Video.topic == exam_topic).all()

    total_points = db.session.query(Exam.total_points).filter(Exam.exam_id == exam_id).first()[0]
    examresults = db.session.query(ExamResult.student_email, ExamResult.score).filter(ExamResult.exam_id == exam_id).all()

    def convert_percent_to_grade(exam_percentage):
        if exam_percentage >= 0.9:
            return 'A'
        elif exam_percentage >= 0.8:
            return 'B'
        elif exam_percentage >= 0.7:
            return 'C'
        elif exam_percentage >= 0.6:
            return 'D'
        else:
            return 'F'

    results = {}

    for examresult in examresults:
        student_email, exam_score = examresult

        video_ids = db.session.query(VideoResult.video_id).filter(VideoResult.student_email == student_email)\
                                                          .order_by(VideoResult.timestamp).all()

        for video_id in video_ids:
            if video_id in exam_video_ids:
                video_name = db.session.query(Video.name).filter(Video.video_id == video_id).first()[0]
                order_num = db.session.query(Video.order_num).filter(Video.video_id == video_id).first()[0]

                exam_percentage = float(exam_score) / total_points
                grade_range = convert_percent_to_grade(exam_percentage)

                if order_num not in results:
                    results[order_num] = {'video_name': video_name,
                                          'A': 0,
                                          'B': 0,
                                          'C': 0,
                                          'D': 0,
                                          'F': 0}

                results[order_num][grade_range] += 1

    return jsonify(results)


@app.route('/exam-timestamp-d3')
def show_exam_timestamp_d3():
    """Display d3 timestamp scatterplot chart."""

    exam_id = request.args.get('exam_id')

    return render_template('exam-timestamp-d3.html',
                           exam_id=exam_id)


@app.route('/exam-timestamp-data.json')
def jsonify_exam_timestamp_data():
    """Query database for data filtering by exam_id. Return data for timestamp scatterplot chart as JSON.

    Data consists of examresult and videoresult details listed by video_name:
        video_url, total_views, A_views, B_views, C_views, D_views, and F_views."""

    exam_id = request.args.get('exam_id')

    exam = db.session.query(Exam).filter(Exam.exam_id == exam_id).first()
    total_points = exam.total_points
    exam_date = exam.timestamp
    exam_topic = exam.topic
    exam_video_ids = db.session.query(Video.video_id).filter(Video.topic == exam_topic).all()

    examresults = db.session.query(ExamResult.student_email, ExamResult.score).filter(ExamResult.exam_id == exam_id).all()

    results = []

    def convert_percent_to_grade(exam_percentage):
        if exam_percentage >= 0.9:
            return 'A'
        elif exam_percentage >= 0.8:
            return 'B'
        elif exam_percentage >= 0.7:
            return 'C'
        elif exam_percentage >= 0.6:
            return 'D'
        else:
            return 'F'

    for examresult in examresults:
        student_email, exam_score = examresult

        exam_percentage = float(exam_score) / total_points
        grade_range = convert_percent_to_grade(exam_percentage)

        video_ids = db.session.query(VideoResult.video_id).filter((VideoResult.student_email == student_email) &
                                                                  (VideoResult.timestamp < exam_date)).all()

        for video_id in video_ids:
            if video_id in exam_video_ids:
                video_name = db.session.query(Video.name).filter(Video.video_id == video_id).first()[0]
                video_order = db.session.query(Video.order_num).filter(Video.video_id == video_id).first()[0]
                timestamp = db.session.query(VideoResult.timestamp).filter((VideoResult.student_email == student_email) &
                                                                           (VideoResult.video_id == video_id)).first()[0]

                timestamp = datetime.strftime(timestamp, '%m-%d-%H-%M-%S')

                results.append({'videoName': video_name,
                                'videoOrder': video_order,
                                'timestamp': timestamp,
                                'gradeRange': grade_range})

    results = sorted(results, key=lambda d: (d['videoOrder'], d['gradeRange']))

    return jsonify(results)


#####

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
