CREATE TABLE products(
	product_id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_type TEXT,
	product_name TEXT,
);

CREATE TABLE locations(
	location_id INTEGER PRIMARY KEY AUTOINCREMENT,
	location_name TEXT,
	city TEXT,
	general_location TEXT
);

CREATE TABLE prices(
	product_id INTEGER,
	location_id INTEGER,
	price REAL(9,2),
	currency TEXT,
	unit TEXT,
	price_date TEXT,
	PRIMARY KEY(product_id, location_id),
	FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	FOREIGN KEY(location_id) REFERENCES locations(location_id) ON DELETE CASCADE
);