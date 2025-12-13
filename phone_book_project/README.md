 Address Book with PostgreSQL

Overview
PostSal is a command-line address book application that stores contacts in a PostgreSQL database. It supports adding, loading (viewing), searching, and deleting contacts. The interface is interactive and relies on Python to communicate with a PostgreSQL backend.

Tech stack

Python 3.x
PostgreSQL
psycopg2 (PostgreSQL adapter for Python)
Database schema (as used in your code)

Table: phone_book
id SERIAL PRIMARY KEY
contact_name VARCHAR(100) NOT NULL
contact_phone VARCHAR(100) NOT NULL
email VARCHAR(100) -- optional
note TEXT -- optional
address TEXT -- optional
Key features

Add new contact
Search contact by name or phone
Delete contact by name or phone
Load/view contact by name or phone
Persisted storage in PostgreSQL database
Getting started

Prerequisites

PostgreSQL installed and running
Python 3.x installed
Database setup

Create the database (as in your connection string):

Database: phone_book_project
User: postgres
Password: your_password
Host: localhost
Port: 5432
Create the table (SQL):
CREATE TABLE phone_book (
id SERIAL PRIMARY KEY,
contact_name VARCHAR(100) NOT NULL,
contact_phone VARCHAR(100) NOT NULL,
email VARCHAR(100),
note TEXT,
address TEXT
);

Install dependencies (see requirements.txt).

Run the program

python your_script.py
The CLI will prompt you with options:
adding contact
loading contact for dialing
deleting contact
searching contact
Usage examples

Add contact
enter the name: John Doe
enter the phone number: +1-555-0100
enter email(optional if do not want to enter anything just press enter): john@example.com
enter address(optional if do not want to enter anything just press enter): 123 Main St
enter note(optional if do not want to enter anything just press enter):

Search contact
please enter your desired procedure: 1)search by name 2)search by number
enter the name: John Doe
or
enter the phone number: +1-555-0100

Delete contact
please enter your desired procedure: 1)delete by name 2)delete by number
enter the name: John Doe
or
enter the phone number: +1-555-0100

Load contact
please enter your desired procedure: 1)load by name 2)load by number
enter the name: John Doe
or
enter the phone number: +1-555-0100

Notes and troubleshooting

Ensure the PostgreSQL server is running and accessible with the given credentials.
The code uses parameterized queries to prevent SQL injection.
If you encounter a “psycopg2.OperationalError,” check your database connection details.
If you see syntax errors, verify that your Python code is properly indented and that the quotes in SQL strings are balanced.