CREATE DATABASE IF NOT EXISTS watchlist_api CHARACTER SET utf8mb4;

USE watchlist_api;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    mdp VARCHAR(255) NOT NULL
    );

CREATE TABLE IF NOT EXISTS watchlist (
    imdb_id VARCHAR(100),
    user_id INT NOT NULL,
    film_name VARCHAR(100) NOT NULL,
    poster VARCHAR(255) NOT NULL,
    background VARCHAR(255) NOT NULL,
    etat VARCHAR(100) NOT NULL,

    PRIMARY KEY (imdb_id, user_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO users (id, username, mdp)
VALUES (1, 'Admin DWL', 'faux_hash_temporaire');