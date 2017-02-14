"""Utility file to seed project database."""

from sqlalchemy import func

from server import app

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)

from model import connect_to_db, db

import json

from datetime import datetime

from sqlalchemy.inspection import inspect


def load_users():
    """Load users from Khan Academy JSON into database."""

    print 'Users'

    User.query.delete()

    user_string = open('seed_data/sample_users.json').read()
    user_dict = json.loads(user_string)

    for user in user_dict:
        user_id = user['user_id']
        email = user['email']
        password = user['username'][:3] + '123'
        nickname = user['nickname'].split(' ')
        f_name, l_name = nickname
        khan_username = user['username']
        num_students = user['students_count']

        user = User(user_id=user_id,
                    email=email,
                    password=password,
                    f_name=f_name,
                    l_name=l_name,
                    khan_username=khan_username,
                    num_students=num_students)

        db.session.add(user)

    db.session.commit()


def load_subjects():
    """Load subjects into database."""

    print 'Subjects'

    Subject.query.delete()

    for row in open('seed_data/u.subjects'):
        row = row.rstrip()
        subject_code, name = row.split('|')

        subject = Subject(subject_code=subject_code,
                          name=name)

        db.session.add(subject)

    db.session.commit()


def load_classrooms():
    """Load classrooms into database."""

    print 'Classrooms'

    Classroom.query.delete()

    for row in open('seed_data/u.classrooms'):
        row = row.rstrip()
        class_id, name, user_id, subject_code, period, year, school = row.split('|')

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
    """Load students from Khan Academy JSON into database."""

    print 'Students'

    Student.query.delete()

    student_string = open('seed_data/sample_students.json').read()
    student_dict = json.loads(student_string)

    for student in student_dict:
        student_email = student['email']
        nickname = student['nickname'].split(' ')
        f_name, l_name = nickname
        khan_username = student['username']

        student = Student(student_email=student_email,
                          f_name=f_name,
                          l_name=l_name,
                          khan_username=khan_username)

        db.session.add(student)

    db.session.commit()


def load_exams():
    """Load exams into database."""

    print 'Exams'

    Exam.query.delete()

    for row in open('seed_data/u.exams'):
        row = row.rstrip()
        exam_id, name, class_id, total_points = row.split('|')

        exam = Exam(exam_id=exam_id,
                    name=name,
                    class_id=class_id,
                    total_points=total_points)

        db.session.add(exam)

    db.session.commit()


def load_examresults():
    """Load exam results into database."""

    print 'ExamResults'

    ExamResult.query.delete()

    for row in open('seed_data/u.examresults'):
        row = row.rstrip()
        examresult_id, exam_id, student_id, score = row.split('|')

        examresult = ExamResult(examresult_id=examresult_id,
                                exam_id=exam_id,
                                student_id=student_id,
                                score=score)

        db.session.add(examresult)

    db.session.commit()


def load_exercises():
    """Load exercises from Khan Academy JSON into database."""

    print 'Exercises'

    Exercise.query.delete()

    exercise_string = open('seed_data/sample_exercises.json').read()
    exercise_dict = json.loads(exercise_string)

    for exercise in exercise_dict:
        exercise_id = exercise['id']
        name = exercise['title']
        description = exercise['description']
        url = exercise['ka_url']
        is_quiz = exercise['is_quiz']

    # for row in open('seed_data/u.exercises'):
    #     row = row.rstrip()
    #     exercise_id, name, url = row.split('|')

        exercise = Exercise(exercise_id=exercise_id,
                            name=name,
                            description=description,
                            url=url,
                            is_quiz=is_quiz)

        db.session.add(exercise)

    db.session.commit()


def load_exerciseresults():
    """Load exercise results into database."""

    print 'ExerciseResults'

    ExerciseResult.query.delete()

    for row in open('seed_data/u.exerciseresults'):
        row = row.rstrip()
        exerciseresult_id, exercise_id, student_email, timestamp, num_correct, num_done = row.split('|')

        if type(timestamp) != datetime:
            timestamp = datetime.strptime(timestamp, '%d-%m-%Y')

        exerciseresult = ExerciseResult(exerciseresult_id=exerciseresult_id,
                                        exercise_id=exercise_id,
                                        student_email=student_email,
                                        timestamp=timestamp,
                                        num_correct=num_correct,
                                        num_done=num_done)

        db.session.add(exerciseresult)

    db.session.commit()


def load_videos():
    """Load videos from Khan Academy JSON into database."""

    print 'Videos'

    Video.query.delete()

    video_string = open('seed_data/sample_videos.json').read()
    video_dict = json.loads(video_string)

    for video in video_dict:
        video_id = video['id']
        name = video['title']
        description = video['description']
        url = video['ka_url']
        youtube_url = 'https://www.youtube.com/watch?v=' + video['youtube_id']
        length = video['duration']

    # for row in open('seed_data/u.videos'):
    #     row = row.rstrip()
    #     video_id, name, url, length = row.split('|')

        video = Video(video_id=video_id,
                      name=name,
                      description=description,
                      url=url,
                      youtube_url=youtube_url,
                      length=length)

        db.session.add(video)

    db.session.commit()


def load_videoresults():
    """Load video results into database."""

    print 'VideoResults'

    VideoResult.query.delete()

    videoresult_string = open('seed_data/sample_videoresults.json').read()
    videoresult_dict = json.loads(videoresult_string)

    for videoresult in videoresult_dict:
        student_email = videoresult['user']
        timestamp = videoresult['last_watched']
        points = videoresult['points']
        secs_watched = videoresult['seconds_watched']
        last_sec_watched = videoresult['last_second_watched']

        video = videoresult['video']
        # name = video['title']
        # description = video['description']
        url = video['ka_url']
        # youtube_url = 'https://www.youtube.com/watch?v=' + video['youtube_id']
        # length = video['duration']
        video_id = db.session.query(Video.video_id).filter(Video.url == url).first()

    # for row in open('seed_data/u.videoresults'):
    #     row = row.rstrip()
    #     videoresult_id, video_id, student_id, timestamp, secs_watched, last_sec_watched = row.split('|')

        if type(timestamp) != datetime:
            timestamp = datetime.strptime(timestamp, '%d-%m-%Y')

        videoresult = VideoResult(video_id=video_id,
                                  student_email=student_email,
                                  timestamp=timestamp,
                                  points=points,
                                  secs_watched=secs_watched,
                                  last_sec_watched=last_sec_watched)

        db.session.add(videoresult)

    db.session.commit()


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
