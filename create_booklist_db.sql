CREATE TABLE booklist(
	`id` INTEGER PRIMARY KEY ASC AUTOINCREMENT,
	`book_id` TEXT NOT NULL,
	`book_name` TEXT,
	`if_borrow` TEXT,
	`borrow_date`TEXT,
	`people_id` TEXT,
	`borrow_status` TEXT,
	`borrow_class` TEXT,
	`people_number` TEXT,
	`people_name` TEXT,
	`borrow_time` TEXT
);