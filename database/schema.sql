CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    password TEXT,
    role TEXT CHECK(role IN ('student','admin','expert'))
);

CREATE TABLE student_profile (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    education TEXT,
    interests TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE questions (
    question_id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT,
    domain TEXT
);

CREATE TABLE answers (
    answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    question_id INTEGER,
    answer TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(question_id) REFERENCES questions(question_id)
);

CREATE TABLE branches (
    branch_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
);

CREATE TABLE branch_weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER,
    branch_id INTEGER,
    weight INTEGER,
    FOREIGN KEY(question_id) REFERENCES questions(question_id),
    FOREIGN KEY(branch_id) REFERENCES branches(branch_id)
);

CREATE TABLE results (
    result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    recommended_branch TEXT,
    score REAL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE branch_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    category TEXT NOT NULL,
    question_index INTEGER UNIQUE NOT NULL
);

