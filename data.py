import pymysql
from tkinter import messagebox

# Global variables
conn = None
mycursor = None

def conn_database():
    global conn, mycursor
    try:
        conn = pymysql.connect(host="localhost", user="root", password="********")
        mycursor = conn.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS employee_data")
        mycursor.execute("USE employee_data")
        
        # Create table with Email field
        mycursor.execute("""S
            CREATE TABLE IF NOT EXISTS data (
                Id INT PRIMARY KEY,
                Name VARCHAR(50),
                Phone VARCHAR(15),
                Role VARCHAR(62),
                Gender VARCHAR(50),
                Salary DECIMAL(10, 2),
                Email VARCHAR(100)
            )
        """)
        conn.commit()
        messagebox.showinfo("Success", "Your database is connected successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong. Try again later: {e}")

def insert(id, name, phone, role, gender, salary, email):
    try:
        mycursor.execute("INSERT INTO data VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                         (id, name, phone, role, gender, salary, email))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))

def id_exists(id):
    mycursor.execute("SELECT COUNT(*) FROM data WHERE Id=%s", (id,))
    result = mycursor.fetchone()
    return result[0] > 0

def fetch_employees():
    mycursor.execute("SELECT * FROM data")
    return mycursor.fetchall()

def update(id, new_name, new_phone, new_role, new_gender, new_salary, new_email):
    try:
        mycursor.execute("""
            UPDATE data 
            SET Name=%s, Phone=%s, Role=%s, Gender=%s, Salary=%s, Email=%s 
            WHERE Id=%s
        """, (new_name, new_phone, new_role, new_gender, new_salary, new_email, id))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Update Error", str(e))

def delete(id):
    try:
        mycursor.execute("DELETE FROM data WHERE Id=%s", (id,))
        conn.commit()
    except Exception as e:
        messagebox.showerror("Delete Error", str(e))

def search(option, value):
    try:
        if option not in ["Id", "Name", "Phone", "Role", "Gender", "Salary", "Email"]:
            raise ValueError("Invalid search field")
        query = f"SELECT * FROM data WHERE {option}=%s"
        mycursor.execute(query, (value,))
        return mycursor.fetchall()
    except Exception as e:
        messagebox.showerror("Search Error", str(e))
        return []

def deleteall_records():
    try:
        mycursor.execute("TRUNCATE TABLE data")
        conn.commit()
    except Exception as e:
        messagebox.showerror("Truncate Error", str(e))

# Initialize database connection
conn_database()
