"""
Reporting Module for SMAS Application
Generates reports and statistics from student and attendance data.

WHAT IT DOES:
- Generate attendance reports for individual students
- Generate overall class attendance statistics
- Search and filter students
- Calculate attendance percentages and statistics
- Generate reports by date range

WHY SEPARATE:
- Report logic is separate from database and UI
- Can change report formats easily
- Can test report calculations without database
"""

from tkinter import messagebox
from core.database import get_all_students, get_all_attendance, get_attendance_by_student
from datetime import datetime, date


# ===== ATTENDANCE REPORT FUNCTIONS =====

def generate_student_attendance_report(university_id):
    """
    Generate comprehensive attendance report for a student.
    
    PARAMETERS:
    - university_id: Student's 10-digit ID
    
    RETURNS:
    - Dictionary with student info and attendance stats
    - None if student not found
    
    EXAMPLE:
    report = generate_student_attendance_report("1234567890")
    if report:
        print(f"Name: {report['name']}")
        print(f"Attendance %: {report['percentage']}%")
    """
    # Validation: Check ID format
    if not university_id:
        messagebox.showerror("Error", "Please enter a student ID")
        return None
    
    if not university_id.isdigit() or len(university_id) != 10:
        messagebox.showerror("Validation Error", "Student ID must be exactly 10 digits")
        return None
    
    try:
        # Get student info
        all_students = get_all_students()
        if not all_students:
            messagebox.showerror("Error", "No students found")
            return None
        
        student_info = None
        for student in all_students:
            if str(student[0]) == university_id:
                student_info = student
                break
        
        if not student_info:
            messagebox.showerror("Not Found", f"Student {university_id} not found")
            return None
        
        # Get attendance records
        records = get_attendance_by_student(university_id)
        if records is None:
            return None
        
        # Calculate statistics
        total = len(records)
        present = sum(1 for _, status in records if status == "Present")
        absent = total - present
        percentage = (present / total * 100) if total > 0 else 0
        
        # Build report dictionary
        report = {
            'student_id': university_id,
            'name': student_info[1],
            'major': student_info[2],
            'total': total,
            'present': present,
            'absent': absent,
            'percentage': round(percentage, 2),
            'records': records
        }
        
        return report
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate report: {str(e)}")
        return None


def generate_class_attendance_report():
    """
    Generate overall class attendance statistics.
    
    RETURNS:
    - Dictionary with class statistics
    - None if failed
    
    EXAMPLE:
    class_report = generate_class_attendance_report()
    if class_report:
        print(f"Total Students: {class_report['total_students']}")
        print(f"Average Attendance: {class_report['avg_percentage']}%")
    """
    try:
        # Get all students
        students = get_all_students()
        if not students:
            messagebox.showerror("Error", "No students found")
            return None
        
        # Get all attendance records
        all_records = get_all_attendance()
        if all_records is None:
            return None
        
        # Calculate overall statistics
        total_records = len(all_records)
        present_count = sum(1 for _, _, status in all_records if status == "Present")
        absent_count = total_records - present_count
        overall_percentage = (present_count / total_records * 100) if total_records > 0 else 0
        
        # Per-student statistics
        student_stats = {}
        for student in students:
            student_id = str(student[0])
            student_records = get_attendance_by_student(student_id)
            
            if student_records:
                student_total = len(student_records)
                student_present = sum(1 for _, status in student_records if status == "Present")
                student_percentage = (student_present / student_total * 100) if student_total > 0 else 0
                
                student_stats[student_id] = {
                    'name': student[1],
                    'total': student_total,
                    'present': student_present,
                    'absent': student_total - student_present,
                    'percentage': round(student_percentage, 2)
                }
        
        # Build report
        report = {
            'total_students': len(students),
            'total_records': total_records,
            'present_count': present_count,
            'absent_count': absent_count,
            'overall_percentage': round(overall_percentage, 2),
            'student_stats': student_stats
        }
        
        return report
    except Exception as e:
        messagebox.showerror("Error", f"Could not generate class report: {str(e)}")
        return None


def search_students_by_attendance(min_percentage=None, max_percentage=None):
    """
    Search students by attendance percentage range.
    
    PARAMETERS:
    - min_percentage: Minimum attendance % (0-100)
    - max_percentage: Maximum attendance % (0-100)
    
    RETURNS:
    - List of students matching criteria
    - Empty list if none found
    
    EXAMPLE:
    # Get all students with >= 80% attendance
    good_attendance = search_students_by_attendance(min_percentage=80)
    """
    try:
        all_students = get_all_students()
        if not all_students:
            return []
        
        matching_students = []
        
        for student in all_students:
            student_id = str(student[0])
            records = get_attendance_by_student(student_id)
            
            if records:
                total = len(records)
                present = sum(1 for _, status in records if status == "Present")
                percentage = (present / total * 100) if total > 0 else 0
                
                # Check if matches criteria
                if min_percentage is not None and percentage < min_percentage:
                    continue
                if max_percentage is not None and percentage > max_percentage:
                    continue
                
                matching_students.append({
                    'id': student_id,
                    'name': student[1],
                    'major': student[2],
                    'percentage': round(percentage, 2)
                })
        
        return matching_students
    except Exception as e:
        messagebox.showerror("Error", f"Search failed: {str(e)}")
        return []


def get_high_absentees(threshold=20):
    """
    Get students with absence count above threshold.
    
    PARAMETERS:
    - threshold: Minimum number of absences (default 20)
    
    RETURNS:
    - List of students with high absenteeism
    - Empty list if none found
    
    EXAMPLE:
    concern_list = get_high_absentees(threshold=5)
    """
    try:
        all_students = get_all_students()
        if not all_students:
            return []
        
        high_absentees = []
        
        for student in all_students:
            student_id = str(student[0])
            records = get_attendance_by_student(student_id)
            
            if records:
                absent_count = sum(1 for _, status in records if status == "Absent")
                
                if absent_count >= threshold:
                    high_absentees.append({
                        'id': student_id,
                        'name': student[1],
                        'absences': absent_count,
                        'total': len(records)
                    })
        
        # Sort by absences (highest first)
        high_absentees.sort(key=lambda x: x['absences'], reverse=True)
        return high_absentees
    except Exception as e:
        messagebox.showerror("Error", f"Could not get absentee list: {str(e)}")
        return []


def get_attendance_by_date(target_date):
    """
    Get all attendance records for a specific date.
    
    PARAMETERS:
    - target_date: Date string in format 'YYYY-MM-DD'
    
    RETURNS:
    - List of (student_id, status) for that date
    - Empty list if no records found
    
    EXAMPLE:
    records = get_attendance_by_date("2026-05-04")
    """
    try:
        all_records = get_all_attendance()
        if not all_records:
            return []
        
        date_records = [
            (student_id, status) for student_id, rec_date, status in all_records
            if str(rec_date) == target_date
        ]
        
        return date_records
    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve records: {str(e)}")
        return []


def format_attendance_report(report):
    """
    Format attendance report for display.
    
    PARAMETERS:
    - report: Report dictionary from generate_student_attendance_report()
    
    RETURNS:
    - Formatted string for display
    
    EXAMPLE:
    report = generate_student_attendance_report("1234567890")
    display_text = format_attendance_report(report)
    print(display_text)
    """
    if not report:
        return "No report available"
    
    text = f"""
STUDENT ATTENDANCE REPORT
{'='*50}

Student ID: {report['student_id']}
Name: {report['name']}
Major: {report['major']}

STATISTICS:
  Total Records: {report['total']}
  Present: {report['present']}
  Absent: {report['absent']}
  Attendance: {report['percentage']}%

ATTENDANCE HISTORY:
"""
    
    if report['records']:
        for i, (date, status) in enumerate(report['records'], 1):
            text += f"  {i}. {date} - {status}\n"
    else:
        text += "  No records found\n"
    
    return text
