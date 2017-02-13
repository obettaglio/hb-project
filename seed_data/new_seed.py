import json

from server import app

from model import Student, connect_to_db, db

# user_string = open('sample_user.json').read()
# user_dict = json.loads(user_string)

# user_id = user_dict['user_id']

# username = user_dict['username']

# nickname = user_dict['nickname'].split(" ")
# f_name, l_name = nickname

# email = user_dict['email']

# num_students = user_dict['students_count']


def load_students():
    """Load students from Khan Academy JSON into database."""

    print "Students"

    Student.query.delete()

    student_string = open('sample_student.json').read()
    student_dict = json.loads(student_string)

    student_id = student_dict['user_id']
    email = student_dict['email']
    nickname = student_dict['nickname'].split(" ")
    f_name, l_name = nickname
    khan_id = student_dict['username']

    student = Student(student_id=student_id,
                      email=email,
                      f_name=f_name,
                      l_name=l_name,
                      khan_id=khan_id)

    db.session.add(student)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    db.create_all()

    load_students()
    # update_pkey_seqs()
