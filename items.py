from datetime import datetime
import db

valid_menus = ["Appetizer", "Main Course", "Dessert", "Side Dish"]
valid_skills = ["Beginner", "Intermediate", "Advanced"]
valid_tags = ["Vegan", "Vegetarian", "Fish", "Meat", "Chicken", "Pasta", "Salad", "Oven", "Soup"]

def add_item(user_id, title, description, menu, skill):
    """Add a new item into database"""
    sql = """INSERT INTO recipes (user_id, title, description, menu, skill, created)
                VALUES (?, ?, ?, ?, ?, ?)"""
    db.execute(sql, [user_id, title, description, menu, skill, datetime.now().date().isoformat()])

def valid_title(title):
    """Check if recipe title is valid"""
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
    """Check if recipe description is valid"""
    if len(description) < 5:
        return (False, "Recipe description is too short")
    if len(description) > 1000:
        return (False, "Recipe description is too long")
    return (True, None)

def valid_classes(menu, skill, tags):
    """Check if recipe tags are valid"""
    if menu not in valid_menus:
        return (False, "Invalid menu category")
    if skill not in valid_skills:
        return (False, "Invalid skill category")
    for tag in tags:
        if tag not in valid_tags:
            return (False, "Invalid tag")
    return (True, None)

def get_all_items():
    """Get all recipes from database"""
    sql = """SELECT id, user_id, title, description, menu, skill, created FROM recipes"""
    return db.query(sql)

def get_user_items(user_id):
    """Get all user's recipes from database"""
    sql = """SELECT id, user_id, title, description, menu, skill, created
            FROM recipes WHERE user_id = ?"""
    return db.query(sql, [user_id])

def get_item(item_id):
    """Get recipe info from database by id"""
    sql = """SELECT id, user_id, title, description, menu, skill, created
            FROM recipes WHERE id == ?"""
    result = db.query(sql, [item_id])
    return result[0] if result else None

def get_classes(item_id):
    """Get recipe's categorization information from database"""
    sql = """SELECT menu, skill FROM recipes WHERE id = ?"""
    return db.query(sql, [item_id])

def update_item(item_id, user_id, title, description, menu, skill):
    """Update recipe's info on database"""
    sql = """UPDATE recipes
                SET user_id = ?, title = ?, description = ?, menu = ?, skill = ?
                WHERE id = ?"""
    return db.execute(sql, [user_id, title, description, menu, skill, item_id])

def remove_item(item_id):
    """Remove a recipe drom database by id"""
    sql = """DELETE FROM recipes
                WHERE id = ?"""
    return db.execute(sql, [item_id])

def find_item(query, tags):
    """Get recipes that fit the search's keyword and tags"""
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
    """Add a tag to a recipe"""
    sql = """INSERT INTO tags (recipe_id, tag) VALUES (?, ?)"""
    return db.execute(sql, [recipe_id, tag])

def get_tags(item_id):
    """Get tags on a recipe from database"""
    sql = """SELECT recipe_id, tag FROM tags WHERE recipe_id = ?"""
    return db.query(sql, [item_id])

def remove_tags(item_id):
    """Remove all tags on a recipe"""
    sql = """DELETE FROM tags
                WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])

def remove_tag(item_id, tag):
    """Remove certain tag from recipe"""
    sql = """DELETE FROM tags
                WHERE recipe_id = ? AND tag = ?"""
    return db.execute(sql, [item_id, tag])

def add_comment(user_id, item_id, content):
    """Add a comment to a recipe in database"""
    sql = """INSERT INTO comments (user_id, recipe_id, content, created) VALUES (?,?,?,?)"""
    return db.execute(sql, [user_id, item_id, content, datetime.now().isoformat()])

def valid_comment(comment):
    """Check if user's comment is valid"""
    if len(comment) > 500:
        return (False, "Comment is too long")
    return (True, None)

def get_comments(item_id):
    """Get all comments on a recipe from database"""
    sql = """SELECT content, user_id, username, c.created
            FROM comments c JOIN users u ON c.user_id = u.id
            WHERE recipe_id = ?
            ORDER BY c.created"""
    return db.query(sql, [item_id])

def remove_comments(item_id):
    """Remove all comments on a recipe from database"""
    sql = """DELETE FROM comments WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])

def add_rating(user_id, item_id, rating):
    """Add a rating to a recipe into database"""
    sql = """INSERT INTO ratings (user_id, recipe_id, rating, created) VALUES (?,?,?,?)"""
    return db.execute(sql, [user_id, item_id, rating, datetime.now().isoformat()])

def valid_rating(rating):
    """Check if given rating is valid"""
    try:
        rating_value = int(rating)
    except:
        return (False, "Rating in invalid format")
    else:
        if rating_value < 1 or rating_value > 5:
            return (False, "Rating must be between 1 and 5")
    return (True, None)

def get_avg_rating(item_id):
    """Get the average of a recipe's ratings from database"""
    sql = """SELECT AVG(rating) as avg, COUNT(rating) as count
                FROM ratings WHERE recipe_id = ?"""
    result = db.query(sql, [item_id])
    if result[0][0] is None:
        return None
    return (round(result[0]["avg"], 1), result[0]["count"])

def remove_ratings(item_id):
    """Remove all ratings on a recipe from database"""
    sql = """DELETE FROM ratings WHERE recipe_id = ?"""
    return db.execute(sql, [item_id])

def popular_items():
    """Get 5 most popular recipes on whole application from database,
    based on result calculated from comments and ratings"""
    sql = """SELECT r.id AS id, r.title,
            COUNT(DISTINCT c.id) AS comment_count, COUNT(DISTINCT rt.id) AS rating_count,
            AVG(rt.rating) AS average_rating,
            (COUNT(DISTINCT rt.id) * 0.5 + AVG(rt.rating) * 2 + COUNT(DISTINCT c.id) * 0.3) AS popularity_score
            FROM recipes r
            LEFT JOIN comments c ON r.id = c.recipe_id
            LEFT JOIN ratings rt ON r.id = rt.recipe_id
            GROUP BY r.id, r.title
            ORDER BY popularity_score DESC
            LIMIT 5;"""
    return db.query(sql)

def new_items():
    """Get the 5 newest items on whole application from database"""
    sql = """SELECT id, user_id, title, description, menu, skill, created
                FROM recipes
                ORDER BY id DESC
                LIMIT 5"""
    return db.query(sql)

def latest_user_items(user_id):
    """Get 5 newest recipes uploaded by a user"""
    sql = """SELECT id, user_id, title, description, menu, skill, created
                FROM recipes WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 5"""
    return db.query(sql, [user_id])

def get_by_skill(skill):
    """Get recipes that have certain skill category"""
    sql = """SELECT id, title
                FROM recipes WHERE skill = ?"""
    return db.query(sql, [skill])
