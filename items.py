import db
from datetime import datetime

def add_item(user_id, title, description, menu, skill):
    sql = """INSERT INTO recipes (user_id, title, description, menu, skill, created)
                VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, title, description, menu, skill, datetime.now().date().isoformat()])

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

def get_popular_items():
    sql = """SELECT id, title, COUNT(*)
                FROM recipes rec JOIN ratings rat JOIN comments c ON rec.id = rat.recipe_id AND rec.id = c.recipe_id
                GROUP BY id"""

def get_classes(item_id):
    sql = """SELECT menu, skill FROM recipes WHERE id = ?"""
    return db.query(sql, [item_id])

def update_item(item_id, user_id, title, description, menu, skill):
    sql = """UPDATE recipes
                SET user_id = ?, title = ?, description = ?, menu = ?, skill = ?
                WHERE id = ?"""
    return db.execute(sql, [user_id, title, description, menu, skill, item_id])

def remove_item(item_id):
    sql = """DELETE FROM recipes
                WHERE id = ?"""
    return db.execute(sql, [item_id])

def find_item(query, tags):
    sql = """SELECT * FROM recipes
            WHERE title LIKE ? OR description LIKE ?"""
    results = db.query(sql, ["%" + query + "%", "%" + query + "%"])
    filtered = []
    if len(tags) != 0:
        for result in results:
            accepted = True
            result_tags = get_tags(result["id"])
            tag_values = [tag["tag"] for tag in result_tags]
            for tag in tags:
                if tag not in tag_values:
                    accepted = False
                    break
            if accepted:
                filtered.append(result)
        return filtered
    return results

def add_tag(recipe_id, tag):
    sql = """INSERT INTO tags (recipe_id, tag) VALUES (?, ?)"""
    db.execute(sql, [recipe_id, tag])

def get_tags(item_id):
    sql = """SELECT * FROM tags WHERE recipe_id = ?"""
    return db.query(sql, [item_id])

def remove_tags(item_id):
    sql = """DELETE FROM tags
                WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])

def add_comment(user_id, item_id, content):
    sql = """INSERT INTO comments (user_id, recipe_id, content, created) VALUES (?,?,?,?)"""
    return db.execute(sql, [user_id, item_id, content, datetime.now().isoformat()])

def get_comments(item_id):
        sql = """SELECT content, user_id, username, c.created FROM comments c JOIN users u ON c.user_id = u.id
                WHERE recipe_id = ?
                ORDER BY c.created"""
        return db.query(sql, [item_id])
        
def remove_comments(item_id):
    sql = """DELETE FROM comments WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])

def add_rating(user_id, item_id, rating):
    sql = """INSERT INTO ratings (user_id, recipe_id, rating, created) VALUES (?,?,?,?)"""
    return db.execute(sql, [user_id, item_id, rating, datetime.now().isoformat()])

def get_avg_rating(item_id):
    sql = """SELECT AVG(rating) as avg, COUNT(rating) as count
                FROM ratings WHERE recipe_id = ?"""
    result = db.query(sql, [item_id])
    if result[0][0] == None:
        return None
    else:
        return (round(result[0]["avg"], 1), result[0]["count"])
    
def remove_ratings(item_id):
    sql = """DELETE FROM ratings WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])
