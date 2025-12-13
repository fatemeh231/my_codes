CREATE TABLE phone_book (
    id SERIAL PRIMARY KEY,
    contact_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(100) NOT NULL,
	email VARCHAR(100), --optional
	note TEXT, --optional
	address TEXT --optional
);