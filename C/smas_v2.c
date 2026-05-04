/*
 * ============================================================
 * Comprehensive Student Management & Attendance System (SMAS)
 * Track B  -  Procedural C  |  CS516 Advanced Programming
 * Author  : Albaraa
 * Partner : Abdullah (Track A - Python)
 * DB API  : MySQL C API (libmysqlclient)
 * Compiler: TDM-GCC on Windows / VS Code
 * ============================================================
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mysql.h>

/* --- DATABASE CONFIGURATION --- */
#define DB_HOST  "localhost"
#define DB_USER  "root"
#define DB_PASS  "12345678"
#define DB_NAME  "SMAS_DB"
#define DB_PORT  3306

/* --- DATA MODELS (STRUCTS) --- */
struct Student {
    long long universityID;
    char      fullName[101];
    char      major[51];
    char      registrationDate[20];
};

struct AttendanceRecord {
    int       attendanceID;
    long long studentID;
    char      attendanceDate[15]; /* Increased size to easily fit YYYY-MM-DD + \n + \0 */
    char      status[8];
};

/* --- GLOBAL VARIABLES --- */
MYSQL *conn = NULL;

/* --- UTILITY FUNCTIONS --- */
void printSeparator(void) {
    printf("--------------------------------------------------\n");
}

void clearInputBuffer(void) {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

/* --- DATABASE CONNECTION --- */
int connectDB(void) {
    conn = mysql_init(NULL);
    if (conn == NULL) {
        printf("[ERROR] MySQL initialization failed.\n");
        return 0;
    }

    if (mysql_real_connect(conn, DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_PORT, NULL, 0) == NULL) {
        printf("[ERROR] Connection failed: %s\n", mysql_error(conn));
        mysql_close(conn);
        conn = NULL;
        return 0;
    }

    printf("[OK] Connected to MySQL database successfully.\n");
    return 1;
}

void closeDB(void) {
    if (conn != NULL) {
        mysql_close(conn);
        conn = NULL;
        printf("[OK] Database connection closed safely.\n");
    }
}

/* --- CRUD OPERATIONS --- */

void insertStudent(void) {
    /* Manual Memory Allocation on the Heap */
    struct Student *s = (struct Student *)malloc(sizeof(struct Student));
    if (s == NULL) {
        printf("[ERROR] Memory allocation failed.\n");
        return;
    }

    char query[512];

    printSeparator();
    printf("  [1] REGISTER NEW STUDENT\n");
    printSeparator();

    printf("  Enter University ID : ");
    scanf("%lld", &s->universityID);
    clearInputBuffer();

    printf("  Enter Full Name     : ");
    fgets(s->fullName, sizeof(s->fullName), stdin);
    s->fullName[strcspn(s->fullName, "\n")] = '\0'; /* Safely remove the newline character */

    printf("  Enter Major         : ");
    fgets(s->major, sizeof(s->major), stdin);
    s->major[strcspn(s->major, "\n")] = '\0'; /* Safely remove the newline character */

    sprintf(query, "INSERT INTO Students (University_ID, FullName, Major) VALUES (%lld, '%s', '%s')", 
            s->universityID, s->fullName, s->major);

    if (mysql_query(conn, query)) {
        printf("  [ERROR] Insert failed: %s\n", mysql_error(conn));
    } else {
        printf("\n  [SUCCESS] Student registered successfully!\n");
    }

    /* Free allocated memory to prevent memory leaks */
    free(s); 
}

void logAttendance(void) {
    /* Manual Memory Allocation on the Heap */
    struct AttendanceRecord *rec = (struct AttendanceRecord *)malloc(sizeof(struct AttendanceRecord));
    if (rec == NULL) return;

    char query[512];
    int choice;

    printSeparator();
    printf("  [2] LOG ATTENDANCE\n");
    printSeparator();

    printf("  Enter Student ID        : ");
    scanf("%lld", &rec->studentID);
    clearInputBuffer();

    printf("  Enter Date (YYYY-MM-DD) : ");
    fgets(rec->attendanceDate, sizeof(rec->attendanceDate), stdin);
    rec->attendanceDate[strcspn(rec->attendanceDate, "\n")] = '\0'; /* Fix applied here for proper date reading */

    printf("  Select Status [1] Present  [2] Absent : ");
    scanf("%d", &choice);
    clearInputBuffer();

    if (choice == 1) strcpy(rec->status, "Present");
    else strcpy(rec->status, "Absent");

    sprintf(query, "INSERT INTO Attendance (Student_ID, AttendanceDate, Status) VALUES (%lld, '%s', '%s')",
            rec->studentID, rec->attendanceDate, rec->status);

    if (mysql_query(conn, query)) {
        printf("  [ERROR] Attendance log failed: %s\n", mysql_error(conn));
    } else {
        printf("\n  [SUCCESS] Attendance logged as '%s'.\n", rec->status);
    }

    /* Free allocated memory to prevent memory leaks */
    free(rec);
}

void updateStudent(void) {
    long long id;
    char newName[101], newMajor[51], fetchQuery[256], updateQuery[512];
    MYSQL_RES *result;
    MYSQL_ROW row;

    printSeparator();
    printf("  [3A] UPDATE STUDENT RECORD\n");
    printSeparator();

    printf("  Enter University ID to update: ");
    scanf("%lld", &id);
    clearInputBuffer();

    /* Fetch current values from the database */
    sprintf(fetchQuery, "SELECT FullName, Major FROM Students WHERE University_ID = %lld", id);
    if (mysql_query(conn, fetchQuery)) return;

    result = mysql_store_result(conn);
    row = mysql_fetch_row(result);

    if (row == NULL) {
        printf("  [NOT FOUND] No student found with ID %lld.\n", id);
        mysql_free_result(result);
        return;
    }

    printf("  New Full Name (Press Enter to keep '%s'): ", row[0]);
    fgets(newName, sizeof(newName), stdin);
    newName[strcspn(newName, "\n")] = '\0';

    printf("  New Major     (Press Enter to keep '%s'): ", row[1]);
    fgets(newMajor, sizeof(newMajor), stdin);
    newMajor[strcspn(newMajor, "\n")] = '\0';

    /* If input is empty, keep the old value */
    char finalName[101], finalMajor[51];
    strcpy(finalName, strlen(newName) > 0 ? newName : row[0]);
    strcpy(finalMajor, strlen(newMajor) > 0 ? newMajor : row[1]);

    mysql_free_result(result);

    sprintf(updateQuery, "UPDATE Students SET FullName='%s', Major='%s' WHERE University_ID=%lld", 
            finalName, finalMajor, id);

    if (mysql_query(conn, updateQuery)) {
        printf("  [ERROR] Update failed: %s\n", mysql_error(conn));
    } else {
        printf("\n  [SUCCESS] Student record updated successfully.\n");
    }
}

void deleteStudent(void) {
    long long id;
    char confirm[10]; /* Buffer size increased to easily store 'yes' + \n + \0 */
    char query[256];

    printSeparator();
    printf("  [3B] DELETE STUDENT\n");
    printSeparator();

    printf("  Enter University ID to delete: ");
    scanf("%lld", &id);
    clearInputBuffer();

    printf("  WARNING: This will also delete all related attendance records.\n");
    printf("  Type 'yes' to confirm: ");
    fgets(confirm, sizeof(confirm), stdin);
    confirm[strcspn(confirm, "\n")] = '\0'; /* Safely remove the newline character */

    if (strcmp(confirm, "yes") != 0) {
        printf("\n  [CANCELLED] Operation aborted. No records were deleted.\n");
        return;
    }

    sprintf(query, "DELETE FROM Students WHERE University_ID = %lld", id);

    if (mysql_query(conn, query)) {
        printf("  [ERROR] Delete failed: %s\n", mysql_error(conn));
    } else if (mysql_affected_rows(conn) == 0) {
        printf("  [NOT FOUND] No student found with ID %lld.\n", id);
    } else {
        printf("\n  [SUCCESS] Student and all attendance records deleted.\n");
    }
}

void searchAndReport(void) {
    long long id;
    char studentQuery[256], attendQuery[256];
    MYSQL_RES *result;
    MYSQL_ROW row;
    int present = 0, absent = 0, total = 0;

    printSeparator();
    printf("  [4] SEARCH & ATTENDANCE REPORT\n");
    printSeparator();

    printf("  Enter University ID: ");
    scanf("%lld", &id);
    clearInputBuffer();

    /* 1. Fetch Student Details */
    sprintf(studentQuery, "SELECT FullName, Major, RegistrationDate FROM Students WHERE University_ID = %lld", id);
    if (mysql_query(conn, studentQuery)) return;

    result = mysql_store_result(conn);
    row = mysql_fetch_row(result);

    if (row == NULL) {
        printf("  [NOT FOUND] No student found with ID %lld.\n", id);
        mysql_free_result(result);
        return;
    }

    printf("\n  >> STUDENT PROFILE <<\n");
    printf("  ID            : %lld\n", id);
    printf("  Full Name     : %s\n", row[0]);
    printf("  Major         : %s\n", row[1]);
    printf("  Registered On : %s\n", row[2]);
    mysql_free_result(result);

    printSeparator();

    /* 2. Fetch Attendance History */
    sprintf(attendQuery, "SELECT AttendanceDate, Status FROM Attendance WHERE Student_ID = %lld ORDER BY AttendanceDate ASC", id);
    if (mysql_query(conn, attendQuery)) return;

    result = mysql_store_result(conn);
    total = (int)mysql_num_rows(result);

    printf("  >> ATTENDANCE HISTORY (%d records) <<\n\n", total);

    if (total == 0) {
        printf("  No attendance records found for this student.\n");
    } else {
        printf("  %-15s | %-10s\n", "Date", "Status");
        printf("  ----------------|-----------\n");

        while ((row = mysql_fetch_row(result)) != NULL) {
            printf("  %-15s | %-10s\n", row[0], row[1]);
            
            if (strcmp(row[1], "Present") == 0) present++;
            else absent++;
        }
        
        printf("\n  [SUMMARY] Present: %d  |  Absent: %d  |  Total: %d\n", present, absent, total);
    }

    mysql_free_result(result);
    printSeparator();
}

void modifyMenu(void) {
    int choice;
    printSeparator();
    printf("  MODIFY RECORDS MENU\n");
    printSeparator();
    printf("  [1] Update Student Details\n");
    printf("  [2] Delete Student\n");
    printf("  [0] Back to Main Menu\n");
    printSeparator();
    printf("  Enter choice: ");

    scanf("%d", &choice);
    clearInputBuffer();

    if (choice == 1) updateStudent();
    else if (choice == 2) deleteStudent();
    else if (choice != 0) printf("  [ERROR] Invalid option.\n");
}

/* --- MAIN MENU & ENTRY POINT --- */
void showMenu(void) {
    printf("\n");
    printSeparator();
    printf("  SMAS - Student Management & Attendance System\n");
    printf("  Track B  |  Procedural C  |  CS516\n");
    printSeparator();
    printf("  [1] Register a New Student\n");
    printf("  [2] Log Daily Attendance\n");
    printf("  [3] Modify Records (Update / Delete)\n");
    printf("  [4] Search & Generate Report\n");
    printf("  [0] Exit System\n");
    printSeparator();
    printf("  Enter choice: ");
}

int main(void) {
    int choice;
    int running = 1;

    printf("\n  Starting SMAS System...\n");

    if (connectDB() == 0) {
        printf("  [FATAL] Exiting program due to database connection failure.\n");
        return 1;
    }

    while (running == 1) {
        showMenu();
        scanf("%d", &choice);
        clearInputBuffer();

        switch (choice) {
            case 1: insertStudent();   break;
            case 2: logAttendance();   break;
            case 3: modifyMenu();      break;
            case 4: searchAndReport(); break;
            case 0: 
                printf("\n  Exiting SMAS... Goodbye!\n");
                running = 0; 
                break;
            default: 
                printf("  [ERROR] Invalid choice. Please enter a number between 0 and 4.\n");
        }
    }

    closeDB();
    return 0;
}
