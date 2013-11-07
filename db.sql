BEGIN;

CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  userid INTEGER NOT NULL,
  username TEXT,
  email TEXT NOT NULL,
  hash BLOB,
  hint TEXT NOT NULL
);

CREATE INDEX users_username_idx ON users(username);
CREATE INDEX users_email_idx ON users(email);

COMMIT;
