import pandas as pd
from Library_Management import Library_Management

# read data from books.csv and users.csv files
# pass them to date library management system(class), and start the system
def main():
    df_books = pd.read_csv('books.csv', sep=',', header=0, dtype=str)
    df_users = pd.read_csv('users.csv', sep=',', header=0, dtype=str)
    library = Library_Management(df_books, df_users)
    library.start()


main()

