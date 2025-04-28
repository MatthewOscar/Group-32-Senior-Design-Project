/*
*********************************************************************
Name: EGN 4952C MDCS Database
Author: Matthew Wyatt
Date: February 1, 2024
Link: https://phpmyadmin.co
*********************************************************************
*/

/* Creating MySQL Database */
CREATE DATABASE /*!32312 IF NOT EXISTS*/`termprojectdatabase` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `termprojectdatabase`;

/*Table structure for table Drones */
CREATE TABLE Drones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    status VARCHAR(50) NOT NULL,
    battery FLOAT NOT NULL,
    altitude FLOAT NOT NULL,
    speed FLOAT NOT NULL,
    is_armed BOOLEAN NOT NULL,
    has_collided BOOLEAN NOT NULL
);

/*Data for the Drones table, which may be modified using the ExpressJS or Python APIs*/
INSERT INTO Drones (name, status, battery, altitude, speed, is_armed, has_collided)
VALUES
('Drone1', 'Active', 75.5, 120.3, 15.2, TRUE, FALSE),
('Drone2', 'Idle', 50.0, 0.0, 0.0, FALSE, FALSE),
('Drone3', 'Charging', 20.0, 0.0, 0.0, FALSE, FALSE),
('Drone4', 'Landed', 90.0, 0.0, 0.0, FALSE, FALSE);

/*View the sample Drones table*/
SELECT * FROM Drones;