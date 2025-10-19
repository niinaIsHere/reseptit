import sqlite3
from flask import g

def get_connection():
    """Connects to database"""
    con = sqlite3.connect("database.db")
    con.execute("PRAGMA foreign_keys = ON")
    con.row_factory = sqlite3.Row
    return con

def execute(sql, params=[]):
    """Executes an SQL action"""
    con = get_connection()
    result = con.execute(sql, params)
    con.commit()
    g.last_insert_id = result.lastrowid
    con.close()

def query(sql, params=[]):
    """Gets information from the database"""
    con = get_connection()
    result = con.execute(sql, params).fetchall()
    con.close()
    return result

def last_insert_id():
    """Gets id of last insert"""
    return g.last_insert_id
