Mobile Shopping Management System

Project Overview

Mobile Shopping Management System is a web based application developed for managing a mobile shopping business.

The system is developed using Python Flask for the backend, HTML and CSS for the frontend, and Oracle Database 19c for database management.

The system provides management features for users, customers, employees, products, stock, and orders.


Project Objectives

Manage mobile phone products

Manage customers

Manage employees

Manage system users

Manage product stock

Manage customer orders

Provide a secure login system

Implement user roles and permissions

Connect Flask with Oracle Database

Provide a simple and user friendly management system


Technologies Used

Frontend

HTML5
CSS3
JavaScript

Backend

Python
Flask

Database

Oracle Database 19c

Development Tools

Visual Studio Code
Oracle SQL Developer
Git
GitHub


Main Modules

Login

Dashboard

Users

Customers

Employees

Products

Stock

Orders

Order Items


Login System

The login system allows registered users to access the application.

The login system uses username, password, and user role.

Supported user roles are:

ADMIN

EMPLOYEE

CUSTOMER


Dashboard

After successful login, the user is redirected to the dashboard.

The dashboard provides access to the main system modules.

Main modules include users, customers, employees, products, stock, and orders.


User Management

The Users module manages system user accounts.

User information includes:

User ID
Username
Password
User Role

Main operations include inserting, viewing, updating, deleting, and searching users.


Customer Management

The Customer module manages customer information.

Customer information includes:

Customer ID
User ID
Customer Name
Phone
Address

Main operations include inserting, viewing, updating, deleting, and searching customers.


Employee Management

The Employee module manages employee information.

Employee information includes:

Employee ID
Employee Name
Phone

Main operations include inserting, viewing, updating, deleting, and searching employees.


Product Management

The Product module manages mobile phone products.

Product information includes:

Product ID
User ID
Product Name
Color
Model
Price

Main operations include inserting, viewing, updating, deleting, and searching products.


Stock Management

The Stock module manages available product quantities.

Stock management allows the system to:

Add stock
View stock
Update stock
Delete stock
Check product availability


Order Management

The Order module manages customer orders.

Order information includes:

Order ID
Customer ID
Order Date
Status
Total

Order statuses include:

PENDING
CONFIRMED
SHIPPED
DELIVERED
CANCELLED


Order Items

The Order Items module stores products included in an order.

Order item information includes:

Order ID
Product ID
Quantity
Unit Price
Line Total

Line Total is calculated from quantity and unit price.


Database

The project uses Oracle Database 19c.

Main database tables are:

USERS
CUSTOMER
EMPLOYEE
PRODUCTS
STOCK
CUSTOMER_ORDERS
ORDER_ITEMS


Database Relationships

USERS is connected with CUSTOMER, EMPLOYEE, and PRODUCTS.

CUSTOMER is connected with CUSTOMER_ORDERS.

CUSTOMER_ORDERS is connected with ORDER_ITEMS.

ORDER_ITEMS is connected with PRODUCTS.

PRODUCTS is connected with STOCK.

The database uses primary keys, foreign keys, NOT NULL constraints, CHECK constraints, and UNIQUE constraints.


System Architecture

Frontend

HTML
CSS
JavaScript

Backend

Python
Flask

Database

Oracle Database 19c


Project Structure

Mobile Shopping Project

app.py
db1.py
requirements.txt
README.md

templates

login.html
dashboard.html
products.html
customers.html
employees.html
users.html
stock.html

static

css
style.css

js
script.js

database

database.sql


Requirements

Python 3.x

Flask

Oracle Database 19c

Oracle Python Driver

Visual Studio Code

Oracle SQL Developer


Installation

Install Python.

Open the project folder in Visual Studio Code.

Open the VS Code terminal.

Install Flask using the following command:

pip install flask

Install the Oracle Python Driver using:

pip install oracledb


Oracle Database Configuration

Make sure Oracle Database 19c is installed and running.

The application requires an Oracle username, password, host, port, and service name.

The database connection is configured in the Python database file.

Do not publish real database passwords or credentials to GitHub.


Running the Project

Open the project folder in Visual Studio Code.

Run the application using:

python app.py

The Flask application will run on the local computer.

Open the application in a web browser using:

http://127.0.0.1:5000


Security

The project includes basic security features.

User authentication

User roles

Role based permissions

Database constraints

Parameterized SQL queries

Controlled database operations

Passwords should not be stored as plain text in a production application.

A production version should use secure password hashing.


SQL Injection Protection

The project uses parameterized SQL queries to help protect the application from SQL injection.

Example query:

cursor.execute("""
    SELECT USER_ID, USERNAME, PASSWORD, USER_ROLE
    FROM USERS
    WHERE USERNAME = :username
""", {
    "username": username
})


Testing

Login testing

User testing

Customer testing

Employee testing

Product testing

Stock testing

Order testing


Project Workflow

Customer

Login

Select Product

Create Order

Add Order Items

Calculate Total

Confirm Order

Update Stock

Complete Order


Project Advantages

Centralized data management

Easy product management

Easy customer management

Easy employee management

Stock management

Order management

User authentication

Role based access

Oracle database integration

Web based interface


Future Improvements

Product image management

Product categories

Advanced product search

Shopping cart

Online payment

Invoice generation

Sales reports

Stock alerts

Customer order history

Password hashing

Email notifications

Advanced role permissions

Responsive mobile interface


Project Status

Development in progress.

Current implemented modules include:

Oracle Database

Database Tables

Database Relationships

Flask Backend

Login System

Dashboard

User Management

Customer Management

Employee Management

Product Management

Stock Management


Author

Mobile Shopping Management System

Developed as a Software Engineering project.

Technologies used:

Python Flask

Oracle Database 19c

HTML

CSS

JavaScript


License

This project is developed for educational and academic purposes.
