##### upgrade #####
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "email" VARCHAR(64) NOT NULL UNIQUE,
    "password" BYTEA NOT NULL,
    "image_uid" VARCHAR(64)
);
CREATE TABLE IF NOT EXISTS "series" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "year" SMALLINT NOT NULL,
    "description" TEXT,
    "image_uid" VARCHAR(64),
    "creator_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "item" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL,
    "description" TEXT,
    "identify_number" INT,
    "image_uid" VARCHAR(64),
    "series_id" INT NOT NULL REFERENCES "series" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "useritemlink" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "item_id" INT NOT NULL REFERENCES "item" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "usertoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(128) NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
