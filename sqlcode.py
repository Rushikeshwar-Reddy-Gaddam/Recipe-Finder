#import mysql lib
import mysql.connector
#connect to the database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="root",
    database="bs"
)

#connection
mycursor = mydb.cursor()



#create table user
user_query = """
CREATE TABLE if NOT EXISTS user (
  user_id INTEGER AUTO_INCREMENT PRIMARY KEY ,
    username TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    user_address TEXT NOT NULL,
    city varchar(255) NOT NULL,
    state varchar(255) NOT NULL,
    zip varchar(255) NOT NULL,
    phone varchar(255) NOT NULL
)
"""
#create table products
products_query = """
CREATE TABLE if NOT EXISTS products (
  product_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    product_name TEXT NOT NULL,
    product_price FLOAT NOT NULL,
    product_author TEXT NOT NULL,
    product_category TEXT NOT NULL,
    product_quantity INTEGER NOT NULL
)
"""

#create table orders
orders_query = """
CREATE TABLE if NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    order_quantity INTEGER NOT NULL,
    order_total FLOAT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
"""

#create table payments
payments_query = """
CREATE TABLE if NOT EXISTS payments (
  payment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    payment_date DATE NOT NULL,
    payment_amount FLOAT NOT NULL,
    card_number INTEGER NOT NULL,
    card_cvv INTEGER NOT NULL,
    card_expiry DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user(user_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
)
"""


#run the queries
mycursor.execute(user_query)
mycursor.execute(products_query)
mycursor.execute(orders_query)
mycursor.execute(payments_query)

#commit the changes
mydb.commit()



