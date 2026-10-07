
CREATE TABLE IF NOT EXISTS info (
    info_id SERIAL PRIMARY KEY,
    info_score INT DEFAULT 0,
	info_content TEXT DEFAULT NULL,
    title TEXT,
	insert_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS tag (
    tag_name TEXT PRIMARY KEY,
    UNIQUE (tag_name)
);

CREATE TABLE IF NOT EXISTS info_tag (
    tag_name TEXT,
    info_id INTEGER,

    PRIMARY KEY (tag_name, info_id),
    UNIQUE (tag_name, info_id),

    FOREIGN KEY (info_id)
    REFERENCES info(info_id)
    ON DELETE CASCADE,

    FOREIGN KEY (tag_name)
    REFERENCES tag(tag_name)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS app_user (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    hash_password TEXT NOT NULL,

    UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS permission_user (
	permission_id SERIAL PRIMARY KEY,
	permission TEXT,
	user_id INTEGER,

	FOREIGN KEY (user_id)
    REFERENCES app_user(user_id)
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS login_session (
    key_login SERIAL PRIMARY KEY,
    session_token TEXT,
    user_id INTEGER,
	expire_date DATE DEFAULT (CURRENT_DATE + 7),

    FOREIGN KEY (user_id)
    REFERENCES app_user(user_id)
    ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_info_id
ON info(info_id);

CREATE INDEX IF NOT EXISTS idx_tag_id
ON tag(tag_name);
