from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect("bookstore.db")
    conn.row_factory = sqlite3.Row
    return conn


def get_all_categories():
    conn = get_db_connection()
    categories = conn.execute(
        "SELECT * FROM category ORDER BY categoryName"
    ).fetchall()
    conn.close()
    return categories


@app.route("/")
def home():
    categories = get_all_categories()
    return render_template("index.html", categories=categories)


@app.route("/category/<int:categoryId>")
def category(categoryId):
    conn = get_db_connection()

    categories = conn.execute(
        "SELECT * FROM category ORDER BY categoryName"
    ).fetchall()

    selected_category = conn.execute(
        "SELECT * FROM category WHERE categoryId = ?",
        (categoryId,)
    ).fetchone()

    books = conn.execute(
        """
        SELECT *
        FROM book
        WHERE categoryId = ?
        ORDER BY title
        """,
        (categoryId,)
    ).fetchall()

    conn.close()

    if selected_category is None:
        return render_template(
            "error.html",
            categories=categories,
            error="Category not found."
        )

    return render_template(
        "category.html",
        categories=categories,
        selectedCategory=selected_category,
        books=books,
        searchTerm=None,
        nothingFound=False
    )


@app.route("/search", methods=["POST"])
def search():
    search_term = request.form.get("search", "").strip()

    conn = get_db_connection()

    categories = conn.execute(
        "SELECT * FROM category ORDER BY categoryName"
    ).fetchall()

    books = conn.execute(
        """
        SELECT *
        FROM book
        WHERE title LIKE ?
        ORDER BY title
        """,
        (f"%{search_term}%",)
    ).fetchall()

    conn.close()

    return render_template(
        "category.html",
        categories=categories,
        selectedCategory=None,
        books=books,
        searchTerm=search_term,
        nothingFound=(len(books) == 0)
    )


@app.route("/book/<int:bookId>")
def book_detail(bookId):
    conn = get_db_connection()

    categories = conn.execute(
        "SELECT * FROM category ORDER BY categoryName"
    ).fetchall()

    book = conn.execute(
        """
        SELECT b.*, c.categoryName
        FROM book b
        JOIN category c ON b.categoryId = c.categoryId
        WHERE b.bookId = ?
        """,
        (bookId,)
    ).fetchone()

    conn.close()

    if book is None:
        return render_template(
            "error.html",
            categories=categories,
            error="Book not found."
        )

    return render_template(
        "book_detail.html",
        categories=categories,
        book=book
    )


@app.route("/add", methods=["GET", "POST"])
def add_book():
    conn = get_db_connection()
    categories = conn.execute(
        "SELECT * FROM category ORDER BY categoryName"
    ).fetchall()

    if request.method == "POST":
        title = request.form["title"].strip()
        author = request.form["author"].strip()
        isbn = request.form["isbn"].strip()
        price = request.form["price"].strip()
        image = request.form["image"].strip()
        category_id = request.form["categoryId"]

        try:
            conn.execute(
                """
                INSERT INTO book (categoryId, title, author, isbn, price, image, readNow)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (category_id, title, author, isbn, price, image, 0)
            )
            conn.commit()
            conn.close()
            return redirect(url_for("home"))

        except Exception as e:
            conn.close()
            return render_template(
                "error.html",
                categories=categories,
                error=str(e)
            )

    conn.close()
    return render_template("add_book.html", categories=categories)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
