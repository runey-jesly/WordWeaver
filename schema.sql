-- WordWeaver MySQL schema
-- Run this once in MySQL before starting the app:
--   mysql -u root -p < schema.sql

CREATE DATABASE IF NOT EXISTS wordweaver;
USE wordweaver;

CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS stories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title TEXT,
    author TEXT,
    genre TEXT,
    characters TEXT,
    setting TEXT,
    content TEXT
);
