-- Database and table definitions for the Tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- create db and connect
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament;

-- drop tables - because of foreign keys, order is important
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;

-- create tables
CREATE TABLE IF NOT exists tournaments(
    tid serial PRIMARY KEY, -- tournament id
    tname text              -- tournament name
);
ALTER SEQUENCE tournaments_tid_seq RESTART WITH 100;
INSERT INTO tournaments (tname) values('Default Tournament');
INSERT INTO tournaments (tname) values('San Diego Western Regionals');
INSERT INTO tournaments (tname) values('Las Vegas Finals');
INSERT INTO tournaments (tname) values('Kansas City Midwestern');
INSERT INTO tournaments (tname) values('New York Eastern Championships');
INSERT INTO tournaments (tname) values('Seattle NorthPac');


CREATE TABLE IF NOT exists players(
    tid integer REFERENCES tournaments (tid), -- tournament id
    pid serial primary key,                   -- player id
    name text
);

INSERT INTO players (tid, name) values(102, 'Billy Bob Thornton');
INSERT INTO players (tid, name) values(102, 'Christian Bale');
INSERT INTO players (tid, name) values(102, 'Johnny Depp');
INSERT INTO players (tid, name) values(102, 'Brad Pitt');


CREATE TABLE IF NOT exists matches (
    tid integer REFERENCES tournaments (tid),
    winner integer REFERENCES players (pid),
    loser integer REFERENCES players (pid)
);

/*
INSERT INTO matches (tid, winner, loser) values(102,1,5);
INSERT INTO matches (tid, winner, loser) values(102,4,2);
INSERT INTO matches (tid, winner, loser) values(102,2,1);
INSERT INTO matches (tid, winner, loser) values(102,5,4);
INSERT INTO matches (tid, winner, loser) values(102,5,2);
INSERT INTO matches (tid, winner, loser) values(102,5,1);
*/
