Name: Xueyun Bai
Descrption: This project is a bookstore database built with SQLite and Python CLI. It allows you to view categories, view books, search books by title, add new books, update book prices, and delete books.
How I create the database:
sqlite3 bookstore.db < createTables.sql
sqlite3 bookstore.db < sampledata.sql
I first create the table and then insert the sample data from real world, where I searched each book on amazon to see details
Then I insert tables and sampledata with database
How to run the python program:
just write 
python3 bookstorecli.py
in the terminal
