Part 1 - CRUD Exercises
Write the SQL commands necessary to do the following:

1.  Create a database called first_assignment.
    psql
    KBrady=# CREATE DATABASE first_assignment;
    CREATE DATABASE

2.  Connect to that database.
    KBrady=# \c first_assignment
    You are now connected to database "first_assignment" as user "KBrady".
    first_assignment=#

3.  Create a table called products with columns for:
    id, which should be a unique auto-incremementing integer
    name, which should be text, and not nullable
    price, which should be numeric, and greater than zero
    can_be_returned, which should be a boolean, and not nullable

first_assignment=# CREATE TABLE products (id SERIAL PRIMARY KEY,
first_assignment(# name TEXT NOT NULL,
first_assignment(# price NUMERIC CHECK (price > 0)
first_assignment(# ,
first_assignment(# can_be_returned BOOLEAN NOT NULL);
CREATE TABLE

4.  Add a product to the table with the name of "chair", price of 44.00, and can_be_returned of false.

INSERT INTO products(name, price, can_be_returned) VALUES('chair', 44.00, can_be_returned = false);

5.  Add a product to the table with the name of "stool", price of 25.99, and can_be_returned of true.

first_assignment=# INSERT INTO products(name, price, can_be_returned) VALUES ('stool', 25.99, true);
INSERT 0 1
first_assignment=#

6.  Add a product to the table with the name of "table", price of 124.00, and can_be_returned of false.

first_assignment=# INSERT INTO products(name, price, can_be_returned) VALUES ('table', 124.00, false);
INSERT 0 1

7.  Display all of the rows and columns in the table.
    first_assignment=# SELECT \* FROM products;
    id | name | price | can_be_returned
    ----+-------+--------+-----------------
    1 | stool | 25.99 | t
    2 | table | 124.00 | f
    (2 rows)

8.  Display all of the names of the products.
    first_assignment=# SELECT name FROM products;
    name

---

stool
table
(2 rows)

9.  Display all of the names and prices of the products.
    first_assignment=# SELECT name, price FROM products;
    name | price  
    -------+--------
    stool | 25.99
    table | 124.00
    (2 rows)

10. Add a new product - make up whatever you would like!
    first_assignment=# INSERT INTO products(name, price, can_be_returned) VALUES ('couch', 600.00, true);
    INSERT 0 1

11. Display only the products that can_be_returned.
    first_assignment=# SELECT name FROM products WHERE can_be_returned=true;
    name

---

stool
couch
(2 rows)

12. Display only the products that have a price less than 44.00.
    first_assignment=# SELECT name, price FROM products WHERE price < 44.00;
    name | price
    -------+-------
    stool | 25.99
    (1 row)

13. Display only the products that have a price in between 22.50 and 99.99.
    first_assignment=# SELECT name, price FROM products WHERE price > 22.50 AND price < 99.99;
    name | price
    -------+-------
    stool | 25.99
    (1 row)

14. There's been a change in company policy, and now all tables are returnable. Update the database accordingly.
    first_assignment=# UPDATE products SET can_be_returned = true WHERE name = 'table';
    UPDATE 1

15. There's a sale going on: Everything is $20 off! Update the database accordingly.
    first_assignment=# UPDATE products SET price = price -20;
    UPDATE 3

16. Because of the sale, everything that costs less than $25 has sold out. Remove all products whose price meets this criteria.
    first_assignment=# DELETE FROM products WHERE price < 25;
    DELETE 1

17. And now the sale is over. For the remaining products, increase their price by $20. first_assignment=# UPDATE products SET price = price + 20;
    UPDATE 2
