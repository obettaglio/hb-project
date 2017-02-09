"""Teacher app."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)

from model import connect_to_db, db


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


@app.route('/login-validation', methods=['POST'])
def log_user_in():
    """Handle login form.

    Put user_id into session and redirect to homepage."""

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter(User.email == email).first()

    if user:
        if password == user.password:
            session['logged_in_user'] = user.user_id
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


@app.route('/register-success', methods=['POST'])
def register_user():
    """Handle registration form.

    Add user to database and put user_id into session."""

    email = request.form.get('email')
    password = request.form.get('password')
    f_name = request.form.get('f_name')
    l_name = request.form.get('l_name')
    zipcode = request.form.get('zipcode')
    district = request.form.get('district')

    user = db.session.query(User).filter(User.email == email).first()

    if user:
        flash('This email is already registered. Please log in.')
        return redirect('/login')
    else:
        new_user = User(email=email, password=password,
                        f_name=f_name, l_name=l_name,
                        zipcode=zipcode, district=district)
        db.session.add(new_user)
        db.session.commit()

        session['logged_in_user'] = new_user.user_id

        flash('Account created.')
        return redirect('/classes')


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
    if session.get('logged_in_user'):
        user_id = session['logged_in_user']

        user = db.session.query(User).filter(User.user_id == user_id).first()
        print user

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
    """Display form to add a new class."""

    subjects_tup = db.session.query(Subject.name).all()
    subjects = []

    for subject in subjects_tup:
        subject = subject[0]
        subjects.append(subject)

    return render_template('add-class.html',
                           subjects=subjects)


@app.route('/classes/add-class-validation', methods=['POST'])
def add_new_class():
    """Handle form to add a new class and redirect to classes page."""

    user_id = session['logged_in_user']

    name = request.form.get('name')
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

    pass


#####

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
