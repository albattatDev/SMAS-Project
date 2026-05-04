"""
FEATURE 2: Attendance Logging Module
This module handles ALL attendance-related business logic.

WHAT THIS DOES:
- Validates attendance input (date, status)
- Calls database functions to save/retrieve attendance
- Shows success/error messages to user

WHY SEPARATE:
- Attendance logic is different from registration
- Can be tested independently
- Easy to update without touching other features
"""

from tkinter import messagebox
from datetime import datetime
from core.database import insert_attendance, get_attendance_by_student, get_all_attendance


def log_attendance(university_id, date, status):
    """
    Log attendance for a student on a specific date.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    - date: Date in format 'YYYY-MM-DD' (e.g., '2024-05-04')
    - status: Either 'Present' or 'Absent'
    
    RETURNS:
    - True if logged successfully
    - False if validation failed or database error
    
    VALIDATION CHECKS:
    1. All fields must be filled (not empty)
    2. Date must be valid (YYYY-MM-DD format)
    3. Date must not be in the future
    4. Status must be 'Present' or 'Absent'
    5. University ID must be 10 digits
    
    EXAMPLE:
    if log_attendance("1234567890", "2024-05-04", "Present"):
        print("Attendance logged!")
    else:
        print("Failed!")
    """
    
    # ===== VALIDATION CHECKS =====
    
    # Check 1: All fields filled?
    if not university_id or not date or not status:
        messagebox.showwarning("Validation Error", "All fields are required!")
        return False
    
    # Check 2: University ID is 10 digits?
    if len(university_id) != 10 or not university_id.isdigit():
        messagebox.showwarning(
            "Validation Error", 
            "University ID must be exactly 10 digits!"
        )
        return False
    
    # Check 3: Date format is valid?
    try:
        attendance_date = datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        messagebox.showwarning(
            "Validation Error", 
            "Date must be in YYYY-MM-DD format (e.g., 2024-05-04)!"
        )
        return False
    
    # Check 4: Date is not in the future?
    if attendance_date > datetime.now():
        messagebox.showwarning(
            "Validation Error", 
            "Cannot log attendance for future dates!"
        )
        return False
    
    # Check 5: Status is valid?
    if status not in ['Present', 'Absent']:
        messagebox.showwarning(
            "Validation Error", 
            "Status must be 'Present' or 'Absent'!"
        )
        return False
    
    # ===== IF ALL VALIDATION PASSED =====
    # Call database function to insert attendance
    success = insert_attendance(university_id, date, status)
    return success


def get_student_attendance(university_id):
    """
    Get all attendance records for a specific student.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    
    RETURNS:
    - List of attendance records: [(date, status), ...]
    - None if database error
    - Empty list if no records found
    
    EXAMPLE:
    records = get_student_attendance("1234567890")
    for record in records:
        print(f"Date: {record[0]}, Status: {record[1]}")
    """
    
    if not university_id:
        messagebox.showwarning("Error", "Enter a university ID!")
        return []
    
    if len(university_id) != 10 or not university_id.isdigit():
        messagebox.showwarning(
            "Validation Error", 
            "University ID must be exactly 10 digits!"
        )
        return []
    
    records = get_attendance_by_student(university_id)
    
    if records is None:
        return []
    
    if not records:
        messagebox.showinfo("No Records", f"No attendance records for {university_id}!")
        return []
    
    return records


def get_all_attendance_records():
    """
    Retrieve ALL attendance records from database.
    
    RETURNS:
    - List of all attendance: [(id, date, status), ...]
    - None if database error
    
    EXAMPLE:
    all_records = get_all_attendance_records()
    if all_records:
        for record in all_records:
            print(record)
    """
    return get_all_attendance()


def calculate_attendance_percentage(university_id):
    """
    Calculate attendance percentage for a student.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    
    RETURNS:
    - Dictionary with stats:
      {
        'total': 10,
        'present': 8,
        'absent': 2,
        'percentage': 80.0
      }
    - None if no records found
    
    EXAMPLE:
    stats = calculate_attendance_percentage("1234567890")
    print(f"Attendance: {stats['percentage']}%")
    """
    
    records = get_student_attendance(university_id)
    
    if not records:
        return None
    
    total = len(records)
    present = sum(1 for record in records if record[1] == 'Present')
    absent = total - present
    percentage = (present / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'present': present,
        'absent': absent,
        'percentage': round(percentage, 2)
    }
