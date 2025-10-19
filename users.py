from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import db

def create_user(username, password):
    """Adds a new user into database"""
    password_hash = generate_password_hash(password)
    sql = """INSERT INTO users (username, password_hash, created) VALUES (?, ?, ?)"""
    db.execute(sql, [username, password_hash, datetime.now().date().isoformat()])

def check_login(username, password):
    """Checks if login credentials are valid"""
    sql = """SELECT id, password_hash FROM users WHERE username = ?"""
    result = db.query(sql, [username])
    if not result:
        return None
    user_id = result[0]["id"]
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        return user_id
    return None

def valid_username(username):
    """Checks if new user's username is valid"""
    if len(username) > 20:
        return (False, "Username is too long")
    if len(username) < 3:
        return (False, "Username is too short")
    if not username.isalnum():
        return (False, "Username cannot include whitespaces or special characters")
    return (True, None)

def valid_password(password):
    """Checks if new user's password is valid"""
    if len(password) < 8:
        return (False, "Password is too short")
    return (True, None)

def get_user(user_id):
    """Gets user's information from database"""
    sql = """SELECT id, username, created FROM users WHERE users.id = ?"""
    return db.query(sql, [user_id])[0]

def get_bio(user_id):
    """Gets user's bio from database"""
    sql = """SELECT bio FROM profiles WHERE profiles.user_id = ?"""
    result = db.query(sql, [user_id])
    if not result:
        return None
    return result[0][0]

def update_bio(user_id, content):
    """Updates user's bio in database"""
    sql = """INSERT OR REPLACE INTO profiles (user_id, bio) VALUES (?, ?)"""
    return db.execute(sql, [user_id, content])

def valid_bio(bio):
    """Checks if a bio text is valid"""
    if len(bio) > 500:
        return (False, "Bio is too long")
    if len(bio) < 2:
        return (False, "Bio is too short")
    return (True, None)

def get_comments(user_id):
    """Gets comments posted by a user from database"""
    sql = """SELECT recipe_id, content, created FROM comments WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_ratings(user_id):
    """Gets ratings posted by a user from database"""
    sql = """SELECT recipe_id, rating, created FROM ratings WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_rating(user_id, item_id):
    """Gets user's rating on a specific recipe from database"""
    sql = """SELECT rating FROM ratings WHERE user_id = ? AND recipe_id = ?"""
    result = db.query(sql, [user_id, item_id])
    if not result:
        return 0
    return result[0][0]

def get_average_rating(user_id):
    """Gets user's recipes' average rating from database"""
    sql = """SELECT AVG(rating)
                FROM recipes JOIN ratings ON recipes.id = ratings.recipe_id
                WHERE recipes.user_id = ?"""
    result = db.query(sql, [user_id])[0][0]
    if result:
        return round(result, 1)
    return None

def recent_activity(user_id):
    """Gets user's 5 most recent comments and ratings from database"""
    sql = """SELECT title, id, act.type, act.user_id, act.recipe_id, act.content, act.created
            FROM recipes JOIN
            (SELECT 'comment' AS type, user_id, recipe_id, content as content, created
            FROM comments
            UNION ALL
            SELECT 'rating' AS type, user_id, recipe_id, rating as content, created FROM ratings) as act
            ON recipes.id = act.recipe_id
            WHERE act.user_id = ?
            GROUP BY type, act.recipe_id, content
            ORDER BY act.created DESC
            LIMIT 5"""
    return db.query(sql, [user_id])

def comments_received(user_id):
    """Gets amount of comments total on user's recipes from database"""
    sql = """SELECT COUNT(*)
            FROM recipes r JOIN comments c
            ON r.id = c.recipe_id WHERE r.user_id = ?"""
    return db.query(sql, [user_id])[0][0]

def ratings_received(user_id):
    """Gets amount of ratings total on user's recipes from database"""
    sql = """SELECT COUNT(*)
            FROM recipes r JOIN ratings rt ON r.id = rt.recipe_id WHERE r.user_id = ?"""
    return db.query(sql, [user_id])[0][0]
