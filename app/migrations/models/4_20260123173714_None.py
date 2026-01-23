from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "Doc" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(64) NOT NULL,
    "tag" VARCHAR(128) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "Operation" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(32) NOT NULL
);
CREATE TABLE IF NOT EXISTS "User" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "username" VARCHAR(32) NOT NULL UNIQUE,
    "email" VARCHAR(128) NOT NULL UNIQUE,
    "hashed_pwd" VARCHAR(128) NOT NULL,
    "phone_number" VARCHAR(11) UNIQUE,
    "active" BOOL NOT NULL DEFAULT True
);
CREATE TABLE IF NOT EXISTS "Plan" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(32) NOT NULL,
    "content" VARCHAR(1024) NOT NULL,
    "user_id" INT REFERENCES "User" ("id") ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS "Category" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(32) NOT NULL,
    "icon" VARCHAR(32) NOT NULL,
    "color" VARCHAR(7) NOT NULL,
    "is_star" BOOL NOT NULL DEFAULT False,
    "plan_id" INT REFERENCES "Plan" ("id") ON DELETE SET NULL,
    "user_id" INT NOT NULL REFERENCES "User" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Card" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "title" VARCHAR(32) NOT NULL,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "review_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "review_times" INT NOT NULL DEFAULT 0,
    "summary" VARCHAR(1024) NOT NULL DEFAULT '',
    "description" TEXT NOT NULL,
    "is_star" BOOL NOT NULL DEFAULT False,
    "category_id" INT NOT NULL REFERENCES "Category" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "User" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "Record" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "create_at" DATE NOT NULL,
    "operation_id" INT NOT NULL REFERENCES "Operation" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "User" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "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"
    "jDHvDmVyHX/wHOqbUp"
)
