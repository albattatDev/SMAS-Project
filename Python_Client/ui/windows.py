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
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime, date
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, FONT_TITLE, FONT_NORMAL, FONT_BUTTON
from modules.registration import register_student, view_all_students
from modules.attendance import log_attendance, get_student_attendance, calculate_attendance_percentage
from modules.records import (
    update_student_info, delete_student_record, 
    get_student_details, get_attendance_record_details,
    delete_attendance_entry, search_students_by_criteria,
    update_attendance_entry, apply_attendance_update
)
from modules.reporting import (
    generate_student_attendance_report, generate_class_attendance_report,
    search_students_by_attendance, get_high_absentees, format_attendance_report
)


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
        
        # Variables to store input (for records form)
        self.var_rec_id = tk.StringVar()
        self.var_rec_name = tk.StringVar()
        self.var_rec_major = tk.StringVar()
        self.var_rec_operation = tk.StringVar(value="update")  # Default to update
        
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
        
        # ===== HEADER =====
        header = ttk.Label(
            self.root,
            text="Record Management",
            font=FONT_TITLE
        )
        header.pack(pady=10)
        
        # ===== MAIN CONTAINER FRAME =====
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # ===== SEARCH FRAME =====
        search_frame = ttk.LabelFrame(main_frame, text="Search Student", padding=10)
        search_frame.pack(pady=10, fill="x")
        
        search_label = ttk.Label(search_frame, text="Search by ID or Name:", font=FONT_NORMAL)
        search_label.pack(anchor="w", pady=(0, 5))
        
        search_entry = ttk.Entry(search_frame, width=40, font=FONT_NORMAL)
        search_entry.pack(anchor="w", pady=(0, 10), fill="x")
        
        btn_search = ttk.Button(
            search_frame,
            text="Search",
            command=lambda: self.search_student_action(search_entry.get())
        )
        btn_search.pack(fill="x")
        
        # ===== STUDENT INFO FRAME =====
        info_frame = ttk.LabelFrame(main_frame, text="Student Information", padding=10)
        info_frame.pack(pady=10, fill="x")
        
        # ID (Read-only display)
        label_id = ttk.Label(info_frame, text="University ID:", font=FONT_NORMAL)
        label_id.pack(anchor="w", pady=(10, 2))
        
        entry_id = ttk.Entry(info_frame, textvariable=self.var_rec_id, width=40, font=FONT_NORMAL, state="readonly")
        entry_id.pack(anchor="w", pady=(0, 10), fill="x")
        
        # Name (Editable)
        label_name = ttk.Label(info_frame, text="Full Name:", font=FONT_NORMAL)
        label_name.pack(anchor="w", pady=(10, 2))
        
        entry_name = ttk.Entry(info_frame, textvariable=self.var_rec_name, width=40, font=FONT_NORMAL)
        entry_name.pack(anchor="w", pady=(0, 10), fill="x")
        
        # Major (Editable)
        label_major = ttk.Label(info_frame, text="Major:", font=FONT_NORMAL)
        label_major.pack(anchor="w", pady=(10, 2))
        
        entry_major = ttk.Entry(info_frame, textvariable=self.var_rec_major, width=40, font=FONT_NORMAL)
        entry_major.pack(anchor="w", pady=(0, 10), fill="x")
        
        # ===== BUTTON FRAME =====
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15, fill="x")
        
        # Update Button
        btn_update = ttk.Button(
            button_frame,
            text="Update",
            command=self.update_student_action
        )
        btn_update.pack(side="left", padx=5, fill="x", expand=True)
        
        # View Attendance Button
        btn_view_att = ttk.Button(
            button_frame,
            text="View Attendance",
            command=self.view_student_attendance_action
        )
        btn_view_att.pack(side="left", padx=5, fill="x", expand=True)
        
        # Delete Attendance Button
        btn_del_att = ttk.Button(
            button_frame,
            text="Edit Attendance",
            command=self.edit_attendance_action
        )
        btn_del_att.pack(side="left", padx=5, fill="x", expand=True)
        
        # Delete Student Button
        btn_delete = ttk.Button(
            button_frame,
            text="Delete Student",
            command=self.delete_student_action
        )
        btn_delete.pack(side="left", padx=5, fill="x", expand=True)
        
        # ===== BACK BUTTON FRAME =====
        back_frame = ttk.Frame(self.root)
        back_frame.pack(pady=10, padx=20, fill="x")
        
        btn_back = ttk.Button(
            back_frame,
            text="Back to Menu",
            command=self.show_menu
        )
        btn_back.pack(fill="x", expand=True)
    
    def search_student_action(self, search_term):
        """Search for student by ID or name."""
        if not search_term:
            messagebox.showerror("Error", "Please enter search term")
            return
        
        results = search_students_by_criteria(search_term)
        if not results:
            messagebox.showinfo("Not Found", f"No students found matching '{search_term}'")
            return
        
        if len(results) == 1:
            # Single result - auto-fill form
            student = results[0]
            self.var_rec_id.set(student[0])
            self.var_rec_name.set(student[1])
            self.var_rec_major.set(student[2])
        else:
            # Multiple results - show list for user to select
            result_text = "Found multiple students:\n\n"
            for i, student in enumerate(results):
                result_text += f"{i+1}. {student[0]} - {student[1]}\n"
            result_text += "\nClick on a student ID above to select"
            messagebox.showinfo("Search Results", result_text)
    
    def update_student_action(self):
        """Handle update student button click."""
        student_id = self.var_rec_id.get()
        new_name = self.var_rec_name.get()
        new_major = self.var_rec_major.get()
        
        if update_student_info(student_id, new_name, new_major):
            messagebox.showinfo("Success", "Student updated successfully!")
    
    def delete_student_action(self):
        """Handle delete student button click."""
        student_id = self.var_rec_id.get()
        
        if delete_student_record(student_id):
            # Clear form after successful delete
            self.var_rec_id.set("")
            self.var_rec_name.set("")
            self.var_rec_major.set("")
            messagebox.showinfo("Success", "Student deleted. Form cleared.")
    
    def view_student_attendance_action(self):
        """Show student's attendance records."""
        student_id = self.var_rec_id.get()
        
        if not student_id:
            messagebox.showerror("Error", "Please search for a student first")
            return
        
        records = get_attendance_record_details(student_id)
        if not records:
            messagebox.showinfo("No Records", f"No attendance records for {student_id}")
            return
        
        # Display records in a popup
        display_text = f"Attendance Records for {student_id}:\n\n"
        for i, (date, status) in enumerate(records, 1):
            display_text += f"{i}. {date} - {status}\n"
        
        messagebox.showinfo("Attendance Records", display_text)
    
    def delete_attendance_action(self):
        """Show attendance records and allow editing/deletion."""
        student_id = self.var_rec_id.get()
        
        if not student_id:
            messagebox.showerror("Error", "Please search for a student first")
            return
        
        records = update_attendance_entry(student_id)
        if not records:
            return
        
        # Create list of records with display text
        display_text = "Select record to edit:\n\n"
        for i, (att_id, date, status) in enumerate(records, 1):
            display_text += f"{i}. {date} - {status} (ID: {att_id})\n"
        
        messagebox.showinfo("Attendance Records", 
                          display_text + "\nNote: Use Edit Attendance button in main menu")
    
    def edit_attendance_action(self):
        """Show attendance records for editing/updating."""
        student_id = self.var_rec_id.get()
        
        if not student_id:
            messagebox.showerror("Error", "Please search for a student first")
            return
        
        records = update_attendance_entry(student_id)
        if not records:
            return
        
        # Show records with selection
        display_text = "Attendance Records:\n\n"
        for i, (att_id, date, status) in enumerate(records, 1):
            display_text += f"{i}. {date} - {status} (ID: {att_id})\n"
        
        display_text += "\nEnter the Record ID to update:"
        
        # Show dialog asking for record ID
        record_id_str = simpledialog.askstring("Edit Attendance", display_text)
        if not record_id_str:
            return
        
        try:
            record_id = int(record_id_str)
        except ValueError:
            messagebox.showerror("Error", "Record ID must be a number")
            return
        
        # Ask for new status
        status_options = "1. Present\n2. Absent"
        choice = simpledialog.askstring(
            "Update Status",
            f"Select new status:\n{status_options}\n\nEnter (1 or 2):"
        )
        
        if choice == "1":
            apply_attendance_update(record_id, "Present")
        elif choice == "2":
            apply_attendance_update(record_id, "Absent")
        else:
            messagebox.showerror("Error", "Invalid choice. Please enter 1 or 2")
    
    def show_reports(self):
        """Show the reports and search form."""
        self.clear_window()
        
        # ===== HEADER =====
        header = ttk.Label(
            self.root,
            text="Reports & Analytics",
            font=FONT_TITLE
        )
        header.pack(pady=10)
        
        # ===== MAIN CONTAINER FRAME =====
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=5)
        
        # ===== REPORT TYPE FRAME =====
        report_frame = ttk.LabelFrame(main_frame, text="Select Report Type", padding=10)
        report_frame.pack(pady=10, fill="x")
        
        # Report type selection
        report_var = tk.StringVar(value="student")
        
        radio_student = ttk.Radiobutton(
            report_frame,
            text="Individual Student Report",
            variable=report_var,
            value="student"
        )
        radio_student.pack(anchor="w", pady=5)
        
        radio_class = ttk.Radiobutton(
            report_frame,
            text="Class Overall Report",
            variable=report_var,
            value="class"
        )
        radio_class.pack(anchor="w", pady=5)
        
        radio_absentees = ttk.Radiobutton(
            report_frame,
            text="High Absentees List",
            variable=report_var,
            value="absentees"
        )
        radio_absentees.pack(anchor="w", pady=5)
        
        # ===== INPUT FRAME =====
        input_frame = ttk.LabelFrame(main_frame, text="Report Parameters", padding=10)
        input_frame.pack(pady=10, fill="x")
        
        # Student ID input (for student report)
        label_id = ttk.Label(input_frame, text="Student ID (for Individual Report):", font=FONT_NORMAL)
        label_id.pack(anchor="w", pady=(0, 5))
        
        entry_id = ttk.Entry(input_frame, width=40, font=FONT_NORMAL)
        entry_id.pack(anchor="w", pady=(0, 10), fill="x")
        
        # Absence threshold
        label_threshold = ttk.Label(input_frame, text="Absence Threshold (for High Absentees):", font=FONT_NORMAL)
        label_threshold.pack(anchor="w", pady=(0, 5))
        
        entry_threshold = ttk.Entry(input_frame, width=40, font=FONT_NORMAL)
        entry_threshold.insert(0, "5")  # Default value
        entry_threshold.pack(anchor="w", pady=(0, 10), fill="x")
        
        # ===== BUTTON FRAME =====
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15, fill="x")
        
        # Generate Report Button
        btn_generate = ttk.Button(
            button_frame,
            text="Generate Report",
            command=lambda: self.generate_report_action(report_var.get(), entry_id.get(), entry_threshold.get())
        )
        btn_generate.pack(side="left", padx=5, fill="x", expand=True)
        
        # View Class Stats Button
        btn_class_stats = ttk.Button(
            button_frame,
            text="Class Statistics",
            command=self.view_class_stats_action
        )
        btn_class_stats.pack(side="left", padx=5, fill="x", expand=True)
        
        # High Absentees Button
        btn_high_abs = ttk.Button(
            button_frame,
            text="High Absentees",
            command=lambda: self.view_high_absentees_action(entry_threshold.get())
        )
        btn_high_abs.pack(side="left", padx=5, fill="x", expand=True)
        
        # ===== BACK BUTTON FRAME =====
        back_frame = ttk.Frame(self.root)
        back_frame.pack(pady=10, padx=20, fill="x")
        
        btn_back = ttk.Button(
            back_frame,
            text="Back to Menu",
            command=self.show_menu
        )
        btn_back.pack(fill="x", expand=True)
    
    def generate_report_action(self, report_type, student_id, threshold):
        """Generate and display the selected report."""
        if report_type == "student":
            if not student_id:
                messagebox.showerror("Error", "Please enter a student ID")
                return
            
            report = generate_student_attendance_report(student_id)
            if report:
                display_text = format_attendance_report(report)
                messagebox.showinfo("Student Attendance Report", display_text)
        
        elif report_type == "class":
            report = generate_class_attendance_report()
            if report:
                display_text = f"""CLASS ATTENDANCE REPORT
{'='*50}

Total Students: {report['total_students']}
Total Records: {report['total_records']}
Present: {report['present_count']}
Absent: {report['absent_count']}
Overall Attendance: {report['overall_percentage']}%

TOP 5 STUDENTS BY ATTENDANCE:
"""
                # Sort by percentage descending
                sorted_students = sorted(
                    report['student_stats'].items(),
                    key=lambda x: x[1]['percentage'],
                    reverse=True
                )[:5]
                
                for i, (sid, stats) in enumerate(sorted_students, 1):
                    display_text += f"\n{i}. {stats['name']} ({sid})\n"
                    display_text += f"   Attendance: {stats['percentage']}%\n"
                
                messagebox.showinfo("Class Attendance Report", display_text)
        
        elif report_type == "absentees":
            try:
                threshold_val = int(threshold) if threshold else 5
            except ValueError:
                messagebox.showerror("Error", "Threshold must be a number")
                return
            
            absentees = get_high_absentees(threshold=threshold_val)
            if absentees:
                display_text = f"HIGH ABSENTEES (Absences >= {threshold_val}):\n\n"
                for i, student in enumerate(absentees, 1):
                    display_text += f"{i}. {student['name']} ({student['id']})\n"
                    display_text += f"   Absences: {student['absences']} / {student['total']}\n\n"
                
                messagebox.showinfo("High Absentees Report", display_text)
            else:
                messagebox.showinfo("Info", f"No students with {threshold_val}+ absences found")
    
    def view_class_stats_action(self):
        """View overall class statistics."""
        report = generate_class_attendance_report()
        if report:
            display_text = f"""CLASS STATISTICS
{'='*50}

Total Students: {report['total_students']}
Total Attendance Records: {report['total_records']}

OVERALL ATTENDANCE:
  Present: {report['present_count']}
  Absent: {report['absent_count']}
  Percentage: {report['overall_percentage']}%

STUDENT BREAKDOWN:
"""
            for sid, stats in sorted(report['student_stats'].items()):
                display_text += f"\n{stats['name']} ({sid})\n"
                display_text += f"  Attendance: {stats['percentage']}%\n"
            
            messagebox.showinfo("Class Statistics", display_text)
    
    def view_high_absentees_action(self, threshold):
        """View list of high absentees."""
        try:
            threshold_val = int(threshold) if threshold else 5
        except ValueError:
            messagebox.showerror("Error", "Threshold must be a number")
            return
        
        absentees = get_high_absentees(threshold=threshold_val)
        if absentees:
            display_text = f"STUDENTS WITH {threshold_val}+ ABSENCES:\n{'='*50}\n\n"
            for i, student in enumerate(absentees, 1):
                percentage = (student['total'] - student['absences']) / student['total'] * 100
                display_text += f"{i}. {student['name']} ({student['id']})\n"
                display_text += f"   Absences: {student['absences']}\n"
                display_text += f"   Total: {student['total']}\n"
                display_text += f"   Attendance: {round(percentage, 2)}%\n\n"
            
            messagebox.showinfo("High Absentees", display_text)
        else:
            messagebox.showinfo("Info", f"No students with {threshold_val}+ absences found")
    
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

