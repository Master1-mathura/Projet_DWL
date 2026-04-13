CREATE DATABASE watchlist_api CHARACTER SET utf8mb4;

USE watchlist_api;

CREATE TABLE watchlist (
    filmID INT PRIMARY KEY,
    film_name VARCHAR(100) NOT NULL,
    watched BOOLEAN DEFAULT FALSE

);