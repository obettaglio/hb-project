"""Password checker. Demonstrates password hashing."""

# Generally, you never want to store users passwords in a database ---
# if you do, anyone who can query your database could learn *everyone's*
# password!
#
# Therefore, almost always, you'll store a hash of their password in your
# database. You can then hash their login-attempt password and make sure that
# matches the hash of the original password.
#
# In theory, you could use any good cryptographic hash for this, but there
# are subtle security problems if you do so:
#
# - people often pick passwords that are too short, so it could be realistic
#   to brute-force them
#
# - many hash algorithms can be run very quickly on specialized hardware,
#   making it affordable to produce "rainbow tables" of prehashed common
#   passwords
#
# Specialized password hashing libraries exist to solve these problems.
# They provide hash functions which:
#
# - "salt" a password before hashing it (salting adds lots of random characters,
#   so that shorter or common passwords will still be hard to break)
#
# - are designed in ways that are very difficult to execute in parallel,
#   defeating specialized hardware password crackers
#
# Python has an addon a library, `passlib`, which provides several of these
# password-hashing-hashes. A particularly modern and good hash in this library
# is "argon2". Here, we'll use this to check if a password matches a
# previously-hashed password.

from passlib.hash import argon2

passwd = raw_input("Enter a password: ")

hashed = argon2.hash(passwd)

del passwd

while True:
    attempt = raw_input("Verify your password: ")
    if argon2.verify(attempt, hashed):
        print "Correct!"
        break
    else:
        print "Incorrect!"
