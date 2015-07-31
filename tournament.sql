-- Luke Sheppard
-- lshep.usc[(at)]gmail.com
-- Project 2 of the Fullstack Nanodegree at Udacity.
-- July 31, 2015

-- This SQL file is for the final assignment for the Udacity Relational 
-- Databases course as part of the Fullstack Nanodegree. It should accompany 
-- the following three files:

--   README.txt
--   tournament.py
--   tournament_test.py

-- make sure we are not stumbling on a previous db of the same name 
DROP DATABASE IF EXISTS tournament;

CREATE database tournament; 

-- make sure we are connecting to the right db 
\c tournament

-- Table definitions for the tournament project.
CREATE TABLE playernames (
id serial PRIMARY KEY,
name text);

CREATE TABLE matches (
match_id serial PRIMARY KEY,
winner int REFERENCES playernames (id),
loser int REFERENCES playernames (id)
);

-- create a view that returns the players' wins with the required fields
CREATE VIEW player_wins AS
SELECT playernames.id, playernames.name, COUNT(matches.winner) AS wins
FROM playernames LEFT JOIN matches
ON playernames.id = matches.winner
GROUP BY playernames.id,  winner
