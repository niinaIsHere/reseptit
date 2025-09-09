CREATE TABLE users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	password_hash TEXT
);

CREATE TABLE recipes (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	title TEXT,
	description TEXT,
	menu INTEGER,
	skill INTEGER
);

CREATE TABLE options (
	id INTEGER PRIMARY KEY,
	recipe_id INTEGER REFERENCES recipes,
	category TEXT,
	choice TEXT
);

CREATE TABLE comments (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	recipe_id INTEGER REFERENCES recipes,
	content TEXT
);

CREATE TABLE ratings (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users,
	recipe_id INTEGER REFERENCES recipes,
	score INTEGER
);


