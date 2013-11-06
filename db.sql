BEGIN;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uniqueid INTEGER NOT NULL,
  field_2 TEXT,
  email TEXT,
  hash BLOB,
  hint TEXT,
  field_6 TEXT
);

CREATE INDEX users_email_idx ON users(email);

COMMIT;
