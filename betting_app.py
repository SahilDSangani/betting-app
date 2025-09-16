import streamlit as st
import sqlite3
import random

# Database setup

def init_db():
    # conn is sqlite3 connection object used for running queries
    # connect() opens a connection to the sqlite file 'bets.db'
    conn = sqlite3.connect("bets.db")
    conn.execute("PRAGMA foreign_keys = ON")


    # c is a cursor used to run SQL commands
    c = conn.cursor()

    # creates users table 
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    balance INTEGER)''')
    
    # creates bets table
    c.execute('''CREATE TABLE IF NOT EXISTS bets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    amount INTEGER,
                    team TEXT,
                    outcome TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id))''')
    
    # writes the table creation changes to disk
    conn.commit()

    # returns connection object so the rest of the app can run queries on the same DB file
    return conn

def get_user(conn, username):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def create_user(conn, username, balance=100):
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO users (username, balance) VALUES (?, ?)", (username, balance))
    conn.commit()

def update_balance(conn, user_id, new_balance):
    c = conn.cursor()
    c.execute("UPDATE users SET balance = ? WHERE id = ?", (new_balance, user_id))
    conn.commit()

def add_bet(conn, user_id, amount, team, outcome):
    c = conn.cursor()
    c.execute("INSERT INTO bets (user_id, amount, team, outcome) VALUES (?, ?, ?, ?)", 
              (user_id, amount, team, outcome))
    conn.commit()

def get_bet_history(conn, user_id):
    c = conn.cursor()
    c.execute("SELECT amount, team, outcome, timestamp FROM bets WHERE user_id = ?", (user_id,))
    return c.fetchall()


st.title("🎲 Betting App with Database")
st.write("Welcome to my betting app prototype!")

conn = init_db()

username = st.text_input("Username:")

if (username):
    st.write(f"Current user: {username}")

bet_amount = st.number_input("Enter your bet amount:", min_value=0, value=10)
team_choice = st.selectbox("Pick a team:", ["Team A", "Team B"])

if st.button("Place Bet"):
    st.success(f"You bet ${bet_amount} on {team_choice}")

