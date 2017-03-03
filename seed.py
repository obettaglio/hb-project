"""Utility file to seed project database."""

from sqlalchemy import func

from server import app

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)

from model import connect_to_db, db

from data_generator import (generate_students, generate_videoresults, generate_examresults)

import json

from passlib.hash import argon2

import random

from datetime import datetime, timedelta

from sqlalchemy.inspection import inspect


def load_users():
    """Load users from Khan Academy JSON into database."""

    print 'Users'

    User.query.delete()

    user_string = open('static/data/sample_users.json').read()
    user_dict = json.loads(user_string)

    for user in user_dict:
        # user_id = user['user_id']
        user_email = user['email']
        password = user['username'][:3] + '123'
        # password = generate_password()
        pwd_hash = argon2.hash(password)
        nickname = user['nickname'].split(' ')
        f_name, l_name = nickname
        khan_username = user['username']
        khan_id = user['user_id']
        num_students = user['students_count']

        user = User(user_email=user_email,
                    password=pwd_hash,
                    f_name=f_name,
                    l_name=l_name,
                    khan_username=khan_username,
                    khan_id=khan_id,
                    num_students=num_students)

        db.session.add(user)

    db.session.commit()


def load_subjects():
    """Load subjects into database."""

    print 'Subjects'

    Subject.query.delete()

    for row in open('static/data/u.subjects'):
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

    for row in open('static/data/u.classrooms'):
        row = row.rstrip()
        class_id, name, user_email, subject_code, start_date, period, year, school = row.split('|')

        if type(start_date) != datetime:
            start_date = datetime.strptime(start_date, '%m-%d-%Y')

        classroom = Classroom(class_id=class_id,
                              name=name,
                              user_email=user_email,
                              subject_code=subject_code,
                              start_date=start_date,
                              period=period,
                              year=year,
                              school=school)

        db.session.add(classroom)

    db.session.commit()


def load_students():
    """Load students from Khan Academy JSON into database."""

    print 'Students'

    Student.query.delete()

    student_string = open('static/data/sample_students.json').read()
    student_dict = json.loads(student_string)

    for student in student_dict:
        student_email = student['email']
        nickname = student['nickname'].split(' ')
        f_name, l_name = nickname
        khan_username = student['username']
        khan_id = student['user_id']
        class_id = 1

        student = Student(student_email=student_email,
                          f_name=f_name,
                          l_name=l_name,
                          khan_username=khan_username,
                          khan_id=khan_id,
                          class_id=class_id)

        db.session.add(student)

    db.session.commit()


def load_exams():
    """Load exams into database."""

    print 'Exams'

    Exam.query.delete()

    for row in open('static/data/u.exams'):
        row = row.rstrip()
        exam_id, name, topic, class_id, total_points, timestamp = row.split('|')

        if type(timestamp) != datetime:
            timestamp = datetime.strptime(timestamp, '%m-%d-%Y')

        exam = Exam(exam_id=exam_id,
                    name=name,
                    topic=topic,
                    class_id=class_id,
                    total_points=total_points,
                    timestamp=timestamp)

        db.session.add(exam)

    db.session.commit()


def load_examresults():
    """Load exam results into database."""

    print 'ExamResults'

    ExamResult.query.delete()

    examresult_string = open('static/data/sample_examresults.json').read()
    examresult_dict = json.loads(examresult_string)

    for examresult in examresult_dict:
        examresult_id = examresult['examresult_id']
        exam_id = examresult['exam_id']
        student_email = examresult['student_email']
        score = examresult['score']

        examresult = ExamResult(examresult_id=examresult_id,
                                exam_id=exam_id,
                                student_email=student_email,
                                score=score)

        db.session.add(examresult)

    db.session.commit()

    # for row in open('static/data/u.examresults'):
    #     row = row.rstrip()
    #     examresult_id, exam_id, student_email, score = row.split('|')

    #     examresult = ExamResult(examresult_id=examresult_id,
    #                             exam_id=exam_id,
    #                             student_email=student_email,
    #                             score=score)

    #     db.session.add(examresult)

    # db.session.commit()


def load_exercises():
    """Load exercises from Khan Academy JSON into database."""

    print 'Exercises'

    Exercise.query.delete()

    exercise_string = open('static/data/sample_exercises.json').read()
    exercise_dict = json.loads(exercise_string)

    for exercise in exercise_dict:
        exercise_id = exercise['id']
        name = exercise['title']
        description = exercise['description']
        url = exercise['ka_url']
        is_quiz = exercise['is_quiz']

    # for row in open('static/data/u.exercises'):
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

    # for row in open('static/data/u.exerciseresults'):
    #     row = row.rstrip()
    #     exerciseresult_id, exercise_id, student_email, timestamp, num_correct, num_done = row.split('|')

    #     if type(timestamp) != datetime:
    #         timestamp = datetime.strptime(timestamp, '%d-%m-%Y')

    #     exerciseresult = ExerciseResult(exerciseresult_id=exerciseresult_id,
    #                                     exercise_id=exercise_id,
    #                                     student_email=student_email,
    #                                     timestamp=timestamp,
    #                                     num_correct=num_correct,
    #                                     num_done=num_done)

    #     db.session.add(exerciseresult)

    # db.session.commit()

    student_emails = db.session.query(Student.student_email).all()
    exercises = db.session.query(Exercise).all()

    def generate_random_date(start, end):
        """Return a random datetime between two datetime objects."""

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        return start + timedelta(seconds=random_second)

    d1 = datetime.strptime('1/1/2017 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('2/1/2017 4:50 AM', '%m/%d/%Y %I:%M %p')

    for exercise in exercises:
        # num_problems = exercise.?

        for student_email in student_emails:
            exercise_id = exercise.exercise_id
            timestamp = generate_random_date(d1, d2)
            # points = random.randint(1, 30)
            # secs_watched = random.randint(1, total_secs)
            # last_sec_watched = random.randint(secs_watched, total_secs)
            num_correct = random.randint(0, 15)
            num_done = random.randint(num_correct, 18)

            exerciseresult = ExerciseResult(exercise_id=exercise_id,
                                            student_email=student_email,
                                            timestamp=timestamp,
                                            num_correct=num_correct,
                                            num_done=num_done)

            # randomly decide whether or not to add result
            if bool(random.getrandbits(1)):
            # random_add = random.random()
            # if random_add < 0.67:
                db.session.add(exerciseresult)

    db.session.commit()


def load_videos():
    """Load videos from Khan Academy JSON into database."""

    print 'Videos'

    Video.query.delete()

    # video_string = open('static/data/sample_videos.json').read()
    video_string = open('static/data/videos.json').read()
    video_dicts = json.loads(video_string)

    i = 1

    for video in video_dicts:
        video_id = video['id']
        name = video['title']
        description = video['description']
        url = video['ka_url']
        # youtube_url = 'https://www.youtube.com/watch?v=' + video['youtube_id']
        topic = video['exam_topic']
        length = video.get('duration', None)
        order_num = i

    # for row in open('static/data/u.videos'):
    #     row = row.rstrip()
    #     video_id, name, url, length = row.split('|')

        if length:
            video = Video(video_id=video_id,
                          name=name,
                          description=description,
                          url=url,
                          # youtube_url=youtube_url,
                          topic=topic,
                          length=length,
                          order_num=order_num)

            db.session.add(video)

        i += 1

    db.session.commit()


# def load_videoresults():
#     """Load video results into database."""

#     print 'VideoResults'

#     VideoResult.query.delete()

#     videoresult_string = open('static/data/sample_videoresults.json').read()
#     videoresult_dict = json.loads(videoresult_string)

#     for videoresult in videoresult_dict:
#         student_email = videoresult['user']
#         timestamp = videoresult['last_watched']
#         points = videoresult['points']
#         secs_watched = videoresult['seconds_watched']
#         last_sec_watched = videoresult['last_second_watched']

#         video = videoresult['video']
#         # name = video['title']
#         # description = video['description']
#         url = video['ka_url']
#         # youtube_url = 'https://www.youtube.com/watch?v=' + video['youtube_id']
#         # length = video['duration']
#         video_id = db.session.query(Video.video_id).filter(Video.url == url).first()

#     # for row in open('static/data/u.videoresults'):
#     #     row = row.rstrip()
#     #     videoresult_id, video_id, student_id, timestamp, secs_watched, last_sec_watched = row.split('|')

#         if type(timestamp) != datetime:
#             # timestamp = datetime.strptime(timestamp, '%d-%m-%Y')
#             timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
#             # 2011-05-04T06:01:47Z

#         videoresult = VideoResult(video_id=video_id,
#                                   student_email=student_email,
#                                   timestamp=timestamp,
#                                   points=points,
#                                   secs_watched=secs_watched,
#                                   last_sec_watched=last_sec_watched)

#         db.session.add(videoresult)

#     db.session.commit()


def load_videoresults():
    """Load video results into database.

    Generate data drawing from existing student and video data."""

    print 'VideoResults'

    VideoResult.query.delete()

    student_emails = db.session.query(Student.student_email).all()
    videos = db.session.query(Video).all()

    def generate_random_date(start, end):
        """Return a random datetime between two datetime objects."""

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        return start + timedelta(seconds=random_second)

    d1 = datetime.strptime('1/1/2017 1:30 PM', '%m/%d/%Y %I:%M %p')
    d2 = datetime.strptime('2/1/2017 4:50 AM', '%m/%d/%Y %I:%M %p')

    for video in videos:
        total_secs = video.length

        for student_email in student_emails:
            video_id = video.video_id
            timestamp = generate_random_date(d1, d2)
            points = random.randint(1, 30)
            secs_watched = random.randint(1, total_secs)
            last_sec_watched = random.randint(secs_watched, total_secs)

            videoresult = VideoResult(video_id=video_id,
                                      student_email=student_email,
                                      timestamp=timestamp,
                                      points=points,
                                      secs_watched=secs_watched,
                                      last_sec_watched=last_sec_watched)

            # randomly decide whether or not to add result
            if bool(random.getrandbits(1)):
            # random_add = random.random()
            # if random_add < 0.67:
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
    # load_students()
    generate_students()
    load_exams()
    # load_examresults()
    # load_exercises()
    # load_exerciseresults()
    load_videos()
    # load_videoresults()
    generate_videoresults()
    generate_examresults()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    call_all_functions()
    update_pkey_seqs()
