-- Table definitions for the tournament project.
--
CREATE database tournament; 

CREATE TABLE playernames (
id serial PRIMARY KEY,
name text);

CREATE TABLE matches (
match_id serial PRIMARY KEY,
player_1 int REFERENCES playernames (id),
player_2 int REFERENCES playernames (id),
winner int REFERENCES playernames (id),
loser int REFERENCES playernames (id)
);


