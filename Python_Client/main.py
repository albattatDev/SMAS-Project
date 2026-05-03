"""
SMAS - Student Management & Attendance System
Main entry point for the application.

HOW IT WORKS:
1. This file just imports and runs the GUI
2. All business logic is in modules/
3. All database code is in core/
4. All GUI code is in ui/
"""

import tkinter as tk
from ui.windows import MainWindow


def main():
    """
    Main function - starts the application.
    
    WHY SIMPLE?
    - All the complex code is in other modules
    - This file just orchestrates them
    - Easy to understand what the app does
    """
    # Create main window
    root = tk.Tk()
    
    # Initialize GUI with main window
    app = MainWindow(root)
    
    # Start the event loop (waits for user interactions)
    root.mainloop()


if __name__ == "__main__":
    main()