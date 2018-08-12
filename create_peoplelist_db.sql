CREATE TABLE `peoplelist`(
    id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    people_id TEXT NOT NULL,
    people_status TEXT,
    people_class TEXT,
    people_number TEXT,
    people_name TEXT,
    borrow_book TEXT
);