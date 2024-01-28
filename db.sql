CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
CREATE UNIQUE INDEX username ON users (username);

CREATE TABLE tweets (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    contents TEXT NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE likes (
    tweet_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (tweet_id) REFERENCES tweets(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);