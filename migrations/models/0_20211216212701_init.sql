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
    "status" VARCHAR(20) NOT NULL  DEFAULT '',
    "bio" VARCHAR(191) NOT NULL  DEFAULT '',
    "country" VARCHAR(2) NOT NULL  DEFAULT '',
    "zipcode" VARCHAR(20) NOT NULL  DEFAULT '',
    "timezone" VARCHAR(10) NOT NULL  DEFAULT '+08:00',
    "currency" VARCHAR(5) NOT NULL  DEFAULT 'PHP',
    "lang" VARCHAR(2) NOT NULL  DEFAULT 'en',
    "metadata" JSONB
);
CREATE INDEX IF NOT EXISTS "idx_auth_accoun_deleted_112596" ON "auth_account" ("deleted_at");
CREATE INDEX IF NOT EXISTS "idx_auth_accoun_email_3074e7" ON "auth_account" ("email");
CREATE TABLE IF NOT EXISTS "auth_group" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(191) NOT NULL UNIQUE,
    "description" VARCHAR(191) NOT NULL  DEFAULT ''
);
CREATE TABLE IF NOT EXISTS "auth_xaccountgroups" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "group_id" INT NOT NULL REFERENCES "auth_group" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "auth_perm" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "code" VARCHAR(30) NOT NULL UNIQUE,
    "description" VARCHAR(191) NOT NULL  DEFAULT ''
);
CREATE TABLE IF NOT EXISTS "auth_xaccountperms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "author_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "perm_id" INT NOT NULL REFERENCES "auth_perm" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "auth_xgroupperms" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "group_id" INT NOT NULL REFERENCES "auth_group" ("id") ON DELETE CASCADE,
    "perm_id" INT NOT NULL REFERENCES "auth_perm" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "auth_token" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "token" VARCHAR(128) NOT NULL UNIQUE,
    "expires" TIMESTAMPTZ NOT NULL,
    "is_blacklisted" BOOL NOT NULL  DEFAULT False,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_auth_token_expires_0eb57d" ON "auth_token" ("expires");
CREATE TABLE IF NOT EXISTS "core_media" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "url" VARCHAR(256) NOT NULL UNIQUE,
    "filename" VARCHAR(199) NOT NULL,
    "width" SMALLINT,
    "height" SMALLINT,
    "label" VARCHAR(191) NOT NULL  DEFAULT '',
    "size" SMALLINT,
    "status" VARCHAR(20) NOT NULL,
    "mediatype" SMALLINT NOT NULL  DEFAULT 1,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "metadata" JSONB,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_core_media_deleted_becbda" ON "core_media" ("deleted_at");
CREATE INDEX IF NOT EXISTS "idx_core_media_mediaty_e27c92" ON "core_media" ("mediatype");
CREATE TABLE IF NOT EXISTS "core_option" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(20) NOT NULL,
    "value" VARCHAR(191) NOT NULL,
    "optiontype" VARCHAR(10) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "account_id" UUID REFERENCES "auth_account" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_core_option_optiont_406baa" ON "core_option" ("optiontype");
CREATE TABLE IF NOT EXISTS "core_taxo" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(50) NOT NULL,
    "display" VARCHAR(50) NOT NULL  DEFAULT '',
    "label" VARCHAR(191) NOT NULL  DEFAULT '',
    "description" VARCHAR(191) NOT NULL  DEFAULT '',
    "sort" SMALLINT NOT NULL  DEFAULT 100,
    "taxotype" VARCHAR(10) NOT NULL,
    "is_active" BOOL NOT NULL  DEFAULT True,
    "is_global" BOOL NOT NULL  DEFAULT False,
    "account_id" UUID REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "parent_id" INT REFERENCES "core_taxo" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_core_taxo_taxotyp_094828" ON "core_taxo" ("taxotype");
CREATE TABLE IF NOT EXISTS "trades_broker" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(191) NOT NULL UNIQUE,
    "label" VARCHAR(191) NOT NULL  DEFAULT '',
    "brokerno" VARCHAR(191) NOT NULL  DEFAULT '',
    "site" VARCHAR(255) NOT NULL  DEFAULT '',
    "currency" VARCHAR(5) NOT NULL  DEFAULT 'USD',
    "is_active" BOOL NOT NULL  DEFAULT True,
    "metadata" JSONB,
    "logo_id" INT NOT NULL REFERENCES "core_media" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_trades_brok_deleted_7af817" ON "trades_broker" ("deleted_at");
CREATE TABLE IF NOT EXISTS "trades_xaccountbrokers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "wallet" DECIMAL(19,8) NOT NULL  DEFAULT 0,
    "traded" DECIMAL(19,8) NOT NULL  DEFAULT 0,
    "status" VARCHAR(20) NOT NULL  DEFAULT 'active',
    "is_primary" BOOL NOT NULL  DEFAULT False,
    "metadata" JSONB,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "broker_id" INT NOT NULL REFERENCES "trades_broker" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_trades_xacc_deleted_a95d16" ON "trades_xaccountbrokers" ("deleted_at");
CREATE TABLE IF NOT EXISTS "trades_pool" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "currency" VARCHAR(20) NOT NULL,
    "amount" DECIMAL(20,8) NOT NULL,
    "costave" DECIMAL(23,8) NOT NULL,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_trades_pool_account_bcd835" UNIQUE ("account_id", "currency")
);
CREATE INDEX IF NOT EXISTS "idx_trades_pool_deleted_5ce4d3" ON "trades_pool" ("deleted_at");
CREATE INDEX IF NOT EXISTS "idx_trades_pool_currenc_85639a" ON "trades_pool" ("currency");
CREATE TABLE IF NOT EXISTS "archiver" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "amount" DECIMAL(20,8) NOT NULL,
    "pool_id" INT NOT NULL REFERENCES "trades_pool" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_archiver_deleted_e45e43" ON "archiver" ("deleted_at");
CREATE TABLE IF NOT EXISTS "trades_security" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(10) NOT NULL,
    "label" VARCHAR(191) NOT NULL  DEFAULT '',
    "tickertype" VARCHAR(10) NOT NULL  DEFAULT 'crypto',
    "metadata" JSONB,
    "exchange_id" INT NOT NULL REFERENCES "core_taxo" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_trades_secu_deleted_dd0c04" ON "trades_security" ("deleted_at");
CREATE TABLE IF NOT EXISTS "trades_trade" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "deleted_at" TIMESTAMPTZ,
    "updated_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "created_at" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "action" SMALLINT NOT NULL,
    "price" DECIMAL(23,8) NOT NULL,
    "basecurr" VARCHAR(20) NOT NULL,
    "quotecurr" VARCHAR(20) NOT NULL,
    "amount" DECIMAL(23,8) NOT NULL,
    "storedamount" DECIMAL(23,8) NOT NULL,
    "gross" DECIMAL(23,8) NOT NULL,
    "feesmain" DECIMAL(23,8),
    "feescurr" VARCHAR(10) NOT NULL,
    "total" DECIMAL(23,8)   DEFAULT 0,
    "leverage" SMALLINT,
    "tradetype" VARCHAR(20) NOT NULL,
    "status" VARCHAR(20) NOT NULL  DEFAULT '',
    "note" VARCHAR(255) NOT NULL  DEFAULT '',
    "is_closed" BOOL NOT NULL  DEFAULT False,
    "metadata" JSONB,
    "account_id" UUID NOT NULL REFERENCES "auth_account" ("id") ON DELETE CASCADE,
    "broker_id" INT NOT NULL REFERENCES "trades_broker" ("id") ON DELETE CASCADE,
    "exchange_id" INT NOT NULL REFERENCES "core_taxo" ("id") ON DELETE CASCADE,
    "pool_id" INT NOT NULL REFERENCES "trades_pool" ("id") ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS "idx_trades_trad_deleted_16353f" ON "trades_trade" ("deleted_at");
CREATE INDEX IF NOT EXISTS "idx_trades_trad_action_e7fe84" ON "trades_trade" ("action");
CREATE INDEX IF NOT EXISTS "idx_trades_trad_basecur_061e35" ON "trades_trade" ("basecurr");
CREATE INDEX IF NOT EXISTS "idx_trades_trad_quotecu_1fbe6d" ON "trades_trade" ("quotecurr");
CREATE INDEX IF NOT EXISTS "idx_trades_trad_tradety_ac4f40" ON "trades_trade" ("tradetype");
CREATE INDEX IF NOT EXISTS "idx_trades_trad_is_clos_3c39ff" ON "trades_trade" ("is_closed");
CREATE TABLE IF NOT EXISTS "trades_xtradetags" (
    "trade_id" INT NOT NULL REFERENCES "trades_trade" ("id") ON DELETE CASCADE,
    "taxo_id" INT NOT NULL REFERENCES "core_taxo" ("id") ON DELETE CASCADE
);
