import db
from datetime import datetime

valid_menus = ["Appetizer", "Main Course", "Dessert", "Side Dish"]
valid_skills = ["Beginner", "Intermediate", "Advanced"]
valid_tags = ["Vegan", "Vegetarian", "Fish", "Meat", "Chicken", "Pasta", "Salad", "Oven", "Soup"]

def add_item(user_id, title, description, menu, skill):
    sql = """INSERT INTO recipes (user_id, title, description, menu, skill, created)
                VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, title, description, menu, skill, datetime.now().date().isoformat()])

def valid_title(title):
    if len(title) < 3:
        return (False, "Recipe title is too short")
    if len(title) > 100:
        return (False, "Recipe title is too long")
    words = title.split()
    for word in words:
        if not word.isalpha():
            return (False, "Recipe title must consist of only letters")
    return (True, None)

def valid_description(description):
    if len(description) < 5:
        return (False, "Recipe description is too short")
    if len(description) > 1000:
        return (False, "Recipe description is too long")
    return (True, None)

def valid_classes(menu, skill, tags):
    if menu not in valid_menus:
        return (False, "Invalid menu category")
    if skill not in valid_skills:
        return (False, "Invalid skill category")
    for tag in tags:
        if tag not in valid_tags:
            return (False, "Invalid tag")
    return (True, None)

def get_all_items():
    sql = """SELECT id, user_id, title, description, menu, skill, created FROM recipes"""
    return db.query(sql)

def get_user_items(user_id):
    sql = """SELECT id, user_id, title, description, menu, skill, created FROM recipes WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_item(item_id):
    sql = """SELECT id, user_id, title, description, menu, skill, created FROM recipes WHERE id == ?"""
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
    sql = """SELECT id, user_id, title FROM recipes
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
    return db.execute(sql, [recipe_id, tag])

def get_tags(item_id):
    sql = """SELECT recipe_id, tag FROM tags WHERE recipe_id = ?"""
    return db.query(sql, [item_id])

def remove_tags(item_id):
    sql = """DELETE FROM tags
                WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])

def remove_tag(item_id, tag):
    sql = """DELETE FROM tags
                WHERE recipe_id = ? AND tag = ?"""
    return db.execute(sql, [item_id, tag])

def add_comment(user_id, item_id, content):
    sql = """INSERT INTO comments (user_id, recipe_id, content, created) VALUES (?,?,?,?)"""
    return db.execute(sql, [user_id, item_id, content, datetime.now().isoformat()])

def valid_comment(comment):
    if len(comment) > 500:
        return (False, "Comment is too long")
    return (True, None)

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

def valid_rating(rating):
    try:
        rating_value = int(rating)
    except:
        return (False, "Rating in invalid format")
    else:
        if rating_value < 1 or rating_value > 5:
            return (False, "Rating must be between 1 and 5")
    return (True, None)

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