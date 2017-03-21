#KhanLine

KhanLine is a data access tool for teachers who use technology in the classroom. A teacher can easily see how online preparation on Khan Academy is related to in-class success on tests, making future lesson plans more effective than ever!


##Tech Stack

Frontend: d3.js, JavaScript, jQuery, HTML5, Bootstrap
Backend: Python, Flask, PostgreSQL, SQLAlchemy
APIs: Khan Academy

##Features

Users register by connecting to their Khan Academy coach account.

Course sections contain student and exam information.

Using D3, KhanLine creates tabular and visual analytics showing the relationship between student progress on Khan Academy and performance on in-class exams.

As a teacher adds a student's score, the graphs dynamically update with the new data.

##Setup

To run KhanLine on your local computer, please proceed with these steps.

Clone repository:

```
$ git clone https://github.com/obettaglio/khan-line.git
```

Create and activate a virtual environment:

```
$ virtualenv env
$ source env/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```

Aquire an API consumer key and secret for [Khan Academy](https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication). Save them to a file `secrets.sh`. The file should look like this:

```
export KHAN_CONSUMER_KEY='abc'
export KHAN_CONSUMER_SECRET='def'
```

Create database:

```
$ createdb khanline
```

Create all tables and seed example data:

```
$ python model.py
$ python seed.py
```

Run the app:

```
$ python server.py
```

##Next Steps for KhanLine

*Integrate Schoology's API to dynamically retreive exam score data