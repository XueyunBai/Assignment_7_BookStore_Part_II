import sqlite3

def connect_db():
    conn = sqlite3.connect("bookstore.db")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def view_all_categories(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category")
    rows = cursor.fetchall()
    print("\nCategories:")
    for row in rows:
        print(row)

def view_all_books(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book")
    rows = cursor.fetchall()
    print("\nBooks:")
    for row in rows:
        print(row)

def view_books_in_category(conn):
    category_id = input("Enter category id: ")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.bookId, b.title, b.author, c.categoryName
        FROM book b
        JOIN category c ON b.categoryId = c.categoryId
        WHERE c.categoryId = ?
    """, (category_id,))
    rows = cursor.fetchall()
    print("\nBooks in category:")
    for row in rows:
        print(row)

def search_books_by_title(conn):
    keyword = input("Enter title keyword: ")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM book WHERE title LIKE ?",
        ('%' + keyword + '%',)
    )
    rows = cursor.fetchall()
    print("\nSearch results:")
    for row in rows:
        print(row)

def add_new_book(conn):
    category_id = input("Enter category id: ")
    title = input("Enter title: ")
    author = input("Enter author: ")
    isbn = input("Enter ISBN: ")
    price = input("Enter price: ")
    image = input("Enter image filename: ")
    read_now = input("Enter readNow (0 or 1): ")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO book (categoryId, title, author, isbn, price, image, readNow)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (category_id, title, author, isbn, price, image, read_now))
    conn.commit()
    print("Book added successfully.")

def update_book_price(conn):
    book_id = input("Enter book id: ")
    new_price = input("Enter new price: ")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE book
        SET price = ?
        WHERE bookId = ?
    """, (new_price, book_id))
    conn.commit()
    print("Book price updated successfully.")

def delete_book(conn):
    book_id = input("Enter book id: ")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM book WHERE bookId = ?", (book_id,))
    conn.commit()
    print("Book deleted successfully.")
def search_books_by_author(conn):
    author_keyword = input("Enter author keyword: ")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM book WHERE author LIKE ?",
        ('%' + author_keyword + '%',)
    )
    rows = cursor.fetchall()
    print("\nBooks by author search:")
    for row in rows:
        print(row)

def main():
    conn = connect_db()
    while True:
        print("\n--- Bookstore Menu ---")
        print("1. View all categories")
        print("2. View all books")
        print("3. View books in a category")
        print("4. Search books by title")
        print("5. Add a new book")
        print("6. Update a book price")
        print("7. Delete a book")
        print("8. Search books by author")
        print("9. Quit")
        choice = input("Enter your choice: ")
        if choice == "1":
            view_all_categories(conn)
        elif choice == "2":
            view_all_books(conn)
        elif choice == "3":
            view_books_in_category(conn)
        elif choice == "4":
            search_books_by_title(conn)
        elif choice == "5":
            add_new_book(conn)
        elif choice == "6":
            update_book_price(conn)
        elif choice == "7":
            delete_book(conn)
        elif choice == "8":
            search_books_by_author(conn)
        elif choice == "9":
            print("Bye")
            break
        else:
            print("Invalid choice. Please try again.")
    conn.close()

if __name__ == "__main__":
    main()
