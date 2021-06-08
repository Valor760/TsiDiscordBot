CREATE TABLE IF NOT EXISTS students(
    UserID integer PRIMARY KEY,
    StudentCode integer,
    StudentName text,
    GroupNum text
);

CREATE TABLE IF NOT EXISTS studentDB(
    StudentCode integer PRIMARY KEY,
    StudentName text,
    GroupNum text
);
