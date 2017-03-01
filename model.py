"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#####

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_email = db.Column(db.String(200), autoincrement=False, primary_key=True)
    password = db.Column(db.String(200), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    khan_username = db.Column(db.String(50), nullable=True)
    khan_id = db.Column(db.String(200), nullable=True)
    num_students = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)
    district = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_email=%s name=%s %s>" % (self.user_email,
                                                    self.f_name,
                                                    self.l_name)


class Student(db.Model):
    """Student with a Khan Academy account."""

    __tablename__ = "students"

    student_email = db.Column(db.String(200), autoincrement=False, primary_key=True)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    khan_username = db.Column(db.String(50), nullable=False)
    khan_id = db.Column(db.String(200), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Student student_email=%s name=%s %s>" % (self.student_email,
                                                          self.f_name,
                                                          self.l_name)


class Subject(db.Model):
    """Academic subject."""

    __tablename__ = "subjects"

    subject_code = db.Column(db.String(4), autoincrement=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Subject subject_code=%s name=%s>" % (self.subject_code,
                                                      self.name)


class Classroom(db.Model):
    """Classroom."""

    __tablename__ = "classrooms"

    class_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    user_email = db.Column(db.String(200), db.ForeignKey('users.user_email'))
    subject_code = db.Column(db.String(4), db.ForeignKey('subjects.subject_code'))
    start_date = db.Column(db.DateTime, nullable=False)
    period = db.Column(db.Integer, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    school = db.Column(db.String(50), nullable=True)

    user = db.relationship('User',
                           backref=db.backref("classrooms",
                                              order_by=class_id))
    subject = db.relationship('Subject',
                              backref=db.backref("classrooms",
                                                 order_by=class_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Classroom class_id=%s user_email=%s>" % (self.class_id,
                                                          self.user_email)


class Exam(db.Model):
    """Test or quiz."""

    __tablename__ = "exams"

    exam_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classrooms.class_id'))
    total_points = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    classroom = db.relationship('Classroom',
                                backref=db.backref("exams",
                                                   order_by=exam_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Exam exam_id=%s name=%s>" % (self.exam_id,
                                              self.name)


class ExamResult(db.Model):
    """Result of exam."""

    __tablename__ = "examresults"

    examresult_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exams.exam_id'))
    student_email = db.Column(db.String(200), db.ForeignKey('students.student_email'))
    score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<ExamResult examresult_id=%s exam_id=%s student_email=%s>" % (self.examresult_id,
                                                                              self.exam_id,
                                                                              self.student_email)


class Exercise(db.Model):
    """Exercise on Khan Academy."""

    __tablename__ = "exercises"

    exercise_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(300), nullable=False)
    url = db.Column(db.String(200), nullable=False)
    is_quiz = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Exercise exercise_id=%s name=%s>" % (self.exercise_id,
                                                      self.name)


class ExerciseResult(db.Model):
    """Result of exercise."""

    __tablename__ = "exerciseresults"

    exerciseresult_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.exercise_id'))
    student_email = db.Column(db.String(200), db.ForeignKey('students.student_email'))
    timestamp = db.Column(db.DateTime, nullable=False)
    num_correct = db.Column(db.Integer, nullable=True)
    num_done = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<ExerciseResult exerciseresult_id=%s exercise_id=%s student_email=%s>" % (self.exerciseresult_id,
                                                                                          self.exercise_id,
                                                                                          self.student_email)


class Video(db.Model):
    """Video on Khan Academy."""

    __tablename__ = "videos"

    video_id = db.Column(db.String(50), autoincrement=False, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    url = db.Column(db.String(200), nullable=False)
    youtube_url = db.Column(db.String(200), nullable=False)
    concept = db.Column(db.String(100), nullable=True)
    length = db.Column(db.Integer, nullable=False)
    order_num = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Video video_id=%s name=%s>" % (self.video_id,
                                                self.name)


class VideoResult(db.Model):
    """Result of video."""

    __tablename__ = "videoresults"

    videoresult_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    video_id = db.Column(db.String(50), db.ForeignKey('videos.video_id'))
    student_email = db.Column(db.String(200), db.ForeignKey('students.student_email'))
    timestamp = db.Column(db.DateTime, nullable=False)
    points = db.Column(db.Integer, nullable=True)
    secs_watched = db.Column(db.Integer, nullable=True)
    last_sec_watched = db.Column(db.Integer, nullable=True)

    video = db.relationship('Video',
                            backref=db.backref("videoresults",
                                               order_by=videoresult_id))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<VideoResult videoresult_id=%s video_id=%s student_email=%s>" % (self.videoresult_id,
                                                                                 self.video_id,
                                                                                 self.student_email)


#####

def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///project'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."
