BEGIN;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  uniqueid INTEGER NOT NULL,
  field_2 TEXT NOT NULL,
  email TEXT NOT NULL,
  hash BLOB,
  hint TEXT NOT NULL,
  field_6 TEXT NOT NULL
);

CREATE INDEX users_email_idx ON users(email);

COMMIT;
