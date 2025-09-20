import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO users (username, password_hash) VALUES (?, ?)"""
    db.execute(sql, [username, password_hash])

def check_login(username, password):
    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    result = db.query(sql, [username])
    if not result:
        return None
    
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    else:
        return None

def get_user(user_id):
    sql = """SELECT * FROM users WHERE users.id = ?"""
    return db.query(sql, [user_id])[0]

def get_comments(user_id):
    sql = """SELECT * FROM comments WHERE user_id = ?"""
    return db.query(sql, [user_id])
