"""
Database module - handles all MySQL connections and queries.
This is the ONLY place where database code lives!
Everything else just calls functions from here.
"""

import mysql.connector
from tkinter import messagebox
from config import DB_CONFIG


def get_db_connection():
    """
    Create a connection to the MySQL database.
    
    WHY THIS FUNCTION EXISTS:
    - Centralized connection logic
    - If connection fails, error handling is in ONE place
    - Easy to debug database issues
    
    RETURNS:
    - mysql.connector.MySQLConnection object if successful
    - None if connection fails (error message shown to user)
    
    EXAMPLE:
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        # do database stuff
        conn.close()
    """
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Connection Failed: {err}")
        return None


def insert_student(university_id, full_name, major):
    """
    Insert a new student into the database.
    
    PARAMETERS:
    - university_id: 10-digit ID (as string)
    - full_name: Student's full name
    - major: Student's major/field of study
    
    RETURNS:
    - True if successful
    - False if failed (error message shown to user)
    
    EXAMPLE:
    if insert_student("1234567890", "Ahmed Ali", "Computer Science"):
        print("Student added!")
    else:
        print("Failed to add student")
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Students (University_ID, FullName, Major) VALUES (%s, %s, %s)"
        cursor.execute(sql, (university_id, full_name, major))
        conn.commit()  # Save changes to database
        messagebox.showinfo("Success", f"Student {full_name} registered successfully!")
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not register student: {err}")
        return False
    finally:
        conn.close()


def get_all_students():
    """
    Retrieve all students from the database.
    
    WHY SEPARATE FUNCTION:
    - Searching students is different from inserting
    - Fetching (SELECT) is different from writing (INSERT)
    
    RETURNS:
    - List of tuples: [(id, name, major), (id, name, major), ...]
    - None if query fails
    
    EXAMPLE:
    students = get_all_students()
    for student in students:
        print(student)  # Prints: (1234567890, 'Ahmed', 'CS')
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        sql = "SELECT University_ID, FullName, Major FROM Students"
        cursor.execute(sql)
        results = cursor.fetchall()  # Get all rows
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not retrieve students: {err}")
        return None
    finally:
        conn.close()


def delete_student(university_id):
    """
    Delete a student from the database.
    
    PARAMETERS:
    - university_id: ID of student to delete
    
    RETURNS:
    - True if deleted
    - False if failed or not found
    
    NOTE: Also deletes attendance records (database handles this with CASCADE)
    
    EXAMPLE:
    if delete_student("1234567890"):
        print("Student deleted")
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        sql = "DELETE FROM Students WHERE University_ID = %s"
        cursor.execute(sql, (university_id,))
        conn.commit()
        
        if cursor.rowcount > 0:  # Check if a row was deleted
            messagebox.showinfo("Success", "Student deleted successfully!")
            return True
        else:
            messagebox.showwarning("Warning", "Student not found!")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not delete student: {err}")
        return False
    finally:
        conn.close()


# ===== ATTENDANCE FUNCTIONS =====

def insert_attendance(university_id, date, status):
    """
    Log attendance for a student.
    
    PARAMETERS:
    - university_id: Student's ID
    - date: Date in format 'YYYY-MM-DD' (e.g., '2024-05-04')
    - status: Either 'Present' or 'Absent'
    
    RETURNS:
    - True if successful
    - False if failed
    
    EXAMPLE:
    if insert_attendance("1234567890", "2024-05-04", "Present"):
        print("Attendance logged!")
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO Attendance (Student_ID, AttendanceDate, Status) VALUES (%s, %s, %s)"
        cursor.execute(sql, (university_id, date, status))
        conn.commit()
        messagebox.showinfo("Success", f"Attendance logged for {university_id}!")
        return True
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not log attendance: {err}")
        return False
    finally:
        conn.close()


def get_attendance_by_student(university_id):
    """
    Get all attendance records for a specific student.
    
    PARAMETERS:
    - university_id: Student's ID
    
    RETURNS:
    - List of attendance records: [(date, status), (date, status), ...]
    - None if failed
    
    EXAMPLE:
    records = get_attendance_by_student("1234567890")
    for record in records:
        print(f"Date: {record[0]}, Status: {record[1]}")
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        sql = "SELECT AttendanceDate, Status FROM Attendance WHERE Student_ID = %s ORDER BY AttendanceDate"
        cursor.execute(sql, (university_id,))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not retrieve attendance: {err}")
        return None
    finally:
        conn.close()


def get_all_attendance():
    """
    Get all attendance records from all students.
    
    RETURNS:
    - List of all attendance: [(id, date, status), ...]
    - None if failed
    
    EXAMPLE:
    all_records = get_all_attendance()
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        sql = "SELECT Student_ID, AttendanceDate, Status FROM Attendance ORDER BY AttendanceDate DESC"
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Could not retrieve attendance: {err}")
        return None
    finally:
        conn.close()
