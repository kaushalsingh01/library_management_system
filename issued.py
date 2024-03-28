import mysql.connector as mycon
from prettytable import PrettyTable
from datetime import datetime, timedelta


def get_database_connection():
    return mycon.connect(
        host="localhost", username="root", password="", database="library"
    )


def issue_book():
    try:
        db = (
            get_database_connection()
        )  # Assuming you have a function to establish the database connection
        cur = db.cursor()

        print("#" * 40)
        m_id = int(input("Enter member Id of borrower: "))
        cur.execute("SELECT * FROM member WHERE member_id = %s", (m_id,))
        result_m = cur.fetchall()
        if not result_m:
            print("Member Id is not valid. Please check again.")
            return "Invalid Member ID"

        b_id = int(input("Enter book Id which is being borrowed: "))
        cur.execute("SELECT availability_status FROM book WHERE book_id = %s", (b_id,))
        status = cur.fetchone()
        if status and status[0] == 0:
            return "Book is not available"

        cur.execute("SELECT * FROM book WHERE book_id = %s", (b_id,))
        result_b = cur.fetchall()
        if not result_b:
            return "Book Id is not valid. Please check again."
        elif result_b[0][5] == False:  # Assuming the availability_status is at index 5
            return "Book is unavailable at the moment."

        issue_date = str(datetime.now().date())
        r_date = None
        ac_date = datetime.strptime(issue_date, "%Y-%m-%d") + timedelta(days=15)
        late_fee = 0.0

        query = "INSERT INTO issue (book_id, member_id, issue_date, return_date, actual_return_date, late_fee) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (b_id, m_id, issue_date, r_date, ac_date, late_fee)
        cur.execute(query, val)

        status_query = "UPDATE book SET availability_status = %s WHERE book_id = %s"
        b_val = (0, b_id)
        cur.execute(status_query, b_val)

        db.commit() 
        return "Book Issued Successfully"

    except mycon.Error as e:
        print("Error:", e)
        db.rollback() 

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()


def late_fee_calc(ac_date, r_date):
    days_late = (ac_date - r_date).days
    late_fee = max(0, days_late * 5)
    return late_fee


def return_book():
    try:
        db = get_database_connection()
        cur = db.cursor()

        print("#" * 40)
        i_id = int(input("Enter issue id : "))
        cur.execute("SELECT * FROM issue WHERE issue_id = %s", (i_id,))
        result_i = cur.fetchall()

        if not result_i:
            print("Issue id is invalid...\n Please check again...")
            return

        r_date = datetime.now().date()
        ac_date = result_i[0][5]
        late_fee = late_fee_calc(r_date, ac_date)

        print(f"You have to pay a late fee of Rs. {late_fee}")
        print("#" * 40)

        query = "UPDATE issue SET late_fee = %s, return_date = %s WHERE issue_id = %s"
        val = (late_fee, r_date, i_id)

        cur.execute(query, val)

        get_book = "SELECT book_id FROM issue WHERE issue_id = %s"
        cur.execute(get_book, (i_id,))
        b_id = cur.fetchone()[0]
        status_query = "UPDATE book SET availability_status = %s WHERE book_id = %s"
        cur.execute(status_query, (True, b_id))

        db.commit()
        
        return str("Book returned successfully!!")

    except mycon.Error as e:
        print("Error:", e)

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()


def extend_borrow():
    try:
        db = get_database_connection()
        cur = db.cursor()

        print("#" * 40)
        i_id = int(input("Enter issue id: "))
        cur.execute("SELECT * FROM issue WHERE issue_id = %s", (i_id,))
        result_i = cur.fetchall()

        if not result_i:
            print("Issue id is invalid...\n Please check again...")
            return

        ac_date = input("Enter extended date (yyyy-mm-dd): ")
        query = "UPDATE issue SET actual_return_date = %s WHERE issue_id = %s"
        val = (ac_date, i_id)
        cur.execute(query, val)
        db.commit()
        return("Date Extended Successfully!!")

    except mycon.Error as e:
        print("Error:", e)

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()


def show_issues():
    try:
        db = get_database_connection()
        cur = db.cursor()

        query = """
        SELECT * FROM issue
        """
        cur.execute(query)
        issue_data = cur.fetchall()

        if not issue_data:
            return "No books found in the library."

        table = PrettyTable()
        table.field_names = [
            "Issue ID",
            "Book ID",
            "Member ID",
            "Issue Date",
            "Return Date",
            "Actual Return Date",
            "Late Fee",
        ]

        for issue in issue_data:
            table.add_row(issue)

        return str(table)

    except mycon.Error as e:
        print("Error:", e)
        return "Error occurred while fetching book details."

    finally:
        if "cur" in locals():
            cur.close()
        if "db" in locals():
            db.close()
