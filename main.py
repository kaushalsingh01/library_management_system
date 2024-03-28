import book
import issued
import member


def book_menu():
    while True:
        print("#" * 40)
        print("****Books Menu****")
        print("1. Add Book")
        print("2. Update Book")
        print("3. Remove Book")
        print("4. Show Books List")
        print("5. Exit")
        choice_book = int(input("Choose an option (1,2,3,4,5): "))
        print("#" * 40)

        if choice_book == 1:
            msg = book.add_book()
            print(msg)

        elif choice_book == 2:
            msg = book.update_book()
            print(msg)

        elif choice_book == 3:
            msg = book.remove_book()
            print(msg)

        elif choice_book == 4:
            msg = book.show_books()
            print(msg)

        elif choice_book == 5:
            break

        else:
            print("Pls! choose a valid option..")


def member_menu():
    while True:
        print("#" * 40)
        print("****Members Menu****")
        print("1. Add Member")
        print("2. Update Member")
        print("3. Remove Member")
        print("4. Show Members List")
        print("5. Exit")
        choice_member = int(input("Choose an option (1,2,3,4,5): "))
        print("#" * 40)

        if choice_member == 1:
            msg = member.add_member()
            print(msg)

        elif choice_member == 2:
            msg = member.update_member()
            print(msg)

        elif choice_member == 3:
            msg = member.remove_member()
            print(msg)

        elif choice_member == 4:
            msg = member.show_members()
            print(msg)

        elif choice_member == 5:
            break

        else:
            print("Pls! choose a valid option..")


def issue_menu():
    while True:
        print("#" * 40)
        print("****Issue and Return Menu****")
        print("1. Issue Book")
        print("2. Extend Issue Time")
        print("3. Return Book")
        print("4. Show Issued List")
        print("5. Exit")
        choice_issue = int(input("Choose an option (1,2,3,4,5): "))
        print("#" * 40)

        if choice_issue == 1:
            msg = issued.issue_book()
            print(msg)

        elif choice_issue == 2:
            msg = issued.extend_borrow()
            print(msg)

        elif choice_issue == 3:
            msg = issued.return_book()
            print(msg)

        elif choice_issue == 4:
            msg = issued.show_issues()
            print(msg)

        elif choice_issue == 5:
            break

        else:
            print("Pls! choose a valid option..")


if __name__ == "__main__":
    while True:
        print("#" * 40)
        print("****WELCOME TO LIBRARY MANAGEMENT SYSTEM****")
        print("1. To Manage Books.")
        print("2. To Manage Members.")
        print("3. To Manage Issuing/Returning Books.")
        print("4. Exit")
        choice_main = int(input("Choose an option (1, 2, 3, 4): "))
        print("#" * 40)

        if choice_main == 1:
            book_menu()

        elif choice_main == 2:
            member_menu()

        elif choice_main == 3:
            issue_menu()

        elif choice_main == 4:
            print("Thank You!! Come Again..")
            break

        else:
            print("Please choose a valid option.")
