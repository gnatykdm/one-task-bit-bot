-- One-Task-bit-Bot DB Scheme --

-- ENUM's --
CREATE TYPE lan AS ENUM ('UKRANIAN', 'ENGLISH');
CREATE TYPE routine_type AS ENUM ('morning', 'evening');

-- TABLE users
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    user_name VARCHAR(255) NOT NULL UNIQUE,
    language lan NOT NULL DEFAULT 'ENGLISH',
    register_date TIMESTAMP NOT NULL DEFAULT NOW(),
    wake_time TIME DEFAULT NULL,
    sleep_time TIME DEFAULT NULL
);

-- TABLE routines --
CREATE TABLE routines (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    routine_type routine_type NOT NULL,
    routine_name VARCHAR(255) NOT NULL
);

-- TABLE Focuses --
CREATE TABLE focuses (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    duration BIGINT NOT NULL,
    title VARCHAR(225),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
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

-- Daily Stats Table --
CREATE TABLE IF NOT EXISTS daily_stats (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_tasks INT NOT NULL DEFAULT 0,
    created_ideas INT NOT NULL DEFAULT 0,
    stats_day TIMESTAMP NOT NULL DEFAULT NOW()
);

ALTER TABLE daily_stats
ADD COLUMN stats_day_date DATE NOT NULL DEFAULT CURRENT_DATE;

CREATE UNIQUE INDEX IF NOT EXISTS unique_daily_stat_per_user
ON daily_stats (user_id, stats_day_date);

