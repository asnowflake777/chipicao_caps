##### upgrade #####
ALTER TABLE "user" ALTER COLUMN "password" TYPE VARCHAR(128);
##### downgrade #####
ALTER TABLE "user" ALTER COLUMN "password" TYPE BYTEA;
