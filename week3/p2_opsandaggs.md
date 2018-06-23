Write the following queries to perform the following:

1.  Find the names of the top five most caloric snacks.
    aggregates_exercise=# SELECT name
    aggregates_exercise-# FROM snacks
    aggregates_exercise-# ORDER BY calories
    aggregates_exercise-# DESC
    aggregates_exercise-# LIMIT 5;
    name

---

ice cream
payday
potato chips
twix
fruit roolup
(5 rows)

2.  Find the names of the 3 cheapest snacks.
    aggregates_exercise=# SELECT name
    aggregates_exercise-# FROM snacks
    aggregates_exercise-# ORDER BY price
    aggregates_exercise-# ASC
    aggregates_exercise-# LIMIT 3;
    name

---

cheese its
capri sun
3 musketeers
(3 rows)

3.  Calculate the total calories for all the snacks. Call this column total_calories.
    aggregates_exercise=# SELECT SUM(calories) AS total_calories FROM snacks;
    total_calories

---

           8040

(1 row)

4.  Calculate the average price for all the snacks. Call this column average_price.
    aggregates_exercise=# SELECT AVG(price) AS average_price FROM snacks;
    average_price

---

3.8676190476190476
(1 row)

5.  Calculate the lowest price for all the snacks. Call this column lowest_price.
    aggregates_exercise=# SELECT MIN(price) AS lowest_price FROM snacks;
    lowest_price

---

         0.99

(1 row)

6.  Calculate the highest price for all the snacks. Call this column highest_price.
    aggregates_exercise=# SELECT MAX(price) AS lowest_price FROM snacks;
    lowest_price

---

        11.99

(1 row)

7.  Find the count for each kind of candy in the table. Your output should look like this:

aggregates_exercise=# SELECT kind, COUNT(kind) FROM snacks GROUP BY kind;
kind | count
-------------+-------
chips | 5
candy bar | 5
fruit snack | 2
yogurt | 1
frozen | 1
baked goods | 5
beverage | 2
(7 rows)

8.  Find the count of each kind of candy where the count is greater than one. Your output should look like this:

aggregates_exercise=# SELECT kind, COUNT(kind) FROM snacks GROUP BY kind HAVING COUNT(kind) > 1;
kind | count
-------------+-------
chips | 5
candy bar | 5
fruit snack | 2
baked goods | 5
beverage | 2
(5 rows)

9.  Find the average number of calories for each kind of candy and call the name of your column that contains the average average_calories. Order your output by the kind of candy in ascending order. Your output should look like this.

aggregates_exercise=# SELECT kind, ROUND(AVG(calories))
AS average_calories
FROM snacks
GROUP BY kind
ORDER BY kind;
kind | average_calories
-------------+------------------
baked goods | 298
beverage | 210
candy bar | 340
chips | 306
frozen | 2000
fruit snack | 320
yogurt | 260


