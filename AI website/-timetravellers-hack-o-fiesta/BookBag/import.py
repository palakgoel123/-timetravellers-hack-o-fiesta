import os
import csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# configuring the databse link
uri = os.getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

# set up the database
engine = create_engine(uri)
db = scoped_session(sessionmaker(bind=engine))

def main():
    '''
    Adding the files from 'books.csv' into the DATABASE
    '''
    # opening the file
    books = open('books.csv')

    # reding the book in csv form
    reader = csv.reader(books)

    # inserting the values from the csv file into the database
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
        {"isbn":isbn, "title":title, "author":author, "year":year})
    db.commit()

    print("Files added")

if __name__ == '__main__':
    main()
