-- Création de la DB et de l'utilisateur
CREATE DATABASE IF NOT EXISTS iot_p1
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS'iot'@'localhost' IDENTIFIED BY 'iot';
GRANT ALL PRIVILEGES ON iot_p1.* TO 'iot'@'localhost';
FLUSH PRIVILEGES;

-- Commande pour se postionner sur la bonne DB
USE iot_p1;

-- Table pour les évènemements
CREATE TABLE events (
    id BIGINT UNSIGNED AUTO_INCREMENT,
    commande_texte VARCHAR(32),
    intention_detectee VARCHAR(32),
    resultat VARCHAR(32),
    ts_utc VARCHAR(32) NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_events_ts (ts_utc)
);