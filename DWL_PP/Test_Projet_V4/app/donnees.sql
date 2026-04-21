CREATE DATABASE IF NOT EXISTS watchlist_api CHARACTER SET utf8mb4;

USE watchlist_api;

CREATE TABLE IF NOT EXISTS watchlist (
    id VARCHAR(100) PRIMARY KEY,
    film_name VARCHAR(100) NOT NULL,
    poster VARCHAR(100) NOT NULL,
    background VARCHAR(100) NOT NULL,
    etat VARCHAR(100) NOT NULL
);