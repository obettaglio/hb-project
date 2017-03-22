# KhanLine

KhanLine is a data access tool for teachers who use technology in the classroom. A teacher can easily see how online preparation on Khan Academy is related to in-class success on tests, making future lesson plans more effective than ever!

To view a comprehensive screencast of KhanLine's features, [click here](https://www.youtube.com/watch?v=q1jQHC-jCOA).


## Tech Stack

__Frontend:__ d3.js, JavaScript, jQuery, HTML5, Bootstrap<br>
__Backend:__ Python, Flask, PostgreSQL, SQLAlchemy<br>
__APIs:__ Khan Academy<br>

## Features

Users register by connecting to their Khan Academy coach account. The register button takes them to Khan Academy's site, where they are prompted to accept the request for access.

Course sections contain student and exam information, as well as a d3.js graph depicting video views and exam averages over time.

![Course section](/static/images/readme-images/course-section.gif)
<br><br>

Each exam page contains an easy-to-read list of scores on the left, as well as several visually-impressive graphs of the effects of each video within an exam topic. Using this chart, a teacher can quickly identify the videos that are most associated with success.

![Exam graph](/static/images/readme-images/exam-graph.gif)
<br><br>

As a teacher adds a student's score, the table and graphs dynamically update with the new data.

![Add score](/static/images/readme-images/add-score.gif)
<br><br>

## Setup

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

Obtain a consumer key and secret from [Khan Academy's API](https://github.com/Khan/khan-api/wiki/Khan-Academy-API-Authentication). Save both to a file `secrets.sh`. The file should look like this:

```
export KHAN_CONSUMER_KEY='abc'
export KHAN_CONSUMER_SECRET='def'
```

Source the new file containing API keys to the current shell:

```
$ source secrets.sh
```

Create a database:

```
$ createdb khanline
```

Create all tables and seed example data:

```
$ python seed.py
```

Run the app:

```
$ python server.py
```

Access the site at this local link:

```
http://localhost:5000/
```

## Next Steps for KhanLine

* Integrate Schoology's API to dynamically retreive exam score data