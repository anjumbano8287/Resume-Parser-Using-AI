from customtkinter import *
from PIL import Image
from tkinter import ttk, messagebox
import tkinter as tk
import data  # Ensure your database module is updated to handle the email field
import csv
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import re
import os
import csv
from tkinter import filedialog, messagebox, END
from docx import Document
from PyPDF2 import PdfReader

# Define regular expressions for email, phone, and name (name can be flexible)
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
PHONE_REGEX = r'\+?[0-9\s\-\(\)]{7,15}'
NAME_REGEX = r'\b[A-Z][a-z]+\s[A-Z][a-z]+'

def fetch_employee_data():
    """
    Automatically fetch Name, Email, and Phone from a file and display it in the entry fields.
    Supports CSV, TXT, DOCX, and PDF formats.
    """
    file_path = filedialog.askopenfilename(filetypes=[
        ("All Files", "*.*"),
        ("CSV files", "*.csv"),
        ("Text files", "*.txt"),
        ("PDF files", "*.pdf"),
        ("Word files", "*.docx")
    ])
    if file_path:
        try:
            file_extension = os.path.splitext(file_path)[-1].lower()
            text = ""

            # Extract text based on file type
            if file_extension == ".csv":
                with open(file_path, "r") as file:
                    reader = csv.reader(file)
                    for row in reader:
                        text += " ".join(row) + " "

            elif file_extension == ".txt":
                with open(file_path, "r") as file:
                    text = file.read()

            elif file_extension == ".docx":
                doc = Document(file_path)
                text = " ".join([para.text for para in doc.paragraphs])

            elif file_extension == ".pdf":
                reader = PdfReader(file_path)
                text = " ".join([page.extract_text() for page in reader.pages])

            # Use regex to extract Name, Email, and Phone
            name = re.search(NAME_REGEX, text)
            email = re.search(EMAIL_REGEX, text)
            phone = re.search(PHONE_REGEX, text)

            # Populate the entry fields
            if name:
                nameEntry.delete(0, END)
                nameEntry.insert(0, name.group(0).strip())
            else:
                nameEntry.delete(0, END)
                nameEntry.insert(0, "Not Found")

            if email:
                emailEntry.delete(0, END)
                emailEntry.insert(0, email.group(0).strip())
            else:
                emailEntry.delete(0, END)
                emailEntry.insert(0, "Not Found")

            if phone:
                phoneEntry.delete(0, END)
                phoneEntry.insert(0, phone.group(0).strip())
            else:
                phoneEntry.delete(0, END)
                phoneEntry.insert(0, "Not Found")

            messagebox.showinfo("Success", "Employee data loaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "No file selected!")


# Add the button in the button frame


def export_to_csv():
    employees = data.fetch_employees()
    with open("employees.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Id", "Name", "Email", "Phone", "Role", "Gender", "Salary"])  # Updated header
        for employee in employees:
            writer.writerow(employee)
    messagebox.showinfo("Export", "Data exported to employees.csv successfully")



def open_rms(parent_window=None):
    """
    Function to open the RMS system UI in a new Toplevel window.
    """
    rms_window = tk.Toplevel(parent_window) if parent_window else tk.Tk()
    rms_window.geometry("800x600")
    rms_window.title("RMS System")

    try:
        # Open the image using PIL
        logo_image = Image.open("ResumeRecordedData.png")
        logo_image = logo_image.resize((800, 200), Image.ANTIALIAS)  # Resize if necessary

        # Convert the image for Tkinter
        logo_tk = ImageTk.PhotoImage(logo_image)

        # Store the reference to prevent garbage collection
        rms_window.logo_image = logo_tk  # Save it to the window to keep it alive

        # Create the logo label
        logo_label = tk.Label(rms_window, image=logo_tk)
        logo_label.pack(pady=20)

    except Exception as e:
        tk.Label(rms_window, text=f"Error loading logo: {e}", font=("Arial", 14)).pack(pady=20)

    # Add other widgets to the window
    tk.Label(rms_window, text="Welcome to the RMS System", font=("Arial", 16)).pack(pady=20)


def treeview_data():
    employees = data.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('', END, values=employee)

def add_employee():
    if idEntry.get() == "" or nameEntry.get() == "" or emailEntry.get() == "" or phoneEntry.get() == "" or salaryEntry.get() == "":
        messagebox.showerror("Error", "All fields are required")
    elif data.id_exists(idEntry.get()):
        messagebox.showerror("Error", "Id already exists")
    else:
        data.insert(
            idEntry.get(),
            nameEntry.get(),
            phoneEntry.get(),
            roleBox.get(),
            genderBox.get(),
            salaryEntry.get(),
            emailEntry.get()
        )
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data successfully added")

def update_employee():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select data to update")
    else:
        data.update(
            idEntry.get(),
            nameEntry.get(),
            emailEntry.get(),
            phoneEntry.get(),
            roleBox.get(),
            genderBox.get(),
            salaryEntry.get()
        )
        treeview_data()
        clear()
        messagebox.showinfo("Success", "Data successfully updated")
     

def delete_employee():
    selected_item = tree.selection()  # Get selected item
    if not selected_item:
        messagebox.showerror("Error", "Select data to delete")
    else:
        # Fetch the selected item's ID
        selected_row = tree.item(selected_item[0])['values']
        employee_id = selected_row[0]  # Assuming ID is the first column

        # Confirm deletion
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete Employee ID: {employee_id}?")
        if confirm:
            data.delete(employee_id)  # Delete from database
            treeview_data()  # Refresh the treeview
            clear()  # Clear the form fields
            messagebox.showinfo("Success", "Employee deleted successfully")


def clear(value=False):
    if value:
        tree.selection_remove(tree.focus())
    idEntry.delete(0, END)
    nameEntry.delete(0, END)
    phoneEntry.delete(0, END)
    roleBox.set("Software Engineer")
    genderBox.set("Male")
    salaryEntry.delete(0, END)
    emailEntry.delete(0, END)

def selection(event):
    selected_item = tree.selection()
    if selected_item:
        clear()
        row = tree.item(selected_item)['values']
        idEntry.insert(0, row[0])
        nameEntry.insert(0, row[1])
        phoneEntry.insert(0, row[2])
        roleBox.set(row[3])
        genderBox.set(row[4])
        salaryEntry.insert(0, row[5])
        emailEntry.insert(0, row[6])
def search_employee():
   if searchEntry.get()=='':
      messagebox.showerror("Error","Enter value to search")
   elif searchBox.get()=="Search By":
      messagebox.showerror("Error","please select an option")    
   else:
      search_data=data.search(searchBox.get(),searchEntry.get())
      tree.delete(*tree.get_children())
      for employee in search_data:
        tree.insert('',END,values=employee)        


def show_all():
   treeview_data()
   searchEntry.delete(0,END)
   searchBox.set("Search By")
# GUI setup
window = CTk()
window.geometry("1200x700+100+100")
window.resizable(0, 0)
window.title("HR Management System")

# Top Logo
logo = CTkImage(Image.open("ResumeRecordedData.png"), size=(1200, 250))
logoLabel = CTkLabel(window, image=logo, text='')
logoLabel.grid(row=0, column=0, columnspan=2)

# Left Frame for Form
leftFrame = CTkFrame(window)
leftFrame.grid(row=1, column=0)

idLabel = CTkLabel(leftFrame, text="Id", font=("Arial", 18, "bold"), padx=20, pady=15)
idLabel.grid(row=1, column=0, sticky='w')
idEntry = CTkEntry(leftFrame, font=("Arial", 15, "bold"), width=180)
idEntry.grid(row=1, column=1)

nameLabel = CTkLabel(leftFrame, text="Name", font=("Arial", 18, "bold"), padx=20, pady=15)
nameLabel.grid(row=2, column=0, sticky='w')
nameEntry = CTkEntry(leftFrame, font=("Arial", 15, "bold"), width=180)
nameEntry.grid(row=2, column=1)



phoneLabel = CTkLabel(leftFrame, text="Phone", font=("Arial", 18, "bold"), padx=20, pady=15)
phoneLabel.grid(row=4, column=0, sticky='w')
phoneEntry = CTkEntry(leftFrame, font=("Arial", 15, "bold"), width=180)
phoneEntry.grid(row=4, column=1)

roleLabel = CTkLabel(leftFrame, text="Role", font=("Arial", 18, "bold"), padx=20, pady=15)
roleLabel.grid(row=5, column=0, sticky='w')
role_options = [
    "Software Engineer",
    "Data Scientist",
    "UI/UX Designer",
    "Project Manager",
    "DevOps Engineer",
    "Product Manager",
    "Data Analyst"
]
roleBox = CTkComboBox(leftFrame, values=role_options, width=180, font=("Arial", 14, "bold"), state="readonly")
roleBox.grid(row=5, column=1)
roleBox.set(role_options[0])

genderLabel = CTkLabel(leftFrame, text="Gender", font=("Arial", 18, "bold"), padx=20, pady=15)
genderLabel.grid(row=6, column=0, sticky='w')
gender_options = ["Male", "Female", "Other"]
genderBox = CTkComboBox(leftFrame, values=gender_options, width=180, font=("Arial", 14, "bold"), state="readonly")
genderBox.grid(row=6, column=1)
genderBox.set(gender_options[0])

salaryLabel = CTkLabel(leftFrame, text="Salary", font=("Arial", 18, "bold"), padx=20, pady=15)
salaryLabel.grid(row=7, column=0, sticky='w')
salaryEntry = CTkEntry(leftFrame, font=("Arial", 15, "bold"), width=180)
salaryEntry.grid(row=7, column=1)


emailLabel = CTkLabel(leftFrame, text="Email", font=("Arial", 18, "bold"), padx=20, pady=15)
emailLabel.grid(row=3, column=0, sticky='w')
emailEntry = CTkEntry(leftFrame, font=("Arial", 15, "bold"), width=180)
emailEntry.grid(row=3, column=1)

# Right Frame for TreeView
rightFrame = CTkFrame(window)
rightFrame.grid(row=1, column=1)

search_options = ["Id", "Name", "Phone", "Role", "Gender", "Salary", "Email"]
searchBox = CTkComboBox(rightFrame, values=search_options, state="readonly")
searchBox.grid(row=0, column=0)
searchBox.set("Search By")

searchEntry = CTkEntry(rightFrame)
searchEntry.grid(row=0, column=1)

searchButton = CTkButton(rightFrame, text="Search", cursor="hand2", width=180, command=lambda: search_employee())
searchButton.grid(row=0, column=2)


showAllButton=CTkButton(rightFrame,text="ShowAll",cursor="hand2",width=180,command=show_all)
showAllButton.grid(row=0, column=3)

tree = ttk.Treeview(rightFrame, height=11)
tree.grid(row=1, column=0, columnspan=4)
tree["columns"] = ("Id", "Name", "Phone", "Role", "Gender", "Salary","Email")

tree.column("Id", width=100)
tree.column("Name", width=150)
tree.column("Phone", width=100)
tree.column("Role", width=130)
tree.column("Gender", width=80)
tree.column("Salary", width=100)
tree.column("Email", width=200)

tree.heading("Id", text="Id")
tree.heading("Name", text="Name")
tree.heading("Phone", text="Phone")
tree.heading("Role", text="Role")
tree.heading("Gender", text="Gender")
tree.heading("Salary", text="Salary")
tree.heading("Email", text="Email")
tree.config(show="headings")

Style=ttk.Style() 
Style.configure("Treeview.Heading",font=("Arial",15,"bold"))
Style.configure("Treeview",font=("Arial",15,"bold"),rowheight="30",background="#161C30",foreground="White")

scrollbar=ttk.Scrollbar(rightFrame,orient="vertical")
scrollbar.grid(row=1,column=4,sticky="ns")
tree.config(yscrollcommand=scrollbar.set)

buttonFrame=CTkFrame(window,fg_color="#161C30",width=1150,height=70)
buttonFrame.grid(row=10,column=0,columnspan=2,pady=50,sticky="ew")

buttonFrame.grid_columnconfigure(0, weight=1)  # Empty space on the left
buttonFrame.grid_columnconfigure(6, weight=1)
addButton=CTkButton(buttonFrame, text="Add Employee", cursor="hand2",font=("Arial",15,"bold"),width=160,corner_radius=15,command=add_employee)
addButton.grid(row=0,column=1,pady=5,padx=10)

fetchButton = CTkButton(buttonFrame, text="Fetch Employee", cursor="hand2", font=("Arial", 15, "bold"),
                        width=160, corner_radius=15, command=fetch_employee_data)
fetchButton.grid(row=0, column=2, pady=5, padx=10)


deleteButton=CTkButton(buttonFrame, text="Delete Employee", cursor="hand2",font=("Arial",15,"bold"),width=160,corner_radius=15,command=delete_employee)
deleteButton.grid(row=0,column=3,pady=5,padx=10)


# exportButton = CTkButton(buttonFrame, text="Export to CSV", cursor="hand2", font=("Arial", 15, "bold"), width=160, corner_radius=15, command=export_to_csv())
# exportButton.grid(row=0, column=5, pady=5, padx=10)
exportButton = CTkButton(buttonFrame, text="Export to CSV", cursor="hand2", font=("Arial", 15, "bold"), width=160, corner_radius=15, command=export_to_csv)
exportButton.grid(row=0, column=5, pady=5, padx=10)
treeview_data()
window.mainloop()




