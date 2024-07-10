#import necessary modules 
from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import re
from PIL import ImageTk, Image

import datetime
import sqlite3
from tkcalendar import DateEntry
import tkinter as tk
from tkinter import simpledialog
import tkinter.messagebox as mb
import tkinter.ttk as ttk
import matplotlib.pyplot as plt
from tkinter import filedialog
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PIL import ImageTk, Image
import pandas as pd


# Create a Tkinter window
root = Tk()
root.title("Python: Expense Tracker")
width = 740
height = 650
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

#defining the variables
USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()
PHONENUMBER = StringVar()
EMAIL = StringVar()

#creating a connection to the database
def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `users` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT,phonenumber NUMBER, email TEXT)")

# Regular expression pattern for phone number validation
PHONE= r'^\+?\d{1,3}[-. ]?\d{3}[-. ]?\d{3}[-. ]?\d{4}$'

# Regular expression pattern for email validation
MAIL = r'^\w+[\w\.\-]*@[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$'

#creating a function to validate the phone number
phone_number = PHONENUMBER.get()
def validate_phone_number(phone_number):
    """Validates a phone number using regular expression"""
    return bool(re.match(PHONE, phone_number))

#creating a function to validate the email
mail_id =EMAIL.get()
def validate_email(mail_id):
    """Validates an email address using regular expression"""
    return bool(re.match(MAIL, mail_id))

#creating a function to validate the password
def validate_password(password):
    """Validates a password by checking if it has a minimum length of 4 characters"""
    return len(password) >= 4

#creating a exit function
def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
root.protocol("WM_DELETE_WINDOW", Exit)


#login form functions
#options shown in the login form
def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.configure(bg='#32E4C0')
    LoginFrame.pack(side=TOP, pady=80)

    lbl_username = Label(LoginFrame, text="Username:",bg='#32E4C0', font=('arial', 25),fg='black', bd=18)
    lbl_username.grid(row=1)

    lbl_password = Label(LoginFrame, text="Password:",bg='#32E4C0', font=('arial', 25),fg='black', bd=18)
    lbl_password.grid(row=2)

    lbl_result1 = Label(LoginFrame, text="",bg='#32E4C0', font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)

    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15,bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    username.grid(row=1, column=1)

    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*",bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    password.grid(row=2, column=1)

    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=30,fg='green',bg='black', highlightbackground="red", highlightthickness=2,borderwidth=5,command=Login)
    btn_login.grid(row=4, columnspan=2, pady=15)

    btn_login = Button(LoginFrame, text="Exit", font=('arial', 18), width=30,fg='green',bg='black' ,borderwidth=5, command=Exit)
    btn_login.grid(row=6, columnspan=2, pady=15)

    lbl_register = Label(LoginFrame, text="Register", fg="green",bg='black' ,borderwidth=5, font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)

#register form functions
#options shown in registration form
def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.configure(bg='#32E4C0')
    RegisterFrame.pack(side=TOP, pady=40)
    
    lbl_username = Label(RegisterFrame, text="Username:",bg='#32E4C0', font=('arial', 18),fg='black', bd=18)
    lbl_username.grid(row=1)
    
    lbl_password = Label(RegisterFrame, text="Password:",bg='#32E4C0', font=('arial', 18),fg='black', bd=18)
    lbl_password.grid(row=4)
    
    lbl_firstname = Label(RegisterFrame, text="Firstname:", bg='#32E4C0',font=('arial', 18),fg='black', bd=18)
    lbl_firstname.grid(row=2)
    
    lbl_lastname = Label(RegisterFrame, text="Lastname:",bg='#32E4C0', font=('arial', 18),fg='black', bd=18)
    lbl_lastname.grid(row=3)
    
    lbl_phone = Label(RegisterFrame, text="Phone Number with code:",bg='#32E4C0', font=('arial', 18),fg='black', bd=18)
    lbl_phone.grid(row=5)
    
    lbl_email = Label(RegisterFrame, text="Email:",bg='#32E4C0', font=('arial', 18),fg='black', bd=18)
    lbl_email.grid(row=6)
    
    lbl_result2 = Label(RegisterFrame, text="", bg='#32E4C0',font=('arial', 18))
    lbl_result2.grid(row=7, columnspan=2)
    
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=14,bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    username.grid(row=1, column=1)
    
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=14,bd=2, relief='solid', highlightthickness=1, highlightbackground='black' )
    password.grid(row=2, column=1)
    
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=14,bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    firstname.grid(row=3, column=1)
    
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=14, show="*",bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    lastname.grid(row=4, column=1)
    
    phone = Entry(RegisterFrame, font=('arial', 20), textvariable=PHONENUMBER, width=14,bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    phone.grid(row=5, column=1)
    
    email = Entry(RegisterFrame, font=('arial', 20), textvariable=EMAIL, width=15, bd=2, relief='solid', highlightthickness=1, highlightbackground='black')
    email.grid(row=6, column=1)

    
    btn_login = Button(RegisterFrame, text="Register", fg="green",bg='black' ,borderwidth=5, font=('arial', 18), width=30, command=Register)
    btn_login.grid(row=8, columnspan=2, pady=20)
    
    lbl_login = Label(RegisterFrame, text="Login", fg="green",bg='black' ,borderwidth=5, font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)

#defining functions for the toggle operation
def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()

def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()

#register form validation
def Register():
    Database()
    if USERNAME.get() == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get() == "" or PHONENUMBER.get() == "" or EMAIL.get() == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange") 
    elif not validate_phone_number(PHONENUMBER.get()):
        lbl_result2.config(text="Invalid phone number", fg="red")
    elif not validate_email(EMAIL.get()):
        lbl_result2.config(text="Invalid email address", fg="red")
    elif not validate_password(PASSWORD.get()):
        lbl_result2.config(text="Password should have a minimum length of 4 characters", fg="red")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `users` (username, password, firstname, lastname, phonenumber, email) VALUES(?, ?, ?, ?, ?, ?)", (str(USERNAME.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get()), str(PHONENUMBER.get()), str(EMAIL.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            PHONENUMBER.set("")
            EMAIL.set("")
            lbl_result2.config(text="Successfully Created!", fg='green')
        cursor.close()
        conn.close()

#login form validation
def Login():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `users` WHERE `username` = ? and `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            lbl_result1.config(text="You Successfully Login", fg="green")
            root.after(2000, root.destroy)

        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")
LoginForm()

root.mainloop()

#main window functions
# Initializing the GUI window
root = Tk()
root.title('EXPENSE TRACKER USING PYHON')
# Maximize the window
root.state('zoomed')


Label(root, text='Python-Based EXPENSE TRACKING System for Personal Finance Management', font=('Noto Sans CJK TC', 19, 'bold','underline'), bg='#1F2833',fg='gold').pack(side=TOP, fill=X)

# Connecting to the Database
connector = sqlite3.connect("Expense Tracker.db")
cursor = connector.cursor()

connector.execute(
	'CREATE TABLE IF NOT EXISTS ExpenseTracker (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, Date DATETIME, Payee TEXT, Description TEXT, Amount FLOAT, ModeOfPayment TEXT,Categories TEXT)'
)
connector.commit()

# Backgrounds anf Fonts for main window
dataentry_frame_bg = '#1F2833'
buttons_frame_bg ='#1F2833'
hlb_btn_bg = '#1F2833'

lbl_font = ('Georgia bold', 11)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT bold', 11)

font_color ='#45A29E'
label_font_color = '#45A29E'

# Frames
data_entry_frame = Frame(root,bg=dataentry_frame_bg)
data_entry_frame.place(x=0, y=35, relheight=0.95, relwidth=0.25)

buttons_frame = Frame(root, bg=buttons_frame_bg)
buttons_frame.place(x=340, y=35, relwidth=0.75, relheight=0.15)

tree_frame = Frame(root, bg=buttons_frame_bg)
tree_frame.place(relx=0.25, rely=0.20, relwidth=0.75, relheight=0.6)

sort_frame = Frame(root, bg=buttons_frame_bg)
sort_frame.place(relx=0.25, rely=0.80, relwidth=0.75, relheight=0.30)


# Treeview Frame
table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment','Categories'))

# Customize the style of the Treeview widget
style = ttk.Style()
style.configure('Treeview', background='#D3D3D3', foreground='black', rowheight=25, fieldbackground='#D3D3D3')
style.configure('Treeview.Heading', font=('Arial', 10, 'bold'))
style.map("Treeview", background=[("selected", 'green')])
X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)

table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

table.heading('ID', text='S No.(ID)', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)
table.heading('Categories', text='Categories', anchor=CENTER)


table.column('#0', width=0, stretch=NO)
table.column('#1', width=70, stretch=NO)   #s.no column
table.column('#2', width=110, stretch=NO)  # Date column
table.column('#3', width=140, stretch=NO)  # Payee column
table.column('#4', width=255, stretch=NO)  # Title column
table.column('#5', width=130, stretch=NO)  # Descripton column
table.column('#6', width=160, stretch=NO)  # Mode of Payment column
table.column('#7', width=170, stretch=NO)  # Categories column


# populate the table with data from the database
conn = sqlite3.connect('Expense Tracker.db')
c = conn.cursor()
c.execute('SELECT * FROM ExpenseTracker')
for row in c.fetchall():
    table.insert("", "end", values=row)
conn.close()

#table functions
def filter_table():
    global filter_text
    filter_text = filter_entry.get().lower()  # Convert the filter text to lowercase
    match = False  # Flag to check if there is a match
    for row in table.get_children():
        values = [str(val).lower() for val in table.item(row)['values']]  # Convert the table values to lowercase
        if filter_text in values:
            table.item(row, tags=('highlight',))
	    	# Set the flag to True if there is a match
            match = True  
        else:
            table.item(row, tags=())
    if not match:
		# Show an error message if there is no match
        mb.showerror("No matching records found", "Please check the spelling or value to search", icon="warning")  	
	    	
    table.tag_configure('highlight', background='red', foreground='black', font='TkDefaultFont 10 bold')

filter_entry = Entry(buttons_frame)
filter_entry.config(font=('BebasNeue', 15),width=15)
filter_entry.place(x=255,y=7)
Button(buttons_frame, text='Filter',command=filter_table, font=btn_font, width=8,fg=font_color ,bg=hlb_btn_bg).place(x=445, y=5)
table.place(relx=0, y=0, relheight=1, relwidth=1)

# Functions in button frame
def list_all_expenses():
	global connector, table

	table.delete(*table.get_children())

	all_data = connector.execute('SELECT * FROM ExpenseTracker')
	data = all_data.fetchall()

	for values in data:
		table.insert('', END, values=values)


def view_expense_details():
	global table
	global date, payee, desc, amnt, MoP,CaT

	if not table.selection():
		mb.showerror('No expense selected', 'Please select an expense from the table to view its details')

	current_selected_expense = table.item(table.focus())
	values = current_selected_expense['values']

	expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))

	date.set_date(expenditure_date) ; payee.set(values[2]) ; desc.set(values[3]) ; amnt.set(values[4]) ; MoP.set(values[5]); CaT.set(values[6])


def clear_fields():
	global desc, payee, amnt, MoP, date, table,CaT

	today_date = datetime.datetime.now().date()

	desc.set('') ; payee.set('') ; amnt.set('') ; MoP.set('Cash');CaT.set('Food'), date.set_date(today_date)
	table.selection_remove(*table.selection())


def remove_expense():
	if not table.selection():
		mb.showerror('No record selected!', 'Please select a record to delete!')
		return

	current_selected_expense = table.item(table.focus())
	values_selected = current_selected_expense['values']

	surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

	if surety:
		connector.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
		connector.commit()

		list_all_expenses()
		mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')


def remove_all_expenses():
	surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')

	if surety:
		table.delete(*table.get_children())

		connector.execute('DELETE FROM ExpenseTracker')
		connector.commit()

		clear_fields()
		list_all_expenses()
		mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
	else:
		mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')


def add_another_expense():
	global date, payee, desc, amnt, MoP ,CaT
	global connector

	if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get() or not CaT.get():
		mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
		amnt = StringVar()
		mb.showerror('Error!', "Please enter a valid amount.!")
	else:
		connector.execute(
		'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment, Categories) VALUES (?, ?, ?, ?, ?, ?)',
		(date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(),CaT.get())
		)
		connector.commit()

		clear_fields()
		list_all_expenses()
		mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')



def edit_expense():
	global table

	def edit_existing_expense():
		global date, amnt, desc, payee, MoP,CaT
		global connector, table

		current_selected_expense = table.item(table.focus())
		contents = current_selected_expense['values']

		connector.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? ,Categories = ?  WHERE ID = ?',
		                  (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(),CaT.get(), contents[0]))
		connector.commit()

		clear_fields()
		list_all_expenses()

		mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
		edit_btn.destroy()
		return

	if not table.selection():
		mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
		return

	view_expense_details()

	edit_btn = Button(data_entry_frame, text='Edit expense', font=btn_font, width=30,
	                  bg=hlb_btn_bg, command=edit_existing_expense)
	edit_btn.place(x=10, y=395)


def selected_expense_to_words():
	global table

	if not table.selection():
		mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
		return

	current_selected_expense = table.item(table.focus())
	values = current_selected_expense['values']

	message = f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'

	mb.showinfo('Here\'s how to read your expense', message)


def expense_to_words_before_adding():
	global date, desc, amnt, payee, MoP

	if not date or not desc or not amnt or not payee or not MoP:
		mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')

	message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {desc.get()} on {date.get_date()} via {MoP.get()}"'

	add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')

	if add_question:
		add_another_expense()
	else:
		mb.showinfo('Ok', 'Please take your time to add this record')

def Exit1():
    result = mb.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()
root.protocol("WM_DELETE_WINDOW", Exit1)

def download_data():
    # Connect to the database
    conn = sqlite3.connect('Expense Tracker.db')
    cursor = conn.cursor()

    # Retrieve the data from the database
    cursor.execute('SELECT * FROM ExpenseTracker')
    data = cursor.fetchall()
    
    # Create a PDF document
    filename = filedialog.asksaveasfilename(defaultextension='.pdf')
    pdf = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.alignment = 1
    table_style = TableStyle([
    	('BACKGROUND', (0, 0), (-1, 0), colors.black),
    	('TEXTCOLOR', (0, 0), (-1, 0), colors.green),
    	('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    	('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    	('FONTSIZE', (0, 0), (-1, 0), 14),
    	('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    	('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    	('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
    	('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    	('FONTSIZE', (0, 1), (-1, -1), 13),
    	('BOTTOMPADDING', (0, 1), (-1, -1), 6),
    	('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])
    elements = []

	# Create a table from the data
    table_data = [['ID', 'Date', 'Payee','Description','Amount','Mode of payment','Categories']]
    for row in data:
      table_data.append(list(row))
    table = Table(table_data)
    table.setStyle(table_style)
    elements.append(table)

    # Save the PDF document
    pdf.build(elements)

    
    # Close the database connection
    conn.close()


#functions in sort frame
# default sort order (None = unsorted, 'asc' = ascending, 'desc' = descending)
sort_order = None   

def sortby(column, descending):
    # connect to the database
    conn = sqlite3.connect('Expense Tracker.db')
    c = conn.cursor()
    
    # execute the query to sort the table
    if descending:
        query = "SELECT * FROM ExpenseTracker ORDER BY " + column + " DESC"
    else:
        query = "SELECT * FROM ExpenseTracker ORDER BY " + column + " ASC"
    c.execute(query)
    
    # clear the table
    for row in table.get_children():
        table.delete(row)
        
    # populate the table with the sorted data
    for row in c.fetchall():
        table.insert("", "end", values=row)
    
    # close the database connection
    conn.close()

def refreshTotal():
    cursor.execute("SELECT SUM(Amount) FROM ExpenseTracker")
    total = cursor.fetchone()[0]
    total_label.config(text=f"Total: {total}")

# Function to Update the budget with the total and show a message
def Update_budget():
    # Get the budget from the user
    budget_str = tk.simpledialog.askstring("Set Budget", "Enter your budget:")
    if budget_str is not None and budget_str.strip() != "":
        budget = float(budget_str)
    else:
        budget = 0.0

    # Update the budget with the total and show a message if it's above or below the total
    if budget is not None and budget >= total:
        message = f"Budget Okay,You have spent ₹({total})."
    elif budget == 0.0:
        message = f"Budget is Zero(₹0.0) ,Please enter your budget ."
    else:
        message = f"Budget Exceeded,You have spent ₹ ({total})."

    # Update the labels with the budget and message
    budget_label.config(text=f"Budget: ₹ {budget}")
    message_label.config(text=message)

# Define a function to show the histogram
def show_histogram():   
 # Connect to the SQLite database
   conn = sqlite3.connect('Expense Tracker.db')

 # Extract the data for the Categories and amount columns from the table
   df = pd.read_sql_query('SELECT Categories, amount FROM ExpenseTracker', conn)

 # Create a figure and an axis object
   fig, ax = plt.subplots()
   

 # Create the histogram
   ax.hist(df['Categories'], bins=10, color='green', alpha=0.5, edgecolor='black')

 # Customize the histogram
   ax.set_title('Expenses by Categories')
   ax.set_xlabel('Categories')
   ax.set_ylabel('Frequency')

 # Display the chart
   plt.show()

 # Close the database connection
   conn.close()

# Define a function to show the pie chart
def show_pie():
   # Connect to the SQLite database
   conn = sqlite3.connect('Expense Tracker.db')
   cur = conn.cursor()

   # Extract the data for the Categories and amount columns from the table
   cur.execute('SELECT Categories, SUM(amount) FROM ExpenseTracker GROUP BY Categories')
   data = cur.fetchall()
   Categories = [row for row in data]
   amounts = [row[1] for row in data]

   # Create a figure and an axis object
   fig, ax = plt.subplots()

   # Create the pie chart
   ax.pie(amounts, labels=Categories)

   # Customize the pie chart
   ax.set_title('Expenses by Categories')
   ax.legend(title='Categories', loc='best')

   # Display the chart
   plt.show()

   # Close the database connection
   conn.close()



# StringVar and DoubleVar variables
desc = StringVar()
amnt = DoubleVar(value='')
payee = StringVar()
MoP = StringVar(value='Cash')
CaT = StringVar(value='Food')



# Data Entry Frame
Label(data_entry_frame, text='Date (MM/DD/YY) :', font=lbl_font,bg=dataentry_frame_bg, fg=label_font_color).place(x=10, y=50)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(),bg='light blue', font=entry_font)
date.place(x=180, y=50)

Label(data_entry_frame, text='Payee\t             :', font=lbl_font, bg=dataentry_frame_bg,fg=label_font_color).place(x=10, y=230)
Entry(data_entry_frame,bg='light blue', font=entry_font, width=31, text=payee).place(x=10, y=260)

Label(data_entry_frame, text='Description           :', font=lbl_font, bg=dataentry_frame_bg,fg=label_font_color).place(x=10, y=100)
Entry(data_entry_frame, bg='light blue',font=entry_font, width=31, text=desc).place(x=10, y=130)

Label(data_entry_frame, text='Amount(in Rs(₹)):', font=lbl_font, bg=dataentry_frame_bg,fg=label_font_color).place(x=10, y=180)
Entry(data_entry_frame,bg='light blue', font=entry_font, width=14, text=amnt).place(x=160, y=180)


Label(data_entry_frame, text='Mode of Payment:', font=lbl_font, bg=dataentry_frame_bg,fg=label_font_color).place(x=10, y=310)
dd1 = OptionMenu(data_entry_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Phonepay'])
dd1.place(x=160, y=305)     ;     dd1.configure(width=10,bg='light blue', font=entry_font)
dd1["menu"].config(bg="light blue",font=entry_font)

Label(data_entry_frame, text='Categories:', font=lbl_font, bg=dataentry_frame_bg,fg=label_font_color).place(x=14, y=360)
dd2 = OptionMenu(data_entry_frame, CaT, *['Food', 'Education', 'Entertainment', 'Transport', 'Cloths', 'Others'])
dd2.place(x=160, y=355)     ;     dd2.configure(width=15,bg='light blue', font=entry_font)
dd2["menu"].config(bg="light blue",font=entry_font)

# Create a button to show the histogram
Button(data_entry_frame, text='Show pie',command=show_pie, font=btn_font, width=13,fg=font_color,
        bg=hlb_btn_bg).place(x=10,y=500)
Button(data_entry_frame, text='Show hist',command=show_histogram, font=btn_font, width=13,
       fg=font_color, bg=hlb_btn_bg).place(x=160,y=500)
# Create a button to hide the histogram and the pie chart
Button(data_entry_frame, text='Hide',command=plt.close, font=btn_font, width=15,
       fg=font_color ,bg=hlb_btn_bg).place(x=10,y=550)

Button(data_entry_frame, text='Add expense', command=add_another_expense, font=btn_font, width=30,
       bg=hlb_btn_bg,fg=font_color).place(x=10, y=395)

Button(data_entry_frame, text='Convert to words before adding',command=expense_to_words_before_adding, font=btn_font, width=30, bg=hlb_btn_bg,fg=font_color).place(x=10,y=450)

Button(data_entry_frame, text='Clear Fields in DataEntry Frame', font=btn_font, width=25, bg=hlb_btn_bg,fg=font_color,
       command=clear_fields).place(x=15,y=610)

# Buttons' Frame
Button(buttons_frame, text='Delete Expense', font=btn_font, width=22, bg=hlb_btn_bg, command=remove_expense,fg=font_color).place(x=30, y=5)

Button(buttons_frame, text='Delete All Expense', font=btn_font, width=25, bg=hlb_btn_bg, command=remove_all_expenses,fg=font_color).place(x=550, y=5)

Button(buttons_frame, text='View Selected Expense\'s Details', font=btn_font, width=25, bg=hlb_btn_bg,fg=font_color,
       command=view_expense_details).place(x=30, y=65)

Button(buttons_frame, text='Edit Selected Expense', command=edit_expense, font=btn_font, width=25, bg=hlb_btn_bg,fg=font_color).place(x=290,y=65)

Button(buttons_frame, text='Read Selected expense', font=btn_font, width=25, bg=hlb_btn_bg,fg=font_color,
       command=selected_expense_to_words).place(x=550, y=65)
Button(buttons_frame, text='Exit', font=btn_font, width=22, bg=hlb_btn_bg,fg=font_color,
       command=Exit).place(x=800, y=65)
Button(buttons_frame, text='Download data', font=btn_font, width=22, bg=hlb_btn_bg,fg=font_color,
       command=download_data).place(x=800, y=5)


#sort frame buttons
# add the filter buttons
Button(sort_frame, text=' ID Asc',  font=btn_font, bg=hlb_btn_bg,fg=font_color,command=lambda: sortby('ID', False)).place(x=5,y=5)
Button(sort_frame, text=' ID Desc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('ID', True)).place(x=5,y=50)
Button(sort_frame, text='Date Asc',  font=btn_font, bg=hlb_btn_bg,fg=font_color,command=lambda: sortby('Date', False)).place(x=75,y=5)
Button(sort_frame ,text='Date Desc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Date', True)).place(x=75,y=50)
Button(sort_frame, text='Payee Asc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Payee', False)).place(x=200,y=5)
Button(sort_frame, text='Payee Desc', font=btn_font, bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Payee', True)).place(x=200,y=50)
Button(sort_frame, text='Description Asc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Description', False)).place(x=400,y=5)
Button(sort_frame, text='Description Desc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Description', True)).place(x=400,y=50)
Button(sort_frame, text='Amount Asc', font=btn_font, bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Amount', False)).place(x=600,y=5)
Button(sort_frame, text='Amount Desc', font=btn_font, bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Amount', True)).place(x=600,y=50)
Button(sort_frame, text='Mode of Payment Asc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('ModeOfPayment', False)).place(x=720,y=5)
Button(sort_frame, text='Mode of Payment Desc', font=btn_font,  bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('ModeOfPayment', True)).place(x=720,y=50)
Button(sort_frame, text='Categories Asc', font=btn_font, bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Categories', False)).place(x=900,y=5)
Button(sort_frame, text='Categories Desc', font=btn_font, bg=hlb_btn_bg,fg=font_color, command=lambda: sortby('Categories', True)).place(x=900,y=50)


#create connection to the database
conn = sqlite3.connect("Expense Tracker.db")
cursor = conn.cursor()
# Fetch the initial total amount from the SQLite table
cursor.execute("SELECT SUM(Amount) FROM ExpenseTracker")
total = cursor.fetchone()[0]
# Create a label to display the total
total_label = tk.Label(sort_frame, text=f"Total: {total}", font='BebasNeue 15 bold ', bg='gold',fg='black')
total_label.place(x=20, y=95)

# Create a button to refresh the total amount
total_button = tk.Button(sort_frame, text="Refresh Total", font=btn_font, bg=hlb_btn_bg,fg=font_color, command=refreshTotal)
total_button.place(x=170, y=95)

# Create a button to Update the budget with the total
Update_button = tk.Button(sort_frame, text="Update Budget", font=btn_font, bg=hlb_btn_bg,fg=font_color, command=Update_budget)
Update_button.place(x=850, y=95)

# Create a label to display the budget
budget_label = tk.Label(sort_frame, text="Budget: Not Set.", font='BebasNeue 13 bold ', bg='light coral',fg='black')
budget_label.place(x=300, y=100)

# Create a label to display the message
message_label = tk.Label(sort_frame, text="Message: Set Your Budget", font='BebasNeue 13 bold ', bg='light coral',fg='black')
message_label.place(x=460, y=100)


# Finalizing the GUI window
root.update()
root.mainloop()