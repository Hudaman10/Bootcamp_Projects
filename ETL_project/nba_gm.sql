CREATE DATABASE nba_db;

USE nba_db;


CREATE TABLE nba_info (
	id INTEGER auto_increment primary KEY,
    player_name TEXT,
    salary INT,
    season_start INT,
    season_end INT,
    team_name TEXT,
    draft_rank INT,
    draft INT,
    position TEXT,
    height TEXT,
    weight FLOAT,
    birth_date TEXT,
    college TEXT
);

SELECT * FROM nba_info;