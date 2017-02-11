import json

user_string = open('sample_user.json').read()
user_dict = json.loads(user_string)

user_id = user_dict['user_id']

# student_summary = user_dict['student_summary']

username = user_dict['username']

nickname = user_dict['nickname'].split(" ")
f_name, l_name = nickname

email = user_dict['email']

num_students = user_dict['students_count']
