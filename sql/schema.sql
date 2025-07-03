-- One-Task-bit-Bot DB Scheme --

-- ENUM's --
CREATE TYPE lan AS ENUM ('UKRANIAN', 'ENGLISH');

-- TABLE users
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    language lan NOT NULL DEFAULT 'ENGLISH',
    register_date TIMESTAMP NOT NULL DEFAULT NOW()
);

-- TABLE tasks
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_name VARCHAR(255) NOT NULL,
    status BOOLEAN NOT NULL DEFAULT FALSE,
    start_time TIMESTAMP,
    creation_date TIMESTAMP NOT NULL DEFAULT NOW()
);

-- TABLE ideas
CREATE TABLE ideas (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    idea_name VARCHAR(255) NOT NULL UNIQUE,
    creation_date TIMESTAMP NOT NULL DEFAULT NOW()
);


