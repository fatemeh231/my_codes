"""
Created on Wed Sep 24 20:02:16 2025
@author: fatemeh
"""
#creating address book(add,search,load,delete) and saving into database of postsal
import psycopg2
conn = psycopg2.connect(
        dbname="phone_book_project",
        user="postgres",
        password="asal1234@",
        host="localhost",
        port="5432"
    )
cur = conn.cursor()
def add_contact():
    name=input("enter the name: ")
    phone=input("enter the phone number:")
    email=input("enter email(optional if do not want to enter anything just press enter): ")
    address=input("enter address(optional if do not want to enter anything just press enter): ")
    note=input("enter note(optional if do not want to enter anything just press enter): ")
    cur.execute("""
        INSERT 
            INTO phone_book (contact_name, contact_phone, email, address, note)
            VALUES (%s, %s, %s, %s, %s)
    """,(name, phone, email, address, note))
    conn.commit()
    cur.close()
    conn.close()
    print("contact added")
def search_contact():
    searching=int(input("please enter your desired procedure: 1)search by name 2)search by number "))
    match searching:
        case 1:
            search_name = input("enter the name: ")
            cur.execute("""SELECT * 
                            FROM 
                                phone_book 
                            WHERE 
                                contact_name = %s""", (search_name,))
        case 2:
            search_phone = input("enter the phone number: ")
            cur.execute(""""SELECT * 
                            FROM 
                                phone_book 
                            WHERE 
                                contact_phone = %s""", (search_phone,))
    result = cur.fetchall()
    for row in result:
        print(row)
    cur.close()
    conn.close()

def delete_conatct():
    deleting=int(input("please enter your desired procedure: 1)delete by name 2)delete by number "))
    match deleting:
        case 1:
            delete_name = input("enter the name: ")
            cur.execute("""DELETE FROM phone_book 
                            WHERE 
                                contact_name = %s""", (delete_name,))
        case 2:
            delete_phone = input("enter the phone number: ")
            cur.execute("""DELETE FROM phone_book 
                           WHERE 
                               contact_phone = %s""", (delete_phone,))
    conn.commit()
    cur.close()
    conn.close()
    print("contact deleted")

def load_contact():
    load=int(input("please enter your desired procedure: 1)load by name 2)load by number "))
    match load:
        case 1:
            load_name = input("enter the name: ")
            cur.execute("""SELECT * 
                            FROM 
                                phone_book 
                            WHERE 
                                contact_name = %s""",(load_name,))
        case 2:
            load_phone = input("enter the phone number: ")
            cur.execute(""""SELECT * 
                            FROM 
                                phone_book 
                            WHERE 
                                contact_phone = %s""",(load_phone,))
    result=cur.fetchall()
    for row in result:
        print(row)
    cur.close()
    conn.close()

phone_book=int(input("please enter your desired procedure: 1)adding contact 2)loading contact for dialing 3)deleting contact 4)searching contact"))
match phone_book:
    case 1:
         add_contact()
    case 2:
         search_contact()
    case 3: 
        delete_conatct()
    case 4: 
        load_contact()