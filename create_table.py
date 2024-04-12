

import sqlite3

conn = sqlite3.connect('database.db')
print("Connected to database successfully")

conn.execute('CREATE TABLE products (product_name TEXT, product_price REAL)')
print("Created table successfully!")
conn.execute('CREATE TABLE List (product_nm TEXT, product_prc REAL)')
print("Created table successfully!")

conn.close()

