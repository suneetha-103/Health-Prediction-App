
CREATE DATABASE health_db;
USE health_db;

CREATE TABLE patients(
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    email VARCHAR(100) NOT NULL,
    glucose FLOAT NOT NULL,
    haemoglobin FLOAT NOT NULL,
    cholesterol FLOAT NOT NULL,
    remarks TEXT
);

-- select * from patients
