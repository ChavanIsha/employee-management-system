import sqlite3
import os
import csv

# Database setup
def init_db():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            department TEXT NOT NULL,
            salary REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Admin login system
def login():
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        print("\nLogin successful!\n")
        return True
    else:
        print("\nInvalid credentials! Access Denied.\n")
        return False

# Add employee
def add_employee():
    name = input("Enter Employee Name: ")
    position = input("Enter Position: ")
    department = input("Enter Department: ")
    salary = float(input("Enter Salary: "))

    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, position, department, salary)
        VALUES (?, ?, ?, ?)
    ''', (name, position, department, salary))
    conn.commit()
    conn.close()
    print("\nEmployee added successfully!\n")

# View employees
def view_employees():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    records = cursor.fetchall()
    conn.close()

    if records:
        print("\n--- Employee Records ---")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Department: {row[3]}, Salary: {row[4]}")
    else:
        print("\nNo employee records found.\n")

# Update employee
def update_employee():
    emp_id = int(input("Enter Employee ID to Update: "))
    name = input("Enter New Name: ")
    position = input("Enter New Position: ")
    department = input("Enter New Department: ")
    salary = float(input("Enter New Salary: "))

    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE employees
        SET name = ?, position = ?, department = ?, salary = ?
        WHERE id = ?
    ''', (name, position, department, salary, emp_id))
    conn.commit()
    conn.close()
    print("\nEmployee record updated successfully!\n")

# Delete employee
def delete_employee():
    emp_id = int(input("Enter Employee ID to Delete: "))
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id = ?', (emp_id,))
    conn.commit()
    conn.close()
    print("\nEmployee record deleted successfully!\n")

# Search employee
def search_employee():
    name = input("Enter Employee Name to Search: ")
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE name LIKE ?', ('%' + name + '%',))
    records = cursor.fetchall()
    conn.close()

    if records:
        print("\n--- Search Results ---")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Department: {row[3]}, Salary: {row[4]}")
    else:
        print("\nNo matching employee found.\n")

# Export to CSV
def export_to_csv():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    records = cursor.fetchall()
    conn.close()

    with open('employees.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Name', 'Position', 'Department', 'Salary'])
        writer.writerows(records)

    print("\nEmployee data exported successfully to 'employees.csv'\n")

# Sort employees
def sort_employees():
    print("\n1. Sort by Salary")
    print("2. Sort by Department")
    choice = input("Choose sorting option: ")

    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()

    if choice == '1':
        cursor.execute('SELECT * FROM employees ORDER BY salary DESC')
    elif choice == '2':
        cursor.execute('SELECT * FROM employees ORDER BY department')
    else:
        print("Invalid option!")
        return
    
    records = cursor.fetchall()
    conn.close()

    if records:
        print("\n--- Sorted Employees ---")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Department: {row[3]}, Salary: {row[4]}")
    else:
        print("\nNo employee records found.\n")

# Department-wise report
def department_report():
    department = input("Enter department name: ")
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees WHERE department = ?', (department,))
    records = cursor.fetchall()
    conn.close()

    if records:
        print(f"\n--- Employees in {department} Department ---")
        for row in records:
            print(f"ID: {row[0]}, Name: {row[1]}, Position: {row[2]}, Salary: {row[4]}")
    else:
        print("\nNo employees found in this department.\n")

# Total salary expense
def total_salary_expense():
    conn = sqlite3.connect('employee.db')
    cursor = conn.cursor()
    cursor.execute('SELECT SUM(salary) FROM employees')
    total = cursor.fetchone()[0]
    conn.close()
    
    print(f"\nTotal Salary Expense: {total if total else 0}\n")

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main menu
def menu():
    while True:
        print("\n--- Employee Management System ---")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Search Employee")
        print("6. Exit")
        print("7. Export Data to CSV")
        print("8. Sort Employees")
        print("9. Department-wise Report")
        print("10. Total Salary Expense")
        print("11. Clear Screen")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_employee()
        elif choice == '2':
            view_employees()
        elif choice == '3':
            update_employee()
        elif choice == '4':
            delete_employee()
        elif choice == '5':
            search_employee()
        elif choice == '6':
            print("Exiting...")
            break
        elif choice == '7':
            export_to_csv()
        elif choice == '8':
            sort_employees()
        elif choice == '9':
            department_report()
        elif choice == '10':
            total_salary_expense()
        elif choice == '11':
            clear_screen()
        else:
            print("Invalid choice! Please try again.")

if __name__ == '__main__':
    init_db()
    if login():
        menu()
