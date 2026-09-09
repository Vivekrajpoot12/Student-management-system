import tkinter as tk
from tkinter import ttk, messagebox
import pymysql

# ================== WINDOW ==================
win = tk.Tk()
win.geometry("1350x700+0+0")
win.title("Student Management System")
win.configure(bg="light green")

title_label = tk.Label(win, text="Student Management System",
                       font=("Arial", 30, "bold"),
                       bd=12, relief=tk.GROOVE,
                       bg="sky blue")
title_label.pack(side=tk.TOP, fill=tk.X)

# ================== FRAMES ==================
detail_frame = tk.LabelFrame(win, text="Enter Details",
                             font=("Arial", 20),
                             bd=12, relief=tk.GROOVE)
detail_frame.place(x=20, y=90, width=420, height=575)

data_frame = tk.Frame(win, bd=12, bg="lightgrey", relief=tk.GROOVE)
data_frame.place(x=475, y=90, width=810, height=575)

# ================== VARIABLES ==================
rollno = tk.StringVar()
name = tk.StringVar()
student_class = tk.StringVar()
section = tk.StringVar()
contact = tk.StringVar()
father_name = tk.StringVar()
address = tk.StringVar()
gender = tk.StringVar()
dob = tk.StringVar()

# ================== FUNCTIONS ==================

def fetch_data():
    con = pymysql.connect(host="localhost", user="root", password="", database="sms1")
    cur = con.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()

    if rows:
        student_table.delete(*student_table.get_children())
        for row in rows:
            student_table.insert('', tk.END, values=row)
    con.close()


def add_func():
    if rollno.get() == "" or name.get() == "" or student_class.get() == "":
        messagebox.showerror("Error", "Please fill required fields")
    else:
        con = pymysql.connect(host="localhost", user="root", password="", database="sms1")
        cur = con.cursor()
        cur.execute("INSERT INTO student VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (rollno.get(), name.get(), student_class.get(), section.get(),
                     contact.get(), father_name.get(), address.get(),
                     gender.get(), dob.get()))
        con.commit()
        con.close()
        fetch_data()
        clear()


def get_cursor(event):
    cursor_row = student_table.focus()
    content = student_table.item(cursor_row)
    row = content['values']

    if row:
        rollno.set(row[0])
        name.set(row[1])
        student_class.set(row[2])
        section.set(row[3])
        contact.set(row[4])
        father_name.set(row[5])
        address.set(row[6])
        gender.set(row[7])
        dob.set(row[8])


def clear():
    rollno.set("")
    name.set("")
    student_class.set("")
    section.set("")
    contact.set("")
    father_name.set("")
    address.set("")
    gender.set("")
    dob.set("")


def update_func():
    con = pymysql.connect(host="localhost", user="root", password="", database="sms1")
    cur = con.cursor()
    cur.execute("""UPDATE student SET 
                name=%s, student_class=%s, section=%s, contact=%s,
                father_name=%s, address=%s, gender=%s, dob=%s 
                WHERE roll_no=%s""",
                (name.get(), student_class.get(), section.get(), contact.get(),
                 father_name.get(), address.get(), gender.get(),
                 dob.get(), rollno.get()))
    con.commit()
    con.close()
    fetch_data()
    clear()


def delete_func():
    con = pymysql.connect(host="localhost", user="root", password="", database="sms1")
    cur = con.cursor()
    cur.execute("DELETE FROM student WHERE roll_no=%s", rollno.get())
    con.commit()
    con.close()
    fetch_data()
    clear()


# ================== ENTRY FIELDS ==================

labels = ["Roll No", "Name", "Class", "Section", "Contact",
          "Father Name", "Address", "Gender", "DOB"]

vars_list = [rollno, name, student_class, section, contact,
             father_name, address, gender, dob]

for i in range(len(labels)):
    tk.Label(detail_frame, text=labels[i], font=("Arial", 14)).grid(row=i, column=0, padx=5, pady=5)

    if labels[i] == "Gender":
        ttk.Combobox(detail_frame, textvariable=gender,
                     values=("Male", "Female", "Other"),
                     state="readonly").grid(row=i, column=1)
    else:
        tk.Entry(detail_frame, textvariable=vars_list[i]).grid(row=i, column=1)


# ================== BUTTONS ==================
btn_frame = tk.Frame(detail_frame, bd=10, relief=tk.GROOVE)
btn_frame.place(x=10, y=400, width=360)

tk.Button(btn_frame, text="Add", width=15, command=add_func).grid(row=0, column=0)
tk.Button(btn_frame, text="Update", width=15, command=update_func).grid(row=0, column=1)
tk.Button(btn_frame, text="Delete", width=15, command=delete_func).grid(row=1, column=0)
tk.Button(btn_frame, text="Clear", width=15, command=clear).grid(row=1, column=1)

# ================== TABLE ==================
main_frame = tk.Frame(data_frame, bd=11, relief=tk.GROOVE)
main_frame.pack(fill=tk.BOTH, expand=True)

scroll_y = tk.Scrollbar(main_frame, orient=tk.VERTICAL)
scroll_x = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL)

student_table = ttk.Treeview(main_frame,
                             columns=("rollno", "name", "class", "section", "contact",
                                      "father_name", "address", "gender", "dob"),
                             yscrollcommand=scroll_y.set,
                             xscrollcommand=scroll_x.set)

scroll_y.config(command=student_table.yview)
scroll_x.config(command=student_table.xview)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

for col in ("rollno", "name", "class", "section", "contact",
            "father_name", "address", "gender", "dob"):
    student_table.heading(col, text=col.upper())
    student_table.column(col, width=100)

student_table['show'] = "headings"
student_table.pack(fill=tk.BOTH, expand=True)

student_table.bind("<ButtonRelease-1>", get_cursor)

fetch_data()

win.mainloop()