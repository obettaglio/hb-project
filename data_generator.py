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
    exams = db.session.query(Exam).filter(Exam.class_id == 1).all()
    # videos_query = db.session.query(Video).order_by(Video.order_num)

    exam_order = 0
    completed_exams = []

    def generate_random_date(start, end):
        """Return a random datetime between two datetime objects."""

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        return start + timedelta(seconds=random_second) / 5

    # def find_exam_videos(exam_order, videos_query):
    #     """Return list of 20 video objects corresponding to exam."""

    #     skip = exam_order * 20
    #     exam_videos = videos_query.offset(skip).limit(20).all()

    #     return exam_videos

    def find_exam_videos(exam):
        """Return list of video objects corresponding to exam's exam_topic."""

        exam_topic = exam.topic
        exam_videos = db.session.query(Video).filter(Video.topic == exam_topic)\
                                             .order_by(Video.order_num).all()
        print "Adding videos for exam_topic: " + exam_topic

        return exam_videos

    for exam in exams:

        if completed_exams == []:
            start_date = db.session.query(Classroom.start_date).filter(Classroom.class_id == 1).first()[0]
        else:
            prev_exam = completed_exams[-1]
            start_date = prev_exam.timestamp

        ## identify videos assigned during exam grading period -- TO DO ##
        # exam_videos = videos_query.limit(20).all()
        # exam_videos = find_exam_videos(exam_order, videos_query)
        exam_videos = find_exam_videos(exam)

        for student_email in student_emails:

            # d1 = datetime.strptime('1/1/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
            # d2 = datetime.strptime('2/1/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
            d1 = start_date
            d2 = exam.timestamp

            for video in exam_videos:
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

        exam_order += 1
        completed_exams.append(exam)

    db.session.commit()


def generate_examresults():

    # first videoresult timestamp
    # if student hit numvideos threshold by date:
        # higher grade range

    student_emails = db.session.query(Student.student_email).filter(Student.class_id == 1).all()

    exams = db.session.query(Exam).filter(Exam.class_id == 1).order_by(Exam.timestamp).all()
    completed_exams = []

    def find_num_exam_videos(exam):
        """Return number of videos that correspond to exam's exam_topic."""

        exam_topic = exam.topic
        num_exam_videos = db.session.query(Video).filter(Video.topic == exam_topic)\
                                                 .order_by(Video.order_num).count()

        return num_exam_videos

    for exam in exams:

        exam_id = exam.exam_id
        exam_date = exam.timestamp
        # exam_topic = exam.topic

        if completed_exams == []:
            start_date = db.session.query(Classroom.start_date).filter(Classroom.class_id == 1).first()[0]
        else:
            prev_exam = completed_exams[-1]
            start_date = prev_exam.timestamp

        num_exam_videos = find_num_exam_videos(exam)

        # have to query to find exam grading period
        # first_third = datetime.strptime('1/10/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
        # second_third = datetime.strptime('1/20/2017 1:00 AM', '%m/%d/%Y %I:%M %p')
        first_third = ((exam_date - start_date) / 3) + start_date
        second_third = ((exam_date - start_date) * 2 / 3) + start_date
        print first_third, second_third

        for student_email in student_emails:
            videoresults_query = db.session.query(VideoResult)\
                                           .filter(VideoResult.student_email == student_email)\
                                           .order_by(VideoResult.timestamp)

            first_third_count = videoresults_query.filter((VideoResult.timestamp > start_date) &
                                                          (VideoResult.timestamp < first_third)).count()
            second_third_count = videoresults_query.filter((VideoResult.timestamp > first_third) &
                                                           (VideoResult.timestamp < second_third)).count()
            final_count = videoresults_query.filter((VideoResult.timestamp > second_third) &
                                                    (VideoResult.timestamp < exam_date)).count()

            print "First third: ", first_third_count
            print "Second third: ", second_third_count
            print "Final count: ", final_count

            # make realistic exam scores
            if first_third_count >= (num_exam_videos / 3):
                if second_third_count >= num_exam_videos * 2 / 3:
                    score = random.randint(90, 100)
                else:
                    score = random.randint(75, 100)
            else:
                if second_third_count >= (num_exam_videos * 3 / 5):
                    score = random.randint(75, 90)
                elif final_count >= (num_exam_videos * 2 / 3):
                    score = random.randint(60, 85)
                else:
                    score = random.randint(45, 80)

            # score = random.randint(45, 100)

            examresult = ExamResult(exam_id=exam_id,
                                    student_email=student_email,
                                    score=score)

            db.session.add(examresult)

        completed_exams.append(exam)

    db.session.commit()
