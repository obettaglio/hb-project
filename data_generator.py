"""Generator of users, students, exam results, and Khan Academy activities."""

import random
from datetime import datetime, timedelta
from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)
from model import db


f_names = ["Meggie", "Leslie", "Agne", "Kelly", "Katie", "Ahmad", "Dennis",
           "Ariella", "Matthew", "Ethan", "William", "Catherine", "Jason",
           "Serena", "Joel", "Henry", "Conor", "Samuel", "Danielle", "Tony"]

l_names = ["Smith", "Johnson", "Inge", "Glassman", "Weinberg", "Carroll",
           "Mahnken", "Yeh", "Goodman", "Winchester", "Burton", "Conrad",
           "Chen", "Boyette", "Lonne", "Fischbach", "Wickham", "Horvatic",
           "Yoder", "Hardin"]


def generate_students():
    """Generate mock students, drawing first and last names from a list of options."""

    for f_name in f_names:

        random_index = random.randint(0, len(l_names) - 1)
        l_name = l_names[random_index]
        del l_names[random_index]

        khan_username = "khanstudent" + f_name[:2].lower() + l_name[:5].lower()
        student_email = khan_username + "@genstudent.com"
        # password = khan_username + str(123)
        class_id = 1

        student = Student(student_email=student_email,
                          f_name=f_name,
                          l_name=l_name,
                          khan_username=khan_username,
                          class_id=class_id)

        db.session.add(student)

    db.session.commit()


def generate_videoresults():
    """Generate videoresults for each student.

    Generated date includes: timestamp, points, secs_watched, last_sec_watched.
    Randomly choose whether or not to add videoresult."""

    VideoResult.query.delete()

    student_emails = db.session.query(Student.student_email).all()
    videos = db.session.query(Video).order_by(Video.order_num).all()

    def generate_random_date(start, end):
        """Return a random datetime between two datetime objects."""

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        return start + timedelta(seconds=random_second) / 5

    for student_email in student_emails:

        d1 = datetime.strptime('1/1/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
        d2 = datetime.strptime('2/1/2017 1:00 AM', '%m/%d/%Y %I:%M %p')

        for video in videos:
            total_secs = video.length

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
            # if bool(random.getrandbits(1)):
            random_add = random.random()
            print random_add
            if random_add < 0.67:
                db.session.add(videoresult)
                d1 = timestamp

    db.session.commit()


def generate_examresults():

    # first videoresult timestamp
    # if student hit numvideos threshold by date:
        # higher grade range

    student_emails = db.session.query(Student.student_email).all()

    exam = db.session.query(Exam).filter(Exam.exam_id == 1).first()

    exam_id = exam.exam_id
    videos_count = db.session.query(Video).count()
    print "Videos count: ", videos_count

    # have to query to find exam grading period
    first_third = datetime.strptime('1/10/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
    second_third = datetime.strptime('1/20/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
    exam_date = exam.timestamp

    for student_email in student_emails:
        videoresults_query = db.session.query(VideoResult)\
                                       .filter(VideoResult.student_email == student_email)\
                                       .order_by(VideoResult.timestamp)

        first_third_count = videoresults_query.filter(VideoResult.timestamp < first_third).count()
        second_third_count = videoresults_query.filter((VideoResult.timestamp > first_third) &
                                                       (VideoResult.timestamp < second_third)).count()
        final_count = videoresults_query.filter((VideoResult.timestamp > second_third) &
                                                (VideoResult.timestamp < exam_date)).count()

        print "First third: ", first_third_count
        print "Second third: ", second_third_count
        print "Final count: ", final_count

        # make realistic exam scores
        if first_third_count >= (videos_count / 4):
            if second_third_count >= videos_count / 3:
                score = random.randint(90, 100)
            else:
                score = random.randint(75, 100)
        else:
            if second_third_count >= (videos_count / 3):
                score = random.randint(75, 90)
            elif final_count >= (videos_count * 2 / 3):
                score = random.randint(60, 85)
            else:
                score = random.randint(45, 80)

        # score = random.randint(45, 100)

        examresult = ExamResult(exam_id=exam_id,
                                student_email=student_email,
                                score=score)

        db.session.add(examresult)

    db.session.commit()
