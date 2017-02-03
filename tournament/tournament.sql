-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players(player_id SERIAL PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE matches(match_id SERIAL PRIMARY KEY, winner INTEGER references players(player_id) ON DELETE CASCADE,loser INTEGER references players(player_id) ON DELETE CASCADE);

CREATE VIEW standings AS
  SELECT players.player_id,players.name,
  (SELECT count(matches.winner)
      FROM matches
      WHERE players.player_id = matches.winner)
      AS total_wins,
  (SELECT count(matches.match_id)
      FROM matches
      WHERE players.player_id = matches.winner
      OR players.player_id = matches.loser)
      AS total_matches
  FROM players
  ORDER BY total_wins DESC, total_matches DESC;


--unique ID for each player SERIAL
--Count using SQL aggregations to count things or add them up
--use VIEWS
