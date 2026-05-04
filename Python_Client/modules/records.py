"""
Records Module for SMAS Application
Handles updating and deleting student and attendance records.

WHAT IT DOES:
- Update student information (Full Name, Major)
- Delete students from system
- Delete attendance records
- Retrieve record details for editing

WHY SEPARATE:
- Business logic (validation, operations) is separate from database layer
- Can test validation without database
- Can change validation rules easily
"""

from tkinter import messagebox
from core.database import (
    get_all_students,
    get_attendance_by_student,
    get_attendance_by_student_with_id,
    update_student,
    delete_student,
    delete_attendance_record,
    update_attendance_status
)


# ===== STUDENT UPDATE FUNCTIONS =====

def get_student_details(university_id):
    """
    Retrieve student information by ID.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    
    RETURNS:
    - Tuple (university_id, full_name, major) if found
    - None if not found
    
    EXAMPLE:
    student = get_student_details("1234567890")
    if student:
        print(f"Name: {student[1]}")
    """
    if not university_id:
        messagebox.showerror("Error", "Please enter a student ID")
        return None
    
    try:
        students = get_all_students()
        if not students:
            messagebox.showerror("Error", "No students found")
            return None
        
        for student in students:
            if str(student[0]) == university_id:
                return student
        
        messagebox.showerror("Not Found", f"Student {university_id} not found")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve student: {str(e)}")
        return None


def update_student_info(university_id, new_name, new_major):
    """
    Update student's name and major.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    - new_name: New full name (minimum 3 characters)
    - new_major: New major (minimum 2 characters)
    
    RETURNS:
    - True if successful
    - False if validation fails
    
    VALIDATION:
    - Student ID must be 10 digits
    - Name must be at least 3 characters
    - Major must be at least 2 characters
    - Student must exist in database
    
    EXAMPLE:
    if update_student_info("1234567890", "Ahmad Ali", "Computer Science"):
        print("Updated successfully")
    """
    # Validation 1: Check if fields are empty
    if not university_id or not new_name or not new_major:
        messagebox.showerror("Validation Error", "All fields are required")
        return False
    
    # Validation 2: Check ID format (10 digits)
    if not university_id.isdigit() or len(university_id) != 10:
        messagebox.showerror("Validation Error", "Student ID must be exactly 10 digits")
        return False
    
    # Validation 3: Check name length (minimum 3 characters)
    if len(new_name.strip()) < 3:
        messagebox.showerror("Validation Error", "Name must be at least 3 characters")
        return False
    
    # Validation 4: Check major length (minimum 2 characters)
    if len(new_major.strip()) < 2:
        messagebox.showerror("Validation Error", "Major must be at least 2 characters")
        return False
    
    # Validation 5: Check if student exists
    student = get_student_details(university_id)
    if not student:
        # get_student_details already shows error message
        return False
    
    # Try to update in database
    success = update_student(university_id, new_name, new_major)
    if success:
        messagebox.showinfo("Success", f"Student {university_id} updated successfully!")
    
    return success


def delete_student_record(university_id):
    """
    Delete a student from the system (and all their attendance records).
    
    PARAMETERS:
    - university_id: Student's 10-digit ID to delete
    
    RETURNS:
    - True if successful
    - False if validation fails or student not found
    
    VALIDATION:
    - Student ID must be 10 digits
    - Student must exist
    - Shows confirmation dialog before deleting
    
    EXAMPLE:
    if delete_student_record("1234567890"):
        print("Student deleted")
    """
    # Validation 1: Check if ID is empty
    if not university_id:
        messagebox.showerror("Error", "Please enter a student ID")
        return False
    
    # Validation 2: Check ID format (10 digits)
    if not university_id.isdigit() or len(university_id) != 10:
        messagebox.showerror("Validation Error", "Student ID must be exactly 10 digits")
        return False
    
    # Validation 3: Check if student exists
    student = get_student_details(university_id)
    if not student:
        # get_student_details already shows error message
        return False
    
    # Show confirmation dialog
    student_name = student[1]
    response = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete:\n\nID: {university_id}\nName: {student_name}\n\nThis will also delete all attendance records!"
    )
    
    if not response:
        return False
    
    # Delete from database
    success = delete_student(university_id)
    if success:
        messagebox.showinfo("Success", f"Student {university_id} deleted successfully!")
    
    return success


# ===== ATTENDANCE UPDATE FUNCTIONS =====

def get_attendance_record_details(university_id):
    """
    Retrieve attendance records for a student.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    
    RETURNS:
    - List of (date, status) tuples if records exist
    - Empty list if no records found
    
    EXAMPLE:
    records = get_attendance_record_details("1234567890")
    for date, status in records:
        print(f"{date}: {status}")
    """
    if not university_id:
        messagebox.showerror("Error", "Please enter a student ID")
        return []
    
    # Validation: Check ID format
    if not university_id.isdigit() or len(university_id) != 10:
        messagebox.showerror("Validation Error", "Student ID must be exactly 10 digits")
        return []
    
    # Try to retrieve from database
    records = get_attendance_by_student(university_id)
    if records is None:
        return []
    
    if not records:
        messagebox.showinfo("Info", f"No attendance records found for {university_id}")
    
    return records if records else []


def delete_attendance_entry(attendance_id):
    """
    Delete a specific attendance record by ID.
    
    PARAMETERS:
    - attendance_id: The Attendance_ID to delete
    
    RETURNS:
    - True if successful
    - False if failed
    
    EXAMPLE:
    if delete_attendance_entry(5):
        print("Record deleted")
    """
    if not attendance_id:
        messagebox.showerror("Error", "Please select an attendance record")
        return False
    
    # Show confirmation
    response = messagebox.askyesno(
        "Confirm Delete",
        f"Delete attendance record #{attendance_id}?\n\nThis action cannot be undone."
    )
    
    if not response:
        return False
    
    # Delete from database
    success = delete_attendance_record(attendance_id)
    if success:
        messagebox.showinfo("Success", "Attendance record deleted successfully!")
    
    return success


def update_attendance_entry(university_id):
    """
    Get attendance records for a student to update.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    
    RETURNS:
    - List of (Attendance_ID, date, status) tuples
    - Empty list if no records found
    
    EXAMPLE:
    records = update_attendance_entry("1234567890")
    """
    if not university_id:
        messagebox.showerror("Error", "Please enter a student ID")
        return []
    
    # Validation: Check ID format
    if not university_id.isdigit() or len(university_id) != 10:
        messagebox.showerror("Validation Error", "Student ID must be exactly 10 digits")
        return []
    
    # Try to retrieve from database
    records = get_attendance_by_student_with_id(university_id)
    if records is None:
        return []
    
    if not records:
        messagebox.showinfo("Info", f"No attendance records found for {university_id}")
    
    return records if records else []


def apply_attendance_update(attendance_id, new_status):
    """
    Update attendance record status.
    
    PARAMETERS:
    - attendance_id: The Attendance_ID to update
    - new_status: New status 'Present' or 'Absent'
    
    RETURNS:
    - True if successful
    - False if failed
    
    EXAMPLE:
    if apply_attendance_update(5, "Absent"):
        print("Updated successfully")
    """
    if not attendance_id:
        messagebox.showerror("Error", "Please select an attendance record")
        return False
    
    if new_status not in ["Present", "Absent"]:
        messagebox.showerror("Error", "Status must be 'Present' or 'Absent'")
        return False
    
    # Update in database
    success = update_attendance_status(attendance_id, new_status)
    if success:
        messagebox.showinfo("Success", f"Record updated to {new_status}!")
    
    return success


def search_students_by_criteria(search_term):
    """
    Search for students by ID or name.
    
    PARAMETERS:
    - search_term: Part of ID or name to search for
    
    RETURNS:
    - List of matching students: [(id, name, major), ...]
    - Empty list if no matches
    
    EXAMPLE:
    results = search_students_by_criteria("Ahmed")
    for student_id, name, major in results:
        print(f"{student_id}: {name}")
    """
    if not search_term:
        messagebox.showerror("Error", "Please enter search term")
        return []
    
    try:
        all_students = get_all_students()
        if not all_students:
            return []
        
        # Search by ID or name (case-insensitive)
        search_lower = search_term.lower()
        results = [
            student for student in all_students
            if search_lower in str(student[0]) or search_lower in student[1].lower()
        ]
        
        return results
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {str(e)}")
        return []
