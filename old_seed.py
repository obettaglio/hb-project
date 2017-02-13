"""Utility file to seed project database."""

from sqlalchemy import func

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)

from model import connect_to_db, db

from server import app

from datetime import datetime

from sqlalchemy.inspection import inspect


def load_users():
    """Load users into database."""

    print "Users"

    User.query.delete()

    for row in open("seed_data/u.users"):
        row = row.rstrip()
        user_id, email, password, f_name, l_name = row.split("|")

        user = User(user_id=user_id,
                    email=email,
                    password=password,
                    f_name=f_name,
                    l_name=l_name)

        db.session.add(user)

    # CSV FILE READING #
    # import psycopg2
    # conn = psycopg2.connect("dbname=project")
    # cur = conn.cursor()
    # f = open('seed_data/users.csv')
    # header = f.readline()
    # line = f.readline()
    # while line:
    #     cur.execute("INSERT INTO users(email, password, f_name, l_name) VALUES(\'%s\', \'%s\', \'%s\', \'%s\');" % (tuple(line.split(",")[1:5])))
    #     line = f.readline()
    # f.close()
    # cur.close()
    # conn.commit()
    # conn.close()

    db.session.commit()


def load_subjects():
    """Load subjects into database."""

    print "Subjects"

    Subject.query.delete()

    for row in open("seed_data/u.subjects"):
        row = row.rstrip()
        subject_code, name = row.split("|")

        subject = Subject(subject_code=subject_code,
                          name=name)

        db.session.add(subject)

    db.session.commit()


def load_classrooms():
    """Load classrooms into database."""

    print "Classrooms"

    Classroom.query.delete()

    for row in open("seed_data/u.classrooms"):
        row = row.rstrip()
        class_id, name, user_id, subject_code, period, year, school = row.split("|")

        classroom = Classroom(class_id=class_id,
                              name=name,
                              user_id=user_id,
                              subject_code=subject_code,
                              period=period,
                              year=year,
                              school=school)

        db.session.add(classroom)

    db.session.commit()


def load_students():
    """Load students into database."""

    print "Students"

    Student.query.delete()

    for row in open("seed_data/u.students"):
        row = row.rstrip()
        student_id, email, f_name, l_name, class_id = row.split("|")

        student = Student(student_id=student_id,
                          email=email,
                          f_name=f_name,
                          l_name=l_name,
                          class_id=class_id)

        db.session.add(student)

    db.session.commit()


def load_exams():
    """Load exams into database."""

    print "Exams"

    Exam.query.delete()

    for row in open("seed_data/u.exams"):
        row = row.rstrip()
        exam_id, name, class_id, total_points = row.split("|")

        exam = Exam(exam_id=exam_id,
                    name=name,
                    class_id=class_id,
                    total_points=total_points)

        db.session.add(exam)

    db.session.commit()


def load_examresults():
    """Load exam results into database."""

    print "ExamResults"

    ExamResult.query.delete()

    for row in open("seed_data/u.examresults"):
        row = row.rstrip()
        examresult_id, exam_id, student_id, score = row.split("|")

        examresult = ExamResult(examresult_id=examresult_id,
                                exam_id=exam_id,
                                student_id=student_id,
                                score=score)

        db.session.add(examresult)

    db.session.commit()


def load_exercises():
    """Load exercises into database."""

    print "Exercises"

    Exercise.query.delete()

    for row in open("seed_data/u.exercises"):
        row = row.rstrip()
        exercise_id, name, url = row.split("|")

        exercise = Exercise(exercise_id=exercise_id,
                            name=name,
                            url=url)

        db.session.add(exercise)

    db.session.commit()


def load_exerciseresults():
    """Load exercise results into database."""

    print "ExerciseResults"

    ExerciseResult.query.delete()

    for row in open("seed_data/u.exerciseresults"):
        row = row.rstrip()
        exerciseresult_id, exercise_id, student_id, timestamp, num_correct, num_done = row.split("|")

        if type(timestamp) != datetime:
            timestamp = datetime.strptime(timestamp, '%d-%m-%Y')

        exerciseresult = ExerciseResult(exerciseresult_id=exerciseresult_id,
                                        exercise_id=exercise_id,
                                        student_id=student_id,
                                        timestamp=timestamp,
                                        num_correct=num_correct,
                                        num_done=num_done)

        db.session.add(exerciseresult)

    db.session.commit()


def load_videos():
    """Load videos into database."""

    print "Videos"

    Video.query.delete()

    for row in open("seed_data/u.videos"):
        row = row.rstrip()
        video_id, name, url, length = row.split("|")

        video = Video(video_id=video_id,
                      name=name,
                      url=url,
                      length=length)

        db.session.add(video)

    db.session.commit()


def load_videoresults():
    """Load video results into database."""

    print "VideoResults"

    VideoResult.query.delete()

    for row in open("seed_data/u.videoresults"):
        row = row.rstrip()
        videoresult_id, video_id, student_id, timestamp, secs_watched, last_sec_watched = row.split("|")

        if type(timestamp) != datetime:
            timestamp = datetime.strptime(timestamp, '%d-%m-%Y')

        videoresult = VideoResult(videoresult_id=videoresult_id,
                                  video_id=video_id,
                                  student_id=student_id,
                                  timestamp=timestamp,
                                  secs_watched=secs_watched,
                                  last_sec_watched=last_sec_watched)

        db.session.add(videoresult)

    db.session.commit()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     print "Setting max user ID value!"

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


# def set_val_primary_key(class_name, pkey_name, table_name):
#     """Set value for the next user_id after seeding database"""

#     print "Setting max user ID value!"

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


def update_pkey_seqs():
    """Set primary key for each table to start at one higher than the current
    highest key. Helps when data has been manually seeded."""

    # get a dictionary of {classname: class} for all classes in model.py
    model_classes = db.Model._decl_class_registry

    # loop over the classes
    for class_name in model_classes:

        # the dictionary will include a helper class we don't care about, so
        # skip it
        if class_name == "_sa_module_registry":
            continue

        print
        print "working on class", class_name

        # get the class itself out of the dictionary
        cls = model_classes[class_name]

        # get the name of the table associated with the class and its primary
        # key
        table_name = cls.__tablename__
        primary_key = inspect(cls).primary_key[0].name
        print "table name:", table_name
        print "primary key:", primary_key

        # check to see if the primary key is autoincrementing
        # if it isn't, skip to the next class
        print inspect(cls).primary_key[0].__dict__["autoincrement"]
        if inspect(cls).primary_key[0].__dict__["autoincrement"] is not True:
            print "not an autoincrementing key - skipping"
            continue

        # now we know we're dealing with an autoincrementing key, so get the
        # highest id value currently in the table
        result = db.session.query(func.max(getattr(cls, primary_key))).first()
        if result[0]:
            max_id = int(result[0])
            print "highest id:", max_id

            # set the next value to be max + 1
            query = ("SELECT setval('" + table_name + "_" + primary_key +
                     "_seq', :new_id)")
            db.session.execute(query, {'new_id': max_id + 1})
            db.session.commit()

    # we're done!


def call_all_functions():
    """Call all seeding functions."""

    load_users()
    load_subjects()
    load_classrooms()
    load_students()
    load_exams()
    load_examresults()
    load_exercises()
    load_exerciseresults()
    load_videos()
    load_videoresults()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    call_all_functions()
    update_pkey_seqs()
    # set_val_user_id()
