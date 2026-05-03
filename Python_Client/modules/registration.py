"""
FEATURE 1: Student Registration Module
This module handles ALL registration-related business logic.

WHAT THIS DOES:
- Validates student input (checks if fields are empty, ID is valid, etc.)
- Calls database functions to save students
- Shows success/error messages to user

WHY SEPARATE:
- Registration logic is different from other features
- Can be tested independently
- Easy to update or fix registration without touching other features
"""

from tkinter import messagebox
from core.database import insert_student, get_all_students


def register_student(university_id, full_name, major):
    """
    Register a new student in the system.
    
    PARAMETERS:
    - university_id: 10-digit ID (string)
    - full_name: Student's full name
    - major: Student's major/field
    
    RETURNS:
    - True if registration successful
    - False if validation failed or database error
    
    VALIDATION CHECKS:
    1. All fields must be filled (not empty)
    2. University ID must be exactly 10 digits
    3. Name should not be too short
    
    EXAMPLE:
    if register_student("1234567890", "Ahmed Ali", "CS"):
        print("Student registered!")
    else:
        print("Registration failed!")
    """
    
    # ===== VALIDATION CHECKS =====
    
    # Check 1: All fields filled?
    if not university_id or not full_name or not major:
        messagebox.showwarning("Validation Error", "All fields are required!")
        return False
    
    # Check 2: University ID is 10 digits?
    if len(university_id) != 10 or not university_id.isdigit():
        messagebox.showwarning(
            "Validation Error", 
            "University ID must be exactly 10 digits!"
        )
        return False
    
    # Check 3: Name is not too short?
    if len(full_name) < 3:
        messagebox.showwarning(
            "Validation Error", 
            "Student name must be at least 3 characters!"
        )
        return False
    
    # Check 4: Major is not too short?
    if len(major) < 2:
        messagebox.showwarning(
            "Validation Error", 
            "Major must be at least 2 characters!"
        )
        return False
    
    # ===== IF ALL VALIDATION PASSED =====
    # Call database function to insert student
    success = insert_student(university_id, full_name, major)
    return success


def search_student(search_term):
    """
    Search for a student by ID or name.
    
    PARAMETERS:
    - search_term: What to search for (ID or name)
    
    RETURNS:
    - List of matching students: [(id, name, major), ...]
    - Empty list if no matches
    
    EXAMPLE:
    results = search_student("Ahmed")
    for student in results:
        print(student)
    """
    
    if not search_term:
        messagebox.showwarning("Error", "Enter a search term!")
        return []
    
    # Get all students
    all_students = get_all_students()
    
    if not all_students:
        messagebox.showwarning("Warning", "No students found in database!")
        return []
    
    # Search by ID or name (convert search term to lowercase for comparison)
    search_lower = search_term.lower()
    results = []
    
    for student in all_students:
        student_id = str(student[0])  # ID
        student_name = student[1].lower()  # Name
        
        # Check if search term matches ID or name
        if search_lower in student_id or search_lower in student_name:
            results.append(student)
    
    if not results:
        messagebox.showinfo("Search Results", "No students match your search!")
    
    return results


def view_all_students():
    """
    Retrieve all students from database.
    
    RETURNS:
    - List of all students: [(id, name, major), ...]
    - None if database error
    
    EXAMPLE:
    students = view_all_students()
    if students:
        for s in students:
            print(f"{s[0]}: {s[1]} ({s[2]})")
    """
    return get_all_students()
