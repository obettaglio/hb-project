"""Teacher app."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session, url_for)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult, connect_to_db, db)


app = Flask(__name__)

app.secret_key = 'alkjsghfwalejfhbsaldfhuewhif'

app.jinja_env.undefined = StrictUndefined


#####

@app.route('/')
def index():
    """Display homepage.

    If no user is in the session, redirect to login page."""

    # If a user is logged in, show homepage
    if session['logged_in_user']:
        return render_template('homepage.html')
    # If no user is logged in, redirect to login page
    else:
        return redirect('/login')


@app.route('/login')
def show_login_page():
    """Display login page."""

    return render_template('login.html')


@app.route('/login-success')
def log_user_in():
    """Handle login form.

    Put user_id into session and redirect to homepage."""  # CHANGE REDIRECT #

    email = request.form.get('email')
    password = request.form.get('password')

    user = db.session.query(User).filter(User.email == email).first()

    if user:
        if password == user.password:
            # Add user id to Flask session
            session['logged_in_user'] = user.user_id
            flash('Logged in.')
            # CHANGE REDIRECT #
            return redirect('/')
        else:
            flash('Invalid password.')
            return redirect('/login')
    else:
        flash('This email does not have an account.')
        return redirect('/login')


@app.route('/register')
def show_register_page():
    """Display registration page."""

    return render_template('register.html')


@app.route('/register-success')
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
        return redirect('/')


@app.route('/authorize')
def show_authorize_form():
    """Display Khan Academy authorization page."""

    return render_template('authorize.html')


@app.route('/logout')
def logout():
    """Remove user_id from session and redirect to homepage."""

    del session['logged_in_user']

    flash('Logged out')
    return redirect('/')


#####

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
