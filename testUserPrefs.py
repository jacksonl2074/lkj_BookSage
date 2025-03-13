# Co-Pilot: what is a good way to ask user's their prefereces on books? coding in python and i want to save answers to a database
# 

import sqlite3

# Create or connect to a database
conn = sqlite3.connect("user_preferences.db")
cursor = conn.cursor()

# Create a table for storing user preferences
cursor.execute("""
CREATE TABLE IF NOT EXISTS BookPreferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    favorite_genre TEXT,
    favorite_author TEXT,
    favorite_book TEXT
)
""")
conn.commit()

# Function to collect user input
def ask_preferences():
    print("Let's get to know your book preferences!")
    name = input("What's your name? ")
    favorite_genre = input("What's your favorite book genre? ")
    favorite_author = input("Who's your favorite author? ")
    favorite_book = input("What's your all-time favorite book? ")

    # Save answers to the database
    cursor.execute("""
    INSERT INTO BookPreferences (name, favorite_genre, favorite_author, favorite_book)
    VALUES (?, ?, ?, ?)
    """, (name, favorite_genre, favorite_author, favorite_book))
    conn.commit()

    print("Thank you! Your preferences have been saved.")

# Collect preferences
ask_preferences()

# Close the database connection
conn.close()
