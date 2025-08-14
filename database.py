# database.py
import sqlite3
import random
import os

# Create or connect to the database
conn = sqlite3.connect('database.db')
cur = conn.cursor()

# Enable foreign keys
cur.execute("PRAGMA foreign_keys = ON")

# Drop existing tables (for reset)
cur.executescript('''
DROP TABLE IF EXISTS purchases;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS products;
''')

# Create tables
cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    image_url TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    product_name TEXT,
    price REAL NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(product_id) REFERENCES products(id)
)
''')

# Generate sample product data
sample_names = [
    "Shoes", "Watch", "Backpack", "Headphones", "Sunglasses", "T-shirt", "Jeans", "Jacket", "Smartphone",
    "Laptop", "Tablet", "Camera", "Sneakers", "Hat", "Scarf", "Gloves", "Sweater", "Belt", "Wallet", "Perfume",
    "Mug", "Bottle", "Notebook", "Pen", "Speaker", "Charger", "Mouse", "Keyboard", "Monitor", "Desk Lamp",
    "Chair", "TV", "Game Console", "Router", "Power Bank", "Earbuds", "Tripod", "Flashlight", "Fan", "Mirror",
    "Toaster", "Blender", "Oven", "Microwave", "Vacuum", "Curtains", "Bedsheet", "Pillow", "Towel", "Rug"
]

# Insert products with images
product_list = [
    (i + 1, sample_names[i], round(random.uniform(10, 100), 2), f'/static/images/product{i + 1}.jpg')
    for i in range(50)
]

cur.executemany("INSERT INTO products (id, name, price, image_url) VALUES (?, ?, ?, ?)", product_list)

# Commit and close
conn.commit()
conn.close()

print("Database with 50 products created successfully.")
