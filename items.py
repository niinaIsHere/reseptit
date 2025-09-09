import db

def add_item():
    pass

def get_user_items():
    sql = """SELECT * FROM recipes"""
    return db.query(sql)

def get_item(item_id):
    sql = """SELECT * FROM recipes WHERE id == ?"""
    return db.query(sql, [item_id])[0]

def update_item(item_id, user_id, title, description, menu, skill):
    sql = """UPDATE recipes
                SET user_id = ?, title = ?, description = ?, menu = ?, skill = ?
                WHERE id = ?"""
    return db.execute(sql, [user_id, title, description, menu, skill, item_id])

def remove_item(item_id):
    sql = """DELETE FROM recipes
                WHERE id = ?"""
    return db.execute(sql, [item_id])
