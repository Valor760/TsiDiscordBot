CREATE TABLE IF NOT EXISTS students(
    UserID integer PRIMARY KEY,
    StudentCode integer,
    StudentName text
);

CREATE TABLE IF NOT EXISTS roles(
    RoleName text PRIMARY KEY,
    RoleID integer
);