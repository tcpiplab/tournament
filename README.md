Project 2 of the Fullstack Nanodegree at Udacity
================================================
Relational Databases Course
---------------------------

This is my submission for the final assignment of the Udacity Relational Databases course as part of the Fullstack Nanodegree. Follow these instructions in order.

Main Menu                  |  Show Player Standings    | Generate Next Pairings
:-------------------------:|:-------------------------:|:-------------------------:|
![Screenshot of main menu](https://cloud.githubusercontent.com/assets/816651/10701941/4843b01a-797b-11e5-8c24-7f73c6b31b3a.png)  |  ![Screenshot of player standings](https://cloud.githubusercontent.com/assets/816651/10703772/236bddd8-7987-11e5-822f-31405c1aee37.png) | ![Screenshot of next pairings](https://cloud.githubusercontent.com/assets/816651/10708441/315ecc3a-79bd-11e5-95db-6b54aaade132.png)

PURPOSE
-------
The `tournament.py` script will store the win/lose outcomes of game matches between pairs of players and generate pairings for [Swiss-System tournaments][0].

FILES
-----
This README file should accompany the following three files:

* `tournament.py`
* `tournament.sql`
* `tournament_test.py`

The first two were written by me, the latter is just a copy of the test script that I downloaded from the course materials.

PREREQUISITES
-------------
All code was developed on Ubuntu 14.04.2 LTS, python 2.7 and PostgreSQL 9.3.6. You will need to [install the psycopg2 module][1] for Python.

Start the [postgres daemon][2].

BUILD
-----
To create the database and its tables, run this command:

    psql -f tournament.sql


TEST
----
To test the `tournament.py` script, run this command:

    python tournament_test.py

RUN
---
To run the `tournament.py` script, run this command:

    python tournament.py

This will display a menu in a terminal based interface where you select menu
item numbers to call the various functions, including exiting the script if you
choose.

[0]:https://en.wikipedia.org/wiki/Swiss-system_tournament
[1]:http://initd.org/psycopg/docs/install.html
[2]:http://www.postgresql.org/docs/9.3/static/server-start.html
