"""Teacher app."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash,
                   session)

from flask_debugtoolbar import DebugToolbarExtension

from model import (User, Student, Subject, Class, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult, connect_to_db, db)


app = Flask(__name__)

app.secret_key = "alkjsghfwalejfhb"

app.jinja_env.undefined = StrictUndefined


#####

@app.route('/')
def index():
    """Login page."""

    return render_template('login.html')


#####

if __name__ == "__main__":
    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
