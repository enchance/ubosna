-- upgrade --
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "auth_account" (
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "id" UUID NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_superuser" BOOL NOT NULL  DEFAULT False,
    "is_verified" BOOL NOT NULL  DEFAULT False,
    "username" VARCHAR(50) NOT NULL  DEFAULT '',
    "display" VARCHAR(50) NOT NULL  DEFAULT '',
    "firstname" VARCHAR(191) NOT NULL  DEFAULT '',
    "midname" VARCHAR(191) NOT NULL  DEFAULT '',
    "lastname" VARCHAR(191) NOT NULL  DEFAULT '',
    "civil" VARCHAR(20) NOT NULL  DEFAULT '',
    "bday" DATE,
    "avatar" VARCHAR(255) NOT NULL  DEFAULT '',
    "status" VARCHAR(20) NOT NULL  DEFAULT '',
    "bio" VARCHAR(191) NOT NULL  DEFAULT '',
    "country" VARCHAR(2) NOT NULL  DEFAULT '',
    "zipcode" VARCHAR(20) NOT NULL  DEFAULT '',
    "timezone" VARCHAR(10) NOT NULL  DEFAULT '+08:00',
    "currency" VARCHAR(5) NOT NULL  DEFAULT 'PHP',
    "metadata" JSONB NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_auth_accoun_email_3074e7" ON "auth_account" ("email");
CREATE TABLE IF NOT EXISTS "core_taxo" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(50) NOT NULL,
    "display" VARCHAR(50) NOT NULL  DEFAULT '',
    "description" VARCHAR(191) NOT NULL  DEFAULT '',
    "taxotype" SMALLINT NOT NULL  DEFAULT 1,
    "sort" SMALLINT NOT NULL  DEFAULT 100,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_global" BOOL NOT NULL  DEFAULT False,
    "account_id" UUID REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "parent_id" INT REFERENCES "core_taxo" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_core_taxo_name_69eee2" UNIQUE ("name", "taxotype")
);
CREATE INDEX IF NOT EXISTS "idx_core_taxo_taxotyp_094828" ON "core_taxo" ("taxotype");
CREATE TABLE IF NOT EXISTS "auth_group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(191) NOT NULL UNIQUE,
    "summary" TEXT NOT NULL,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_auth_group_name_eb59d9" ON "auth_group" ("name");
CREATE TABLE IF NOT EXISTS "auth_account_groups" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "group_id" INT NOT NULL REFERENCES "auth_group" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_auth_accoun_account_5c16f9" UNIQUE ("account_id", "group_id")
);
CREATE TABLE IF NOT EXISTS "auth_perm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(191) NOT NULL UNIQUE,
    "code" VARCHAR(30) NOT NULL UNIQUE,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "auth_account_perms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "perm_id" INT NOT NULL REFERENCES "auth_perm" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_auth_accoun_account_57d88a" UNIQUE ("account_id", "perm_id")
);
CREATE TABLE IF NOT EXISTS "auth_group_perms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "group_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "perm_id" INT NOT NULL REFERENCES "auth_perm" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_auth_group__group_i_03e28e" UNIQUE ("group_id", "perm_id")
);
CREATE TABLE IF NOT EXISTS "auth_token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(128) NOT NULL UNIQUE,
    "expires" TIMESTAMPTZ NOT NULL,
    "is_blacklisted" BOOL NOT NULL  DEFAULT False,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_auth_token_expires_0eb57d" ON "auth_token" ("expires");
