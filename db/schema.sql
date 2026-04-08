-- Création de la DB et de l'utilisateur
CREATE DATABASE IF NOT EXISTS iot_p1
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

CREATE USER IF NOT EXISTS'iot'@'localhost' IDENTIFIED BY 'iot';
GRANT ALL PRIVILEGES ON iot_p1.* TO 'iot'@'localhost';
FLUSH PRIVILEGES;

-- Commande pour se postionner sur la bonne DB
USE iot_p1;

-- Table pour la télémetrie
CREATE TABLE telemetry (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    device VARCHAR(32) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    value DOUBLE NULL,
    unit VARCHAR(16) NULL,
    ts_utc VARCHAR(30) NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_telemetry_device_ts (device, ts_utc)
);
-- Table pour les évènemements
CREATE TABLE events (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    device VARCHAR(32) NOT NULL,
    topic VARCHAR(255) NOT NULL,
    payload TEXT NOT NULL,
    ts_utc VARCHAR(30) NOT NULL,
    PRIMARY KEY (id),
    INDEX idx_events_device_ts (device, ts_utc)
);