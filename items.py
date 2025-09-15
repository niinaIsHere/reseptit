import db

def add_item():
    pass

def get_all_items():
    sql = """SELECT * FROM recipes"""
    return db.query(sql)

def get_user_items(user_id):
    sql = """SELECT * FROM recipes WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_item(item_id):
    sql = """SELECT * FROM recipes WHERE id == ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def update_item(item_id, user_id, title, description, menu, skill):
    sql = """UPDATE recipes
                SET user_id = ?, title = ?, description = ?, menu = ?, skill = ?
                WHERE id = ?"""
    return db.execute(sql, [user_id, title, description, menu, skill, item_id])

def remove_item(item_id):
    sql = """DELETE FROM recipes
                WHERE id = ?"""
    return db.execute(sql, [item_id])

def find_item(query):
    sql = """SELECT * FROM recipes WHERE title LIKE ? OR description LIKE ?"""
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def get_tags(item_id):
    sql = """SELECT * FROM tags WHERE recipe_id = ?"""
    return db.query(sql, [item_id])
