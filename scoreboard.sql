CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS course(
  course_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  course_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS stream(
  stream_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  stream_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS batch(
  batch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  course_id UUID REFERENCES course (course_id) ON DELETE CASCADE,
  stream_id UUID REFERENCES stream (stream_id) ON DELETE CASCADE,
  batch_name VARCHAR NOT NULL,
  year integer NOT NULL,
  UNIQUE (course_id, stream_id, batch_name, year)
);

CREATE TABLE IF NOT EXISTS campus(
  campus_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  campus_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS color(
  color_id SERIAL PRIMARY KEY,
  color_name VARCHAR UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
  user_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR NOT NULL,
  password VARCHAR NOT NULL DEFAULT "$2b$12$GifHVzEwMmeQfkKJVDXdSu9dTp7CHx7CYVNeoPix5dmF3y15TJzre",
  color INTEGER REFERENCES color (color_id),
  email1 VARCHAR NOT NULL,
  email2 VARCHAR,
  phone1 VARCHAR NOT NULL,
  phone2 VARCHAR,
  batch UUID REFERENCES batch (batch_id),
  campus UUID REFERENCES campus (campus_id)
);