Luke Sheppard
lshep.usc[(at)]gmail.com
Project 2 of the Fullstack Nanodegree at Udacity.
July 25, 2015

This README file is for the final assignment for the Udacity Relational Databases course as part of the Fullstack Nanodegree. Follow these instructions in order.


PURPOSE
The tournament.py script will store the win/lose outcomes of game matches between pairs of players and generate pairings for Swiss-System tournaments, which are described at this URL:

  https://en.wikipedia.org/wiki/Swiss-system_tournament 


FILES 
This README file should accompany the following three files: 

  tournament.py
  tournament.sql
  tournament_test.py

The first two were written by me, the latter is just a copy of the test script that I downloaded from the course materials.


PREREQUISITES
All code was developed on Ubuntu 14.04.2 LTS, python 2.7 and PostgreSQL 9.3.6. You will need to install the psycopg2 module for Python, as described at:

  http://initd.org/psycopg/docs/install.html

The postgres daemon must be running. This URL shows how to do that:

  http://www.postgresql.org/docs/9.3/static/server-start.html


BUILD
To create the database and its tables, run this command:

  psql -f tournament.sql


TEST
To test the tournament.py script, run this command:

  python tournament_test.py


RUN
To run the tournament.py script, run this command:

  python tournament.py

This will display a menu based interface where you select menu item numbers to call the various functions, including exiting the script if you choose. 

