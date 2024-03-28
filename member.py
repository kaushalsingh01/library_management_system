import mysql.connector as mycon
from prettytable import PrettyTable


def get_database_connection():
    return mycon.connect(
        host="localhost", username="root", password="", database="library"
    )


def add_member():
    try:
        print("#" * 40)
        print("== Enter details of member ==")
        name = input("Enter name of member: ")
        email = input("Enter email of member: ")
        address = input("Enter address of member: ")
        ph_num = input("Enter phone number of member: ")

        query = "insert into member (member_id, name, email, address, phone_number) values (%s,%s, %s, %s, %s)"
        val = (None, name, email, address, ph_num)

        db = get_database_connection()
        cur = db.cursor()
        cur.execute(query, val)
        db.commit()
        return "Member Added Successfully!!"

    except mycon.Error as e:
        print("Error:", e)
        return "Failed to add member."

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()


def remove_member():
    try:
        print("#" * 40)
        id = int(input("Enter ID of member: "))
        query = "delete from member where member_id = %s"
        val = (id,)

        db = get_database_connection()
        cur = db.cursor()
        cur.execute(query, val)
        db.commit()
        return "Member Removed Successfully!!"

    except mycon.Error as e:
        print("Error:", e)
        return "Failed to remove member."

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()


def update_member():
    try:
        print("#" * 40)
        id = int(input("Enter id of member: "))
        query = "Select * From member where member_id = %s"
        val = (id,)

        db = get_database_connection()
        cur = db.cursor()
        cur.execute(query, val)
        result = cur.fetchall()

        if result:
            for row in result:
                print(
                    f"\nMember Id = {row[0]}\n Member Name = {row[1]}\n Member Email = {row[2]}\n"
                )
                ans = input("Is this the member you want to update? Type 'y': ").lower()
                if ans == "y":
                    while True:
                        print(
                            "What do you want to update?\n 1. Member Name\n 2. Member Email\n 3. Member Address\n 4. Member Phone No.\n 5. Exit"
                        )
                        choice = int(input("Choose from options: "))

                        if choice == 1:
                            m_name = input("Enter member name: ")
                            query = "update member set name = %s where member_id = %s"
                            val = (m_name, id)
                            cur.execute(query, val)
                            db.commit()
                        elif choice == 2:
                            m_email = input("Enter member email: ")
                            query = "update member set email = %s where member_id = %s"
                            val = (m_email, id)
                            cur.execute(query, val)
                            db.commit()
                        elif choice == 3:
                            m_add = input("Enter member address: ")
                            query = (
                                "update member set address = %s where member_id = %s"
                            )
                            val = (m_add, id)
                            cur.execute(query, val)
                            db.commit()
                        elif choice == 4:
                            ph_no = input("Enter member phone no.: ")
                            query = "update member set phone_number = %s where member_id = %s"
                            val = (ph_no, id)
                            cur.execute(query, val)
                            db.commit()
                        elif choice == 5:
                            break
                        else:
                            print("Please choose a correct option!! (1-5)")
        else:
            print("No members found against the provided member id.")
            update_member()

        return "Member's Details Updated Successfully"

    except mycon.Error as e:
        print("Error:", e)
        return "Failed to update member details."

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()


def show_members():
    try:
        db = get_database_connection()
        cur = db.cursor()
        query = "SELECT * FROM member"
        cur.execute(query)
        members_data = cur.fetchall()

        if not members_data:
            return "No members found in the database."
        table = PrettyTable()
        table.field_names = [
            "Member ID",
            "Name",
            "Email",
            "Address",
            "Phone number",
        ]
        for member in members_data:
            table.add_row(member)
        return str(table)
    except mycon.Error as e:
        print("Error:", e)
        return "Failed to fetch members."

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()
