"""
Configuration file for SMAS application.
All settings are stored here in ONE PLACE - easy to change later!
"""

# ===== DATABASE SETTINGS =====
# These settings connect to your MySQL database
DB_CONFIG = {
    'host': 'localhost',           # Where the database is (your computer)
    'user': 'root',                # MySQL username
    'password': '12345678',        # MySQL password
    'database': 'SMAS_DB'          # Database name
}

# ===== APPLICATION SETTINGS =====
# These are just constants for the GUI

APP_TITLE = "SMAS - Student Management & Attendance System"
APP_WIDTH = 700
APP_HEIGHT = 550

# Font styles (used throughout the app)
FONT_TITLE = ("Arial", 16, "bold")
FONT_SUBTITLE = ("Arial", 12, "bold")
FONT_NORMAL = ("Arial", 10)
FONT_BUTTON = ("Arial", 10, "bold")
