PRAGMA foreign_keys = ON;

CREATE TABLE category (
    categoryId INTEGER PRIMARY KEY,
    categoryName TEXT NOT NULL,
    categoryImage TEXT
);

CREATE TABLE book (
    bookId INTEGER PRIMARY KEY,
    categoryId INTEGER NOT NULL,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE,
    price REAL NOT NULL,
    image TEXT,
    readNow INTEGER DEFAULT 0,
    FOREIGN KEY (categoryId) REFERENCES category(categoryId)
);

