INSERT INTO book (categoryId, title, author, isbn, price, image, readNow)
VALUES (?, ?, ?, ?, ?, ?, ?);

SELECT * FROM category;

SELECT * FROM book;

SELECT b.bookId, b.title, b.author, c.categoryName
FROM book b
JOIN category c 
ON b.categoryId = c.categoryId
WHERE c.categoryId = ?;

SELECT * FROM book
WHERE title LIKE ?;

UPDATE book
SET price = ?
WHERE bookId = ?;

DELETE FROM book
WHERE bookId = ?;

--additional
SELECT * FROM book
WHERE author LIKE ?;
