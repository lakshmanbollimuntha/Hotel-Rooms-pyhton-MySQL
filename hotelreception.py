import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Gju4kbkwy3",
    "database": "reception"
}

def av_room(cursor):
    select_query = "SELECT roomno AS available_rooms FROM rooms AS t1 LEFT JOIN availablerooms AS t2 ON t1.roomno = t2.roomnum WHERE checkout <= CURDATE() OR name IS NULL"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def Book_room(cursor, connection):
    a = int(input("Enter Room Number: "))
    b = input("Enter Customer Name: ")
    c = int(input("Enter Contact Number: "))
    d = input("Enter Address: ")
    e = input("Enter CheckIn Date (YYYY-MM-DD): ")
    insert_query1 = "INSERT INTO availablerooms (roomnum, name, phno, address, checkin) VALUES (%s, %s, %s, %s, %s)"
    data = (a, b, c, d, e)
    cursor.execute(insert_query1, data)
    insert_query2 = "INSERT INTO logbook (room, name, phno, address, checkin) VALUES (%s, %s, %s, %s, %s)"
    data = (a, b, c, d, e)
    cursor.execute(insert_query2, data)
    connection.commit()
    print("Booking Confirmed👌")

def find_checkin(cursor, connection):
    indate = input("Enter Checkin Date (YYYY-MM-DD): ")
    select_query = "SELECT name FROM logbook WHERE checkin = %s"
    cursor.execute(select_query, (indate,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def find_checkout(cursor, connection):
    outdate = input("Enter Checkout Date (YYYY-MM-DD): ")
    select_query = "SELECT name FROM logbook WHERE checkout = %s"
    cursor.execute(select_query, (outdate,))
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def vacating(cursor, connection):
    checkoutdate = input("Enter Checkout Date (YYYY-MM-DD): ")
    roomnum = input("Enter the vacating room No: ")
    name=input("Enter Name of vacating person: ")
    update_query = "UPDATE logbook SET checkout = %s WHERE room = %s and name = %s"
    cursor.execute(update_query, (checkoutdate, roomnum,name))
    connection.commit()
    delete_query = "DELETE FROM availablerooms where roomnum = %s and name = %s"
    cursor.execute(delete_query, (roomnum,name))
    connection.commit()
    print("Vacating updated Successfully ❤️")

def main():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    while True:
        print("\nHotel Room Management")
        print("1. Available Rooms")
        print("2. Book a Room")
        print("3. Find Data")
        print("4. Vacating Info")

        choice = input("Enter your choice: ")

        if choice == "1":
            av_room(cursor)
        elif choice == "2":
            Book_room(cursor, connection)
        elif choice == "3":
            print("1. Checkin")
            print("2. Checkout")
            op = input("Select any parameter: ")
            if op == "1":
                find_checkin(cursor, connection)
            elif op == "2":
                find_checkout(cursor, connection)
            else:
                print("Invalid option...")
        elif choice == "4":
            vacating(cursor, connection)
        else:
            print("Invalid choice. Please enter a valid option.")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    main()
