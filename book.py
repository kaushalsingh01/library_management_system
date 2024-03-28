import mysql.connector as myconn
from prettytable import PrettyTable


def get_database_connection():
    return myconn.connect(
        host="localhost", username="root", password="", database="library"
    )


def add_book():
    try:
        con = get_database_connection()
        cur = con.cursor()
        print("#" * 40)
        print("== Enter details of the book ==")
        title = input("Enter title of book: ")
        author_name = input("Enter author's name: ")
        genre = input("Enter genre of book: ")
        publication_date = input("Enter publication date of book (yyyy-mm-dd): ")
        availability_status = True

        query = "INSERT INTO book (book_id, title, author_name, genre, publication_date, availability_status) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (
            None,
            title,
            author_name,
            genre,
            publication_date,
            availability_status,
        )

        cur.execute(query, val)
        con.commit()
        return "Book added successfully!"

    except myconn.Error as e:
        print("Error:", e)
        return "Error occurred while adding the book."

    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()


def remove_book():
    try:
        con = get_database_connection()
        cur = con.cursor()

        print("#" * 40)
        book_id = int(input("Enter id of book: "))
        query = "DELETE FROM book WHERE book_id = %s"
        val = (book_id,)

        cur.execute(query, val)
        con.commit()
        return "Book removed successfully!"

    except myconn.Error as e:
        print("Error:", e)
        return "Error occurred while removing the book."

    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()


def update_book():
    try:
        con = get_database_connection()
        cur = con.cursor()

        print("#" * 40)
        book_id = int(input("Enter id of book: "))
        query = "SELECT * FROM book WHERE book_id = %s"
        val = (book_id,)

        cur.execute(query, val)
        result = cur.fetchone()

        if result:
            print(
                f"\nBook Id = {result[0]}\nBook Name = {result[1]}\nAuthor Name = {result[2]}\n"
            )
            ans = input("Is this the book you are trying to update? Type 'y': ").lower()

            if ans == "y":
                print(
                    "What do you want to update?\n 1. Book Name\n 2. Author Name\n 3. Genre Book\n 4. Publication Date"
                )
                choice = int(input("Choose from option: "))

                if choice in [1, 2, 3, 4]:
                    update_field = ""
                    new_value = ""

                    if choice == 1:
                        update_field = "title"
                        new_value = input("Enter book name: ")
                    elif choice == 2:
                        update_field = "author_name"
                        new_value = input("Enter author name: ")
                    elif choice == 3:
                        update_field = "genre"
                        new_value = input("Enter genre: ")
                    elif choice == 4:
                        update_field = "publication_date"
                        new_value = input("Enter publication date (yyyy-mm-dd): ")

                    query = f"UPDATE book SET {update_field} = %s WHERE book_id = %s"
                    val = (new_value, book_id)

                    cur.execute(query, val)
                    con.commit()
                    return "Book updated successfully!"

                else:
                    return "Please choose a correct option! (1, 2, 3, 4)"
        else:
            return (
                "No books found against the provided book id... Please check book_id."
            )

    except myconn.Error as e:
        print("Error:", e)
        return "Error occurred while updating the book."

    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()


def show_books():
    try:
        con = get_database_connection()
        cur = con.cursor()

        query = """
        SELECT book_id, title, author_name, genre, publication_date, availability_status
        FROM book
        """
        cur.execute(query)
        books_data = cur.fetchall()

        if not books_data:
            return "No books found in the library."

        table = PrettyTable()
        table.field_names = [
            "Book ID",
            "Title",
            "Author",
            "Genre",
            "Publication Date",
            "Availability",
        ]

        for book in books_data:
            table.add_row(book)

        return str(table)

    except myconn.Error as e:
        print("Error:", e)
        return "Error occurred while fetching book details."

    finally:
        if "cur" in locals():
            cur.close()
        if "con" in locals():
            con.close()
