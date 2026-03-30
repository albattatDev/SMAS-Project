CREATE DATABASE SMAS_DB;
USE SMAS_DB;

CREATE TABLE Students (
    University_ID BIGINT PRIMARY KEY NOT NULL,
    FullName VARCHAR(100) NOT NULL,
    Major VARCHAR(50) NOT NULL,
    RegistrationDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Attendance (
    Attendance_ID INT AUTO_INCREMENT PRIMARY KEY,
    Student_ID BIGINT,
    AttendanceDate DATE NOT NULL,
    Status ENUM('Present', 'Absent') NOT NULL,
    FOREIGN KEY (Student_ID) REFERENCES Students(University_ID) ON DELETE CASCADE
);

/*
I recommend inserting one "dummy" student so you and Albaraa can immediately test your View/Search functions.
SQL

INSERT INTO Students (University_ID, FullName, Major) 
VALUES (2220001392, 'Abdullah Albattat', 'Computer Science');

INSERT INTO Attendance (Student_ID, AttendanceDate, Status) 
VALUES (2220001392, CURDATE(), 'Present');

*/
