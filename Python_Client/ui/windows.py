"""
GUI Windows for SMAS Application
This file contains all the visual windows and forms the user sees.

WHY SEPARATE:
- GUI code is separate from business logic
- Can change how things look without breaking features
- Easy to switch from Tkinter to PyQt5 later if needed

STRUCTURE:
- MainWindow = Single window that changes content (not multiple windows)
- Pages: Menu, Registration, Attendance, Records, Reporting
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, FONT_TITLE, FONT_NORMAL, FONT_BUTTON
from modules.registration import register_student, view_all_students
from modules.attendance import log_attendance, get_student_attendance, calculate_attendance_percentage


def center_window(window, width, height):
    """
    Center a window on the screen.
    
    PARAMETERS:
    - window: Tkinter window object
    - width: Window width
    - height: Window height
    """
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate center position
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set window position and size
    window.geometry(f"{width}x{height}+{x}+{y}")


class MainWindow:
    """
    Single Window Application - Content changes based on user selection.
    
    HOW IT WORKS:
    1. User sees main menu with 4 buttons
    2. User clicks a button (e.g., "Register Student")
    3. Same window clears and shows registration form
    4. User can click "Back to Menu" to return to main menu
    
    WHY SINGLE WINDOW:
    - Better UX (no window clutter)
    - Easier navigation
    - Cleaner code
    """
    
    def __init__(self, root):
        """
        Initialize main window.
        
        PARAMETERS:
        - root: The main Tkinter window object
        """
        self.root = root
        self.root.title(APP_TITLE)
        
        # Center window on screen
        center_window(self.root, APP_WIDTH, APP_HEIGHT)
        
        self.root.resizable(False, False)
        
        # Variables to store input (for registration form)
        self.var_id = tk.StringVar()
        self.var_name = tk.StringVar()
        self.var_major = tk.StringVar()
        
        # Variables to store input (for attendance form)
        self.var_att_id = tk.StringVar()
        self.var_att_date = tk.StringVar()
        self.var_att_status = tk.StringVar(value="Present")  # Default to Present
        
        # Show main menu
        self.show_menu()
    
    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_menu(self):
        """Show the main menu."""
        self.clear_window()
        
        # ===== HEADER =====
        header_frame = ttk.Frame(self.root)
        header_frame.pack(pady=20)
        
        header_label = ttk.Label(
            header_frame,
            text="SMAS Control Panel",
            font=FONT_TITLE
        )
        header_label.pack()
        
        subtitle = ttk.Label(
            header_frame,
            text="Select an operation below",
            font=FONT_NORMAL
        )
        subtitle.pack()
        
        # ===== BUTTON FRAME =====
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Feature 1: Student Registration
        btn_register = ttk.Button(
            button_frame,
            text="1. Student Registration",
            command=self.show_registration,
            width=40
        )
        btn_register.pack(pady=10, fill="x")
        
        # Feature 2: Attendance Logging
        btn_attendance = ttk.Button(
            button_frame,
            text="2. Attendance Logging",
            command=self.show_attendance,
            width=40
        )
        btn_attendance.pack(pady=10, fill="x")
        
        # Feature 3: Record Modification
        btn_records = ttk.Button(
            button_frame,
            text="3. Record Modification",
            command=self.show_records,
            width=40
        )
        btn_records.pack(pady=10, fill="x")
        
        # Feature 4: Reports & Search
        btn_reports = ttk.Button(
            button_frame,
            text="4. Reports & Search",
            command=self.show_reports,
            width=40
        )
        btn_reports.pack(pady=10, fill="x")
        
        # ===== FOOTER =====
        footer = ttk.Label(
            self.root,
            text="Connected to MySQL Database",
            font=("Arial", 8),
            foreground="gray"
        )
        footer.pack(side="bottom", pady=5)
    
    def show_registration(self):
        """Show the student registration form."""
        self.clear_window()
        
        # ===== HEADER =====
        header = ttk.Label(
            self.root,
            text="Student Registration Form",
            font=FONT_TITLE
        )
        header.pack(pady=15)
        
        # ===== FORM FRAME =====
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # ===== FIELD 1: University ID =====
        label_id = ttk.Label(form_frame, text="University ID (10 digits):", font=FONT_NORMAL)
        label_id.pack(anchor="w", pady=(10, 5))
        
        entry_id = ttk.Entry(form_frame, textvariable=self.var_id, width=40, font=FONT_NORMAL)
        entry_id.pack(anchor="w", pady=(0, 10))
        
        # ===== FIELD 2: Full Name =====
        label_name = ttk.Label(form_frame, text="Full Name:", font=FONT_NORMAL)
        label_name.pack(anchor="w", pady=(10, 5))
        
        entry_name = ttk.Entry(form_frame, textvariable=self.var_name, width=40, font=FONT_NORMAL)
        entry_name.pack(anchor="w", pady=(0, 10))
        
        # ===== FIELD 3: Academic Major =====
        label_major = ttk.Label(form_frame, text="Academic Major:", font=FONT_NORMAL)
        label_major.pack(anchor="w", pady=(10, 5))
        
        entry_major = ttk.Entry(form_frame, textvariable=self.var_major, width=40, font=FONT_NORMAL)
        entry_major.pack(anchor="w", pady=(0, 10))
        
        # ===== BUTTON FRAME =====
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15, padx=20, fill="x")
        
        # Register Button
        btn_register = ttk.Button(
            button_frame,
            text="Register",
            command=self.register_student_action
        )
        btn_register.pack(side="left", padx=5, fill="x", expand=True)
        
        # View All Button
        btn_view = ttk.Button(
            button_frame,
            text="View All",
            command=self.view_all_students_action
        )
        btn_view.pack(side="left", padx=5, fill="x", expand=True)
        
        # Clear Button
        btn_clear = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_registration_form
        )
        btn_clear.pack(side="left", padx=5, fill="x", expand=True)
        
        # Back Button
        btn_back = ttk.Button(
            button_frame,
            text="Back",
            command=self.show_menu
        )
        btn_back.pack(side="left", padx=5, fill="x", expand=True)
    
    def show_attendance(self):
        """Show the attendance logging form."""
        self.clear_window()
        
        # ===== HEADER =====
        header = ttk.Label(
            self.root,
            text="Attendance Logging",
            font=FONT_TITLE
        )
        header.pack(pady=15)
        
        # ===== FORM FRAME =====
        form_frame = ttk.Frame(self.root)
        form_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # ===== FIELD 1: University ID =====
        label_id = ttk.Label(form_frame, text="University ID (10 digits):", font=FONT_NORMAL)
        label_id.pack(anchor="w", pady=(10, 5))
        
        entry_att_id = ttk.Entry(form_frame, textvariable=self.var_att_id, width=40, font=FONT_NORMAL)
        entry_att_id.pack(anchor="w", pady=(0, 10))
        
        # ===== FIELD 2: Date =====
        label_date = ttk.Label(form_frame, text="Date (YYYY-MM-DD):", font=FONT_NORMAL)
        label_date.pack(anchor="w", pady=(10, 5))
        
        entry_att_date = ttk.Entry(form_frame, textvariable=self.var_att_date, width=40, font=FONT_NORMAL)
        entry_att_date.pack(anchor="w", pady=(0, 10))
        # Set default to today's date in correct format
        self.var_att_date.set(date.today().strftime('%Y-%m-%d'))
        
        # ===== FIELD 3: Status (Radio Buttons) =====
        label_status = ttk.Label(form_frame, text="Status:", font=FONT_NORMAL)
        label_status.pack(anchor="w", pady=(10, 5))
        
        status_frame = ttk.Frame(form_frame)
        status_frame.pack(anchor="w", pady=(0, 10))
        
        radio_present = ttk.Radiobutton(
            status_frame,
            text="Present",
            variable=self.var_att_status,
            value="Present"
        )
        radio_present.pack(side="left", padx=10)
        
        radio_absent = ttk.Radiobutton(
            status_frame,
            text="Absent",
            variable=self.var_att_status,
            value="Absent"
        )
        radio_absent.pack(side="left", padx=10)
        
        # ===== BUTTON FRAME =====
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=15, padx=20, fill="x")
        
        # Log Attendance Button
        btn_log = ttk.Button(
            button_frame,
            text="Log",
            command=self.log_attendance_action
        )
        btn_log.pack(side="left", padx=5, fill="x", expand=True)
        
        # View Attendance Button
        btn_view = ttk.Button(
            button_frame,
            text="View",
            command=self.view_attendance_action
        )
        btn_view.pack(side="left", padx=5, fill="x", expand=True)
        
        # Stats Button
        btn_stats = ttk.Button(
            button_frame,
            text="Stats",
            command=self.view_attendance_stats_action
        )
        btn_stats.pack(side="left", padx=5, fill="x", expand=True)
        
        # Clear Button
        btn_clear = ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_attendance_form
        )
        btn_clear.pack(side="left", padx=5, fill="x", expand=True)
        
        # ===== BACK BUTTON FRAME (Bottom) =====
        back_frame = ttk.Frame(self.root)
        back_frame.pack(pady=10, padx=20, fill="x")
        
        btn_back = ttk.Button(
            back_frame,
            text="Back to Menu",
            command=self.show_menu
        )
        btn_back.pack(fill="x", expand=True)
    
    def log_attendance_action(self):
        """Handle log attendance button click."""
        university_id = self.var_att_id.get()
        date = self.var_att_date.get()
        status = self.var_att_status.get()
        
        # Call attendance module
        success = log_attendance(university_id, date, status)
        
        if success:
            self.clear_attendance_form()
    
    def view_attendance_action(self):
        """Show attendance records for a student."""
        university_id = self.var_att_id.get()
        
        if not university_id:
            messagebox.showwarning("Error", "Enter University ID!")
            return
        
        records = get_student_attendance(university_id)
        
        if not records:
            messagebox.showwarning("No Records", "No attendance records found!")
            return
        
        # Create popup window to show results
        results_window = tk.Toplevel(self.root)
        results_window.title(f"Attendance for {university_id}")
        results_window.geometry("600x400")
        center_window(results_window, 600, 400)
        
        # Create text widget
        text_widget = tk.Text(results_window, font=("Courier", 10), state="normal")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add header
        text_widget.insert("end", "DATE\t\t\tSTATUS\n")
        text_widget.insert("end", "=" * 50 + "\n")
        
        # Add records
        for record in records:
            date, status = record
            text_widget.insert("end", f"{date}\t\t{status}\n")
        
        text_widget.config(state="disabled")
    
    def view_attendance_stats_action(self):
        """Show attendance statistics for a student."""
        university_id = self.var_att_id.get()
        
        if not university_id:
            messagebox.showwarning("Error", "Enter University ID!")
            return
        
        stats = calculate_attendance_percentage(university_id)
        
        if not stats:
            messagebox.showwarning("No Data", "No attendance records to calculate!")
            return
        
        # Create popup with stats
        messagebox.showinfo(
            "Attendance Statistics",
            f"""Student ID: {university_id}

Total Classes: {stats['total']}
Present: {stats['present']}
Absent: {stats['absent']}

Attendance: {stats['percentage']}%"""
        )
    
    def clear_attendance_form(self):
        """Clear all attendance form fields."""
        self.var_att_id.set("")
        self.var_att_date.set("")
        self.var_att_status.set("Present")
    
    def show_records(self):
        """Show the record modification form."""
        self.clear_window()
        
        header = ttk.Label(
            self.root,
            text="Record Modification",
            font=FONT_TITLE
        )
        header.pack(pady=20)
        
        message = ttk.Label(
            self.root,
            text="Feature 3: Record Modification\n(Coming Soon - Will be implemented next)",
            font=FONT_NORMAL,
            justify="center"
        )
        message.pack(pady=50)
        
        # Back Button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        btn_back = ttk.Button(
            button_frame,
            text="Back to Menu",
            command=self.show_menu,
            width=30
        )
        btn_back.pack()
    
    def show_reports(self):
        """Show the reports and search form."""
        self.clear_window()
        
        header = ttk.Label(
            self.root,
            text="Reports & Search",
            font=FONT_TITLE
        )
        header.pack(pady=20)
        
        message = ttk.Label(
            self.root,
            text="Feature 4: Reports & Search\n(Coming Soon - Will be implemented next)",
            font=FONT_NORMAL,
            justify="center"
        )
        message.pack(pady=50)
        
        # Back Button
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=20)
        
        btn_back = ttk.Button(
            button_frame,
            text="Back to Menu",
            command=self.show_menu,
            width=30
        )
        btn_back.pack()
    
    def register_student_action(self):
        """
        Handle registration button click.
        Calls the registration module to validate and save student.
        """
        # Get values from form fields
        university_id = self.var_id.get()
        full_name = self.var_name.get()
        major = self.var_major.get()
        
        # Call registration module (this does validation)
        success = register_student(university_id, full_name, major)
        
        # If successful, clear the form
        if success:
            self.clear_registration_form()
    
    def view_all_students_action(self):
        """
        Show all registered students in a popup window.
        """
        students = view_all_students()
        
        if not students:
            messagebox.showwarning("No Students", "No students registered yet!")
            return
        
        # Create popup window to show results
        results_window = tk.Toplevel(self.root)
        results_window.title("All Students")
        results_window.geometry("600x400")
        
        # Center this popup window too
        center_window(results_window, 600, 400)
        
        # Create text widget to display results
        text_widget = tk.Text(results_window, font=("Courier", 10), state="normal")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add header
        text_widget.insert("end", "ID\t\t\tNAME\t\t\tMAJOR\n")
        text_widget.insert("end", "=" * 80 + "\n")
        
        # Add student data
        for student in students:
            student_id = str(student[0])
            name = student[1]
            major_field = student[2]
            text_widget.insert("end", f"{student_id}\t\t{name}\t\t{major_field}\n")
        
        text_widget.config(state="disabled")  # Make read-only
    
    def clear_registration_form(self):
        """Clear all form fields."""
        self.var_id.set("")
        self.var_name.set("")
        self.var_major.set("")

