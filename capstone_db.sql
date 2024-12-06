DROP DATABASE IF EXISTS capstone_db;


CREATE DATABASE capstone_db;

\c capstone_db;

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username VARCHAR(50) UNIQUE,
  password VARCHAR,
  email VARCHAR,
  first_name VARCHAR,
  last_name  VARCHAR
);

CREATE TABLE playlists (
  playlist_id Serial PRIMARY KEY,
  playlist_title VARCHAR,
  owner_id INTEGER,
  receiver_id INTEGER,
  FOREIGN KEY (owner_id) REFERENCES users(user_id),
  FOREIGN KEY (receiver_id) REFERENCES users(user_id)
  
);

CREATE TABLE shared_songs (
  shared_song_id Serial PRIMARY KEY,
  song_id TEXT,
  song_name TEXT,
  sender_username VARCHAR,
  receiver_username VARCHAR,
  note VARCHAR,
  url VARCHAR,
  FOREIGN KEY (sender_username) REFERENCES users(username),
  FOREIGN KEY (receiver_username) REFERENCES users(username)
);

CREATE TABLE lyrics (
  lyric_id INTEGER PRIMARY KEY,
  lyric TEXT,
  song VARCHAR,
  artist VARCHAR,
  owner_id INTEGER,
  FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- create a table for sharing playlists
--  columns for table
-- table for user id(sharer), user that will receive item, song or playlist id

