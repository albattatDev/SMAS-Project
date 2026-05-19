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
    char      attendanceDate[15]; 
    char      status[8];
};

/* --- GLOBAL VARIABLES --- */
MYSQL *conn = NULL;

/* --- UTILITY FUNCTIONS --- */
void printSeparator(void) {
    printf("--------------------------------------------------\n\n\n");
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

/* ============================================================
 * CRUD OPERATIONS
 * ============================================================ */

void insertStudent(void) {
    struct Student *s = (struct Student *)malloc(sizeof(struct Student));
    if (s == NULL) return;
    char query[512];

    printSeparator();
    printf("  [1] REGISTER NEW STUDENT\n");
    printSeparator();

    printf("  Enter University ID : ");
    scanf("%lld", &s->universityID);
    clearInputBuffer();

    printf("  Enter Full Name     : ");
    fgets(s->fullName, sizeof(s->fullName), stdin);
    s->fullName[strcspn(s->fullName, "\n")] = '\0';

    printf("  Enter Major         : ");
    fgets(s->major, sizeof(s->major), stdin);
    s->major[strcspn(s->major, "\n")] = '\0'; 

    sprintf(query, "INSERT INTO Students (University_ID, FullName, Major) VALUES (%lld, '%s', '%s')", 
            s->universityID, s->fullName, s->major);

    if (mysql_query(conn, query)) printf("  [ERROR] Insert failed: %s\n", mysql_error(conn));
    else printf("\n  [SUCCESS] Student registered successfully!\n");

    free(s); 
}

void logAttendance(void) {
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
    rec->attendanceDate[strcspn(rec->attendanceDate, "\n")] = '\0'; 

    printf("  Select Status [1] Present  [2] Absent : ");
    scanf("%d", &choice);
    clearInputBuffer();

    if (choice == 1) strcpy(rec->status, "Present");
    else strcpy(rec->status, "Absent");

    sprintf(query, "INSERT INTO Attendance (Student_ID, AttendanceDate, Status) VALUES (%lld, '%s', '%s')",
            rec->studentID, rec->attendanceDate, rec->status);

    if (mysql_query(conn, query)) printf("  [ERROR] Attendance log failed: %s\n", mysql_error(conn));
    else printf("\n  [SUCCESS] Attendance logged as '%s'.\n", rec->status);

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

    char finalName[101], finalMajor[51];
    strcpy(finalName, strlen(newName) > 0 ? newName : row[0]);
    strcpy(finalMajor, strlen(newMajor) > 0 ? newMajor : row[1]);

    mysql_free_result(result);

    sprintf(updateQuery, "UPDATE Students SET FullName='%s', Major='%s' WHERE University_ID=%lld", 
            finalName, finalMajor, id);

    if (mysql_query(conn, updateQuery)) printf("  [ERROR] Update failed: %s\n", mysql_error(conn));
    else printf("\n  [SUCCESS] Student record updated successfully.\n");
}

void updateAttendance(void) {
    long long student_id;
    int att_id;
    char query[512], fetchQuery[512];
    MYSQL_RES *result;
    MYSQL_ROW row;

    printSeparator();
    printf("  [3B] MODIFY ATTENDANCE RECORD\n");
    printSeparator();

    printf("  Enter Student ID: ");
    scanf("%lld", &student_id);
    clearInputBuffer();

    sprintf(fetchQuery, "SELECT Attendance_ID, AttendanceDate, Status FROM Attendance WHERE Student_ID = %lld ORDER BY AttendanceDate ASC", student_id);
    if (mysql_query(conn, fetchQuery)) return;

    result = mysql_store_result(conn);
    if (result == NULL || mysql_num_rows(result) == 0) {
        printf("  [NOT FOUND] No attendance records found for Student ID %lld.\n", student_id);
        if (result) mysql_free_result(result);
        return;
    }

    printf("\n  >> ATTENDANCE HISTORY FOR STUDENT %lld <<\n", student_id);
    printf("  %-6s | %-15s | %-10s\n", "ID", "Date", "Status");
    printf("  -------|-----------------|-----------\n");

    while ((row = mysql_fetch_row(result)) != NULL) {
        printf("  %-6s | %-15s | %-10s\n", row[0], row[1], row[2]);
    }
    mysql_free_result(result);

    printf("\n  Enter the 'ID' from the list above to modify: ");
    scanf("%d", &att_id);
    clearInputBuffer();

    sprintf(fetchQuery, "SELECT AttendanceDate, Status FROM Attendance WHERE Attendance_ID = %d AND Student_ID = %lld", att_id, student_id);
    if (mysql_query(conn, fetchQuery)) return;

    result = mysql_store_result(conn);
    row = mysql_fetch_row(result);

    if (row == NULL) {
        printf("  [ERROR] Invalid ID. This record does not belong to the student.\n");
        mysql_free_result(result);
        return;
    }

    char newDate[15], finalDate[15], finalStatus[8];
    int statusChoice;

    printf("  New Date (YYYY-MM-DD) [Press Enter to keep '%s']: ", row[0]);
    fgets(newDate, sizeof(newDate), stdin);
    newDate[strcspn(newDate, "\n")] = '\0';
    strcpy(finalDate, strlen(newDate) > 0 ? newDate : row[0]);

    printf("  New Status [1] Present  [2] Absent  [0] Keep '%s': ", row[1]);
    scanf("%d", &statusChoice);
    clearInputBuffer();

    if (statusChoice == 1) strcpy(finalStatus, "Present");
    else if (statusChoice == 2) strcpy(finalStatus, "Absent");
    else strcpy(finalStatus, row[1]); 

    mysql_free_result(result);

    sprintf(query, "UPDATE Attendance SET AttendanceDate='%s', Status='%s' WHERE Attendance_ID=%d", finalDate, finalStatus, att_id);
    if (mysql_query(conn, query)) printf("  [ERROR] Update failed: %s\n", mysql_error(conn));
    else printf("\n  [SUCCESS] Attendance record updated successfully.\n");
}

void deleteStudent(void) {
    long long id;
    char confirm[10], query[256];

    printSeparator();
    printf("  [3C] DELETE STUDENT\n");
    printSeparator();

    printf("  Enter University ID to delete: ");
    scanf("%lld", &id);
    clearInputBuffer();

    printf("  WARNING: This will also delete all related attendance records.\n");
    printf("  Type 'yes' to confirm: ");
    fgets(confirm, sizeof(confirm), stdin);
    confirm[strcspn(confirm, "\n")] = '\0'; 

    if (strcmp(confirm, "yes") != 0) {
        printf("\n  [CANCELLED] Operation aborted.\n");
        return;
    }

    sprintf(query, "DELETE FROM Students WHERE University_ID = %lld", id);
    if (mysql_query(conn, query)) printf("  [ERROR] Delete failed: %s\n", mysql_error(conn));
    else if (mysql_affected_rows(conn) == 0) printf("  [NOT FOUND] No student found.\n");
    else printf("\n  [SUCCESS] Student and attendance deleted.\n");
}

void modifyMenu(void) {
    int choice;
    printSeparator();
    printf("  MODIFY RECORDS MENU\n");
    printSeparator();
    printf("  [1] Update Student Details\n");
    printf("  [2] Modify Attendance Record\n");
    printf("  [3] Delete Student\n");
    printf("  [0] Back to Main Menu\n");
    printSeparator();
    printf("  Enter choice: ");

    scanf("%d", &choice);
    clearInputBuffer();

    if (choice == 1) updateStudent();
    else if (choice == 2) updateAttendance();
    else if (choice == 3) deleteStudent();
    else if (choice != 0) printf("  [ERROR] Invalid option.\n");
}

/* ============================================================
 * REPORTS MODULE (Matches Python Implementation)
 * ============================================================ */

/* Report 1: Specific Student Report */
void reportStudentAttendance(void) {
    long long id;
    char query[512];
    MYSQL_RES *result;
    MYSQL_ROW row;
    int present = 0, absent = 0, total = 0;

    printf("\n  Enter University ID: ");
    scanf("%lld", &id);
    clearInputBuffer();

    sprintf(query, "SELECT FullName, Major FROM Students WHERE University_ID = %lld", id);
    if (mysql_query(conn, query)) return;
    result = mysql_store_result(conn);
    row = mysql_fetch_row(result);

    if (row == NULL) {
        printf("  [NOT FOUND] Student not found.\n");
        mysql_free_result(result);
        return;
    }

    printf("\n  STUDENT ATTENDANCE REPORT\n");
    printf("  =========================\n");
    printf("  ID    : %lld\n  Name  : %s\n  Major : %s\n\n", id, row[0], row[1]);
    mysql_free_result(result);

    sprintf(query, "SELECT AttendanceDate, Status FROM Attendance WHERE Student_ID = %lld ORDER BY AttendanceDate ASC", id);
    if (mysql_query(conn, query)) return;
    result = mysql_store_result(conn);
    total = (int)mysql_num_rows(result);

    if (total == 0) {
        printf("  No attendance records found.\n");
    } else {
        int i = 1;
        while ((row = mysql_fetch_row(result)) != NULL) {
            printf("  %d. %s - %s\n", i++, row[0], row[1]);
            if (strcmp(row[1], "Present") == 0) present++;
            else absent++;
        }
        float percentage = ((float)present / total) * 100;
        printf("\n  STATISTICS: Total: %d | Present: %d | Absent: %d | Attendance: %.2f%%\n", total, present, absent, percentage);
    }
    mysql_free_result(result);
}

/* Report 2: Class Overall Statistics */
void reportClassAttendance(void) {
    char query[512];
    MYSQL_RES *result;
    MYSQL_ROW row;

    /* Using advanced SQL to calculate everything in one query */
    sprintf(query, 
        "SELECT S.University_ID, S.FullName, "
        "COUNT(A.Attendance_ID) AS Total, "
        "SUM(CASE WHEN A.Status='Present' THEN 1 ELSE 0 END) AS PresentCount "
        "FROM Students S LEFT JOIN Attendance A ON S.University_ID = A.Student_ID "
        "GROUP BY S.University_ID");

    if (mysql_query(conn, query)) return;
    result = mysql_store_result(conn);

    int classTotalRecords = 0;
    int classPresentCount = 0;
    int totalStudents = (int)mysql_num_rows(result);

    printf("\n  CLASS ATTENDANCE REPORT\n");
    printf("  =======================\n");
    printf("  %-12s | %-20s | %-5s | %-7s | %-7s | %-5s\n", "ID", "Name", "Total", "Present", "Absent", "Percentage");
    printf("  -------------|----------------------|-------|---------|---------|----------\n");

    while ((row = mysql_fetch_row(result)) != NULL) {
        int total = row[2] ? atoi(row[2]) : 0;
        int present = row[3] ? atoi(row[3]) : 0;
        int absent = total - present;
        float percentage = total > 0 ? ((float)present / total) * 100 : 0.0;

        classTotalRecords += total;
        classPresentCount += present;

        printf("  %-12s | %-20s | %-5d | %-7d | %-7d | %.2f%%\n", 
               row[0], row[1], total, present, absent, percentage);
    }

    int classAbsentCount = classTotalRecords - classPresentCount;
    float classPercentage = classTotalRecords > 0 ? ((float)classPresentCount / classTotalRecords) * 100 : 0.0;

    printf("  -------------|----------------------|-------|---------|---------|----------\n");
    printf("  [OVERALL] Students: %d | Total Records: %d | Avg Attendance: %.2f%%\n", 
           totalStudents, classTotalRecords, classPercentage);

    mysql_free_result(result);
}

/* Report 3: Search by Percentage */
void reportSearchByPercentage(void) {
    float minPct, maxPct;
    char query[512];
    MYSQL_RES *result;
    MYSQL_ROW row;
    int found = 0;

    printf("\n  Enter Minimum Percentage (e.g. 0): ");
    scanf("%f", &minPct);
    printf("  Enter Maximum Percentage (e.g. 100): ");
    scanf("%f", &maxPct);
    clearInputBuffer();

    sprintf(query, 
        "SELECT S.University_ID, S.FullName, "
        "COUNT(A.Attendance_ID) AS Total, "
        "SUM(CASE WHEN A.Status='Present' THEN 1 ELSE 0 END) AS PresentCount "
        "FROM Students S JOIN Attendance A ON S.University_ID = A.Student_ID "
        "GROUP BY S.University_ID");

    if (mysql_query(conn, query)) return;
    result = mysql_store_result(conn);

    printf("\n  STUDENTS BETWEEN %.1f%% AND %.1f%%\n", minPct, maxPct);
    printf("  ====================================\n");

    while ((row = mysql_fetch_row(result)) != NULL) {
        int total = atoi(row[2]);
        int present = row[3] ? atoi(row[3]) : 0;
        float percentage = total > 0 ? ((float)present / total) * 100 : 0.0;

        if (percentage >= minPct && percentage <= maxPct) {
            printf("  ID: %-12s | Name: %-20s | Percentage: %.2f%%\n", row[0], row[1], percentage);
            found++;
        }
    }

    if (found == 0) printf("  No students found in this range.\n");
    mysql_free_result(result);
}

/* Report 4: High Absentees */
void reportHighAbsentees(void) {
    int threshold;
    char query[512];
    MYSQL_RES *result;
    MYSQL_ROW row;

    printf("\n  Enter absence threshold (e.g. 5): ");
    scanf("%d", &threshold);
    clearInputBuffer();

    /* Advanced SQL: Calculating absences and filtering using HAVING */
    sprintf(query, 
        "SELECT S.University_ID, S.FullName, COUNT(A.Attendance_ID) as Total, "
        "SUM(CASE WHEN A.Status='Absent' THEN 1 ELSE 0 END) as Absences "
        "FROM Students S JOIN Attendance A ON S.University_ID = A.Student_ID "
        "GROUP BY S.University_ID "
        "HAVING Absences >= %d ORDER BY Absences DESC", threshold);

    if (mysql_query(conn, query)) return;
    result = mysql_store_result(conn);

    printf("\n  HIGH ABSENTEE WARNING (>= %d Absences)\n", threshold);
    printf("  ======================================\n");
    
    if (mysql_num_rows(result) == 0) {
        printf("  No students reached this threshold.\n");
    } else {
        while ((row = mysql_fetch_row(result)) != NULL) {
            printf("  ID: %-10s | Absences: %-3s (Out of %s) | Name: %s\n", 
                   row[0], row[3], row[2], row[1]);
        }
    }
    mysql_free_result(result);
}

/* Report 5: Attendance by Date */
void reportAttendanceByDate(void) {
    char targetDate[15];
    char query[512];
    MYSQL_RES *result;
    MYSQL_ROW row;

    printf("\n  Enter target date (YYYY-MM-DD): ");
    fgets(targetDate, sizeof(targetDate), stdin);
    targetDate[strcspn(targetDate, "\n")] = '\0';

    sprintf(query, 
        "SELECT S.University_ID, S.FullName, A.Status "
        "FROM Attendance A JOIN Students S ON A.Student_ID = S.University_ID "
        "WHERE A.AttendanceDate = '%s'", targetDate);

    if (mysql_query(conn, query)) return;
    result = mysql_store_result(conn);

    printf("\n  ATTENDANCE FOR DATE: %s\n", targetDate);
    printf("  ================================\n");

    if (mysql_num_rows(result) == 0) {
        printf("  No records found for this date.\n");
    } else {
        while ((row = mysql_fetch_row(result)) != NULL) {
            printf("  ID: %-12s | Status: %-8s | Name: %s\n", row[0], row[2], row[1]);
        }
    }
    mysql_free_result(result);
}

/* The Sub-Menu for Option 4 */
void reportMenu(void) {
    int choice;
    printSeparator();
    printf("  REPORTS & ANALYTICS MENU\n");
    printSeparator();
    printf("  [1] Student Detailed Report\n");
    printf("  [2] Class Overall Statistics\n");
    printf("  [3] Search by Attendance Percentage\n");
    printf("  [4] High Absentees Warning\n");
    printf("  [5] Attendance by Specific Date\n");
    printf("  [0] Back to Main Menu\n");
    printSeparator();
    printf("  Enter choice: ");

    scanf("%d", &choice);
    clearInputBuffer();

    if (choice == 1) reportStudentAttendance();
    else if (choice == 2) reportClassAttendance();
    else if (choice == 3) reportSearchByPercentage();
    else if (choice == 4) reportHighAbsentees();
    else if (choice == 5) reportAttendanceByDate();
    else if (choice != 0) printf("  [ERROR] Invalid option.\n");
    printSeparator();
}

/* --- MAIN MENU & ENTRY POINT --- */
void showMenu(void) {
    printf("\n");
    printSeparator();
    printf("  SMAS - Student Management & Attendance System\n");
    printSeparator();
    printf("  [1] Register a New Student\n");
    printf("  [2] Log Daily Attendance\n");
    printf("  [3] Modify Records (Update / Delete)\n");
    printf("  [4] Reports & Analytics Module\n"); /* Updated Title */
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
            case 1: insertStudent(); break;
            case 2: logAttendance(); break;
            case 3: modifyMenu();    break;
            case 4: reportMenu();    break; /* Now opens the Report Sub-Menu */
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
