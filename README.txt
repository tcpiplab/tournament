Luke Sheppard
lshep.usc[(at)]gmail.com
Project 2 of the Fullstack Nanodegree at Udacity.
July 24, 2015

This README file is for the final assignment for the Udacity Relational Databases course as part of the Fullstack Nanodegree. It should accompany the following three files:

  tournament.py
  tournament.sql
  tournament_test.py

The first two were written by me, the latter is just a copy of the test script that I downloaded from the course materials.

All code was developed in a vagrant 1.7.2 VM running on Mac OS X 10.10.4. The guest OS was Ubuntu 14.04.2 LTS. Inside that VM was python 2.7 and PostgreSQL 9.3.6.


To get this environment running so that the test script will work, you must do these, in order:

On the Mac, depending on where you've installed vagrant, cd into the apropriate directory. For me it was:

  ~/fullstack/vagrant/tournament

Then,

  vagrant up

Then, after it comes up,

  vagrant ssh

You'll then be inside the Linux environment and be able to run everything. If you have problems, you may need to install the psycopg2 module for Python, or you may need to manually start the postgres daemon.
