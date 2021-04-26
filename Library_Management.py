import numpy as np
import pandas as pd
import random
from Book import Book
from Person import Person
from datetime import datetime

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)


class Library_Management:

    def __init__(self, df_books, df_users):
        self.df_books = df_books
        self.df_users = df_users

    def start(self):
        done = False
        while not done:
            print("    ===============Welcome to  C&M Library===============")
            print("""             ===========LIBRARY MENU===========
                      1. Display all books
                      2. Display all users
                      3. Search books
                      4. Borrow books
                      5. Return books
                      6. Add books
                      7. Remove books
                      8. Exit
                      """)
            choice = input("Please enter choice(1, 2, 3, 4, 5, 6, 7 or 8): ")

            if choice == '1':
                self.display_books()

            elif choice == '2':
                self.display_users()

            elif choice == '3':
                self.search_books()

            elif choice == '4':
                self.borrow_books()

            elif choice == '5':
                self.return_books()

            elif choice == '6':
                self.add_books()

            elif choice == '7':
                self.remove_books()

            elif choice == '8':
                # write or cover current data to the books.csv and users.csv file
                self.df_books.to_csv("books.csv", index=False)
                self.df_users.to_csv("users.csv", index=False)
                done = True
                print('See you next time!')
            else:
                print('Error: Wrong choice!!!')

    def info_confirm(self, account_id):
        # create a set to store all valid account id
        st = set()
        for ele in self.df_users.account_id:
            st.add(ele)
        # check if given account id is valid
        if account_id not in st:
            print(f'Error: account-id {account_id} does not exist')
            return False

        # confirm password
        password = self.df_users[self.df_users.account_id == account_id].password.item()
        first_name = self.df_users[self.df_users.account_id == account_id].first_name.item()
        password_input = input(f'Hi {first_name}, Please enter the password: ')
        if password != password_input:
            print("Error: inaccurate password!!!")
            while True:
                print("""           ===========Please Select===========
                1. Enter the password again
                2. Exit
                                              """)
                choice = input("Please enter your choice(1 or 2): ")
                if choice == '1':
                    # recursion
                    return self.info_confirm(account_id)
                elif choice == '2':
                    return False
                else:
                    print('Error: Wrong choice!!!')
        return True

    def display_books(self):
        print("""           ===========Please Select===========
                1. Yes
                other. No
                                              """)
        choice = input("Are you the administrator: ")
        if choice == "1":
            if self.info_confirm("1"):
                print(self.df_books.to_string(index=False))
            else:
                print(self.df_books.iloc[:, :-2].to_string(index=False))
        else:
            print(self.df_books.iloc[:, :-2].to_string(index=False))

    def display_users(self):
        if self.info_confirm("1"):
            print(self.df_users.to_string(index=False))

    def search_books(self):
        while True:
            print("""               ===========Please Select===========
                        1. Search by book id
                        2. Search by ISBN
                        3. Search by title
                        4. Search by author
                        5. Exit
                                                     """)
            choice = input("Please enter choice(1, 2, 3, 4 or 5): ")
            if choice == '1':
                book_id = input("Please enter book id: ")
                print(self.df_books[self.df_books.book_id == book_id].iloc[:, :-2].to_string(index=False))
            elif choice == '2':
                ISBN = input("Please enter ISBN: ")
                print(self.df_books[self.df_books.ISBN == ISBN].iloc[:, :-2].to_string(index=False))
            elif choice == '3':
                title = input("Please enter title: ")
                booleans = []
                for element in self.df_books.title:
                    if title.lower() in element.lower():
                        booleans.append(True)
                    else:
                        booleans.append(False)
                print(self.df_books[pd.Series(booleans)].iloc[:, :-2].to_string(index=False))
            elif choice == '4':
                author = input("Please enter author: ")
                booleans = []
                for element in self.df_books.author:
                    if author.lower() in element.lower():
                        booleans.append(True)
                    else:
                        booleans.append(False)
                print(self.df_books[pd.Series(booleans)].iloc[:, :-2].to_string(index=False))
            elif choice == '5':
                break
            else:
                print('Error: Wrong choice!!!')

    def borrow_books(self):
        print("""           ===========Please Select===========
                        1. Create a new account
                        2. Borrow with existing account
                        3. Exit
                                                      """)
        choice = input("Please enter your choice(1, 2 or 3): ")
        # Create a new account
        if choice == '1':
            person = Person()
            person.account_id = len(self.df_users) + 1

            first_name = input("Please enter your first name: ")
            person.first_name = first_name.capitalize()

            last_name = input("Please enter your last name: ")
            person.last_name = last_name.capitalize()

            password = input("Please enter your password: ")
            person.password = password

            # store all the information of the person into the dataframe
            row = len(self.df_users)
            for a in [attr for attr in dir(person) if not attr.startswith('__')]:
                self.df_users.loc[row, [a]] = str(getattr(person, a))

            print("Congratulations!, You have created your library account successfully!")
            print("Please record following information to log into library")
            print("************************")
            print(f'  Account id: {person.account_id}')
            print(f'  Password: {password}')
            print("************************")

            self.borrow_books()

        # Borrow with existing account
        elif choice == '2':
            account_id = input("Please enter your account id: ")
            if not self.info_confirm(account_id):
                return
            while True:
                book_id = input("Please enter your book id: ")
                # check whether the book id you entered is valid
                while book_id not in self.df_books.book_id.values or \
                        self.df_books[self.df_books.book_id == book_id].status.item() != 'available':
                    print("Error: The book id you entered is not available")
                    book_id = input("Please enter your book id again: ")

                # show the book you just borrowed
                selected = self.df_books[self.df_books.book_id == book_id]
                print("The following book is just borrowed by you:")
                print(selected.iloc[:, :-2].to_string(index=False))

                # change corresponding information about this book in the df_books (data frame)
                row_index = selected.index.item()
                self.df_books.at[row_index, 'status'] = "unavailable"
                self.df_books.at[row_index, 'holder'] = account_id
                self.df_books.at[row_index, 'borrowed_date'] = datetime.now().strftime("%m/%d/%Y")

                # next selection
                while True:
                    print("""                       ===========Please Select===========
                                    1. keep borrowing books
                                    2. Exit
                                                                          """)
                    choice = input("Please enter your choice(1 or 2): ")
                    if choice == "1":
                        break
                    elif choice == "2":
                        return
                    else:
                        print("Error: Invalid selection")

        elif choice == '3':
            return

        else:
            print('Error: Invalid choice!!!')
            self.borrow_books()

    def return_books(self):
        account_id = input("Please enter your account id: ")
        # account and password confirm
        if not self.info_confirm(account_id):
            return

        while True:
            book_id = input("Please enter your returning book id: ")

            while book_id not in self.df_books.book_id.values or \
                    self.df_books[self.df_books.book_id == book_id].holder.item() != account_id:
                print("Error: The book id you entered is invalid")
                book_id = input("Please enter your returning book id again: ")

            selected = self.df_books[self.df_books.book_id == book_id]
            print("The following book is just returned by you:")
            print(selected.iloc[:, :-2].to_string(index=False))

            row_index = selected.index.item()
            self.df_books.at[row_index, 'status'] = "available"
            self.df_books.at[row_index, 'holder'] = np.NaN
            date = self.df_books.at[row_index, 'borrowed_date']
            self.df_books.at[row_index, 'borrowed_date'] = np.NaN

            try:
                borrowed_date = datetime.strptime(date, "%m/%d/%Y").date()
                current_date = datetime.now().date()
                borrowed_days = (current_date - borrowed_date).days
                charge = (borrowed_days-30) * 1.0
                if borrowed_days <= 30:
                    print("No charge for returning book within 30 days. Thank you!")
                else:
                    index = self.df_users[self.df_users.account_id == account_id].index.item()
                    self.df_users.at[index, 'balance'] = charge
                    print(f'Since you borrowed book over 30 days(starting from {borrowed_date})')
                    print(f'You need to pay ${charge} overdue charge')
            except ValueError:
                print("Data format error for the selected book in the database")

            while True:
                print("""                       ===========Please Select===========
                                1. keep returning books
                                2. Exit
                                                                      """)
                choice = input("Please enter your choice(1 or 2): ")
                if choice == "1":
                    break
                elif choice == "2":
                    return
                else:
                    print("Error: Invalid selection")

    def add_books(self):
        if not self.info_confirm('1'):
            return

        while True:
            book = Book()
            book_id = str(random.randint(100000, 999999))
            while book_id in self.df_books.book_id.values:
                book_id = random.randint(100000, 999999)
            book.book_id = book_id
            ISBN = input("Please enter ISBN of the book: ")
            book.ISBN = ISBN
            title = input("Please enter title of the book: ")
            book.title = title.capitalize()
            author = input("Please enter author of the book: ")
            book.author = author.capitalize()
            publisher = input("Please enter publisher of the book: ")
            book.publisher = publisher.capitalize()
            language = input("Please enter language of the book: ")
            book.language = language
            while True:
                date = input("Please enter publication_date of the book(Mon/Day/Year): ")
                try:
                    datetime.strptime(date, "%m/%d/%Y")
                    book.publication_date = date
                    break
                except ValueError:
                    print("Oops!  That was no valid date.  Try again...")
            row = len(self.df_books)
            for a in [attr for attr in dir(book) if not attr.startswith('__')]:
                self.df_books.loc[row, [a]] = getattr(book, a)
            print("The following book has been added to the library:")
            print(self.df_books[-1:].to_string(index=False))
            print("""           ===========Please Select===========
                    1. Keep adding books
                    Any. Exit
                                          """)
            choice = input("Please enter your choice: ")
            if choice == '1':
                continue
            else:
                break

    def remove_books(self):
        if not self.info_confirm('1'):
            return

        while True:
            book_id = input("Please enter the book id to delete: ")
            if book_id not in self.df_books.book_id.values:
                print("Error: The book id you entered does not exist")
            else:
                deleted = self.df_books[self.df_books.book_id == book_id]
                print("The following book has been removed from library:")
                print(deleted.to_string(index=False))
                self.df_books.drop(deleted.index, inplace=True)
            while True:
                print("""                       ===========Please Select===========
                            1. Continue to delete
                            other. Exit
                                                                     """)
                choice = input("Please enter choice: ")
                if choice == "1":
                    break
                else:
                    return
