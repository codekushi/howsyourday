CREATE TABLE users(
username VARCHAR PRIMARY KEY,
firstname VARCHAR NOT NULL,
lastname VARCHAR NOT NULL,
email VARCHAR CHECK (email ~* '^[A-Za-z0-9._%-]+@[A-Za-z0-9.-]+[.][A-Za-z]+$'),
password VARCHAR NOT NULL,
profile_pic VARCHAR SET DEFAULT 'avatar.png');
