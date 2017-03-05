"""Generator of users, students, exam results, and Khan Academy activities."""

from model import (User, Student, Subject, Classroom, Exam, ExamResult, Exercise,
                   ExerciseResult, Video, VideoResult)
from model import db
from datetime import datetime, timedelta
import random
import string


f_names = ["Meggie", "Leslie", "Agne", "Kelly", "Katie", "Ahmad", "Dennis",
           "Ariella", "Matthew", "Ethan", "William", "Catherine", "Jason",
           "Serena", "Joel", "Henry", "Conor", "Samuel", "Danielle", "Tony"]

l_names = ["Smith", "Johnson", "Inge", "Glassman", "Weinberg", "Carroll",
           "Mahnken", "Young", "Goodman", "Winchester", "Burton", "Conrad",
           "Chen", "Boyette", "Lonne", "Fischbach", "Wickham", "Horvatic",
           "Yoder", "Hardin"]


def generate_password():
    """Generate 8-character alphanumeric password."""

    chars = string.letters + string.digits
    length = 8
    password = ''.join(random.choice(chars) for _ in range(length))

    return password


def generate_students():
    """Generate mock students, drawing first and last names from a list of options."""

    print 'Generating Students'

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


def generate_demo_student():
    """Generate mock student in class without examresults to be used in product demo."""

    print 'Generating Demo Student'

    student_email = 'khanstudentobbetta@genstudent.com'
    f_name = 'Olivia'
    l_name = 'Bettaglio'
    khan_username = 'khanstudentobbetta'
    class_id = 1
    demo = True

    demo_student = Student(student_email=student_email,
                           f_name=f_name,
                           l_name=l_name,
                           khan_username=khan_username,
                           class_id=class_id,
                           demo=demo)

    db.session.add(demo_student)
    db.session.commit()


def generate_videoresults():
    """Generate videoresults for each student.

    Generated date includes: timestamp, points, secs_watched, last_sec_watched.
    Randomly choose whether or not to add videoresult."""

    print 'Generating VideoResults'

    VideoResult.query.delete()

    student_emails = db.session.query(Student.student_email).all()
    exams = db.session.query(Exam).filter(Exam.class_id == 1).all()

    exam_order = 0
    completed_exams = []

    def generate_random_date(start, end, grading_period):
        """Return a random datetime between two datetime objects."""

        delta = end - start
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)

        grading_period = (grading_period).days
        denominator = max((grading_period / 7), 3)

        return start + timedelta(seconds=random_second) / denominator

    def find_exam_videos(exam):
        """Return list of video objects corresponding to exam's exam_topic."""

        exam_topic = exam.topic
        exam_videos = db.session.query(Video).filter(Video.topic == exam_topic)\
                                             .order_by(Video.order_num).all()
        print "Adding videoresults for exam_topic: " + exam_topic

        return exam_videos

    for exam in exams:

        if completed_exams == []:
            start_date = db.session.query(Classroom.start_date).filter(Classroom.class_id == 1).first()[0]
        else:
            prev_exam = completed_exams[-1]
            start_date = prev_exam.timestamp

        exam_videos = find_exam_videos(exam)
        num_exam_videos = len(exam_videos)

        for student_email in student_emails:

            d1 = start_date
            d2 = exam.timestamp
            grading_period = (d2 - d1)

            for video in exam_videos:
                total_secs = video.length

                video_id = video.video_id
                timestamp = generate_random_date(d1, d2, grading_period)
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

                if num_exam_videos > 12:
                    random_add = min((random_add + 0.15), 1)
                elif num_exam_videos > 8:
                    random_add = min((random_add + 0.05), 1)

                if random_add > 0.33:
                    db.session.add(videoresult)
                    d1 = timestamp

        exam_order += 1
        completed_exams.append(exam)

    db.session.commit()


def generate_examresults():
    """Generate examresults for each student.

    Score range depends on student's videoresult data."""

    print 'Generating ExamResults'

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

        if completed_exams == []:
            start_date = db.session.query(Classroom.start_date).filter(Classroom.class_id == 1).first()[0]
        else:
            prev_exam = completed_exams[-1]
            start_date = prev_exam.timestamp

        num_exam_videos = find_num_exam_videos(exam)
        print "Num exam videos: ", num_exam_videos

        first_third_date = ((exam_date - start_date) / 3) + start_date
        second_third_date = ((exam_date - start_date) * 2 / 3) + start_date

        for student_email in student_emails:

            demo = db.session.query(Student.demo).filter(Student.student_email == student_email).first()[0]

            if demo is False:

                videoresults_query = db.session.query(VideoResult)\
                                               .filter(VideoResult.student_email == student_email)\
                                               .order_by(VideoResult.timestamp)

                first_third_count = videoresults_query.filter((VideoResult.timestamp > start_date) &
                                                              (VideoResult.timestamp < first_third_date)).count()
                second_third_count = videoresults_query.filter((VideoResult.timestamp > start_date) &
                                                               (VideoResult.timestamp < second_third_date)).count()
                final_count = videoresults_query.filter((VideoResult.timestamp > start_date) &
                                                        (VideoResult.timestamp < exam_date)).count()

                # A-Bs
                if first_third_count >= (num_exam_videos / 3):
                    # consistently strong
                    if second_third_count >= num_exam_videos * 2 / 3:
                        score = random.randint(90, 100)
                    # started strong, finished weak
                    else:
                        score = random.randint(80, 95)
                # B-Fs
                else:
                    # kicked their butts into gear later
                    if second_third_count >= (num_exam_videos * 2 / 3):
                        score = random.randint(80, 90)
                    # almost finished
                    elif final_count >= (num_exam_videos * 4 / 5):
                        score = random.randint(60, 85)
                    # didn't get close to finishing
                    else:
                        score = random.randint(45, 80)

                examresult = ExamResult(exam_id=exam_id,
                                        student_email=student_email,
                                        score=score)

                db.session.add(examresult)

        completed_exams.append(exam)

    db.session.commit()
