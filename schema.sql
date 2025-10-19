CREATE TABLE IF NOT EXISTS users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	password_hash TEXT,
	created TEXT
);

CREATE TABLE IF NOT EXISTS recipes (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	title TEXT,
	description TEXT,
	menu TEXT,
	skill TEXT,
	created TEXT
);

CREATE TABLE IF NOT EXISTS comments (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	recipe_id INTEGER REFERENCES recipes,
	content TEXT,
	created TEXT
);

CREATE TABLE IF NOT EXISTS ratings (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	recipe_id INTEGER REFERENCES recipes,
	rating INTEGER,
	created TEXT
);

CREATE TABLE IF NOT EXISTS tags (
	id INTEGER PRIMARY KEY,
	recipe_id INTEGER REFERENCES recipes,
	tag TEXT
);

CREATE TABLE IF NOT EXISTS profiles (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	bio TEXT
);
