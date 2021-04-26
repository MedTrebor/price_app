import os
import sqlite3


directory = os.path.dirname(os.path.realpath(__file__))
db_name = os.path.join(directory, 'price_app.sqlite3')


conn = sqlite3.connect(db_name)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE products(
	product_id INTEGER PRIMARY KEY AUTOINCREMENT,
	product_type TEXT,
	product_name TEXT,
	picture BLOB
    );
    """
)
cur.execute(
    """
    CREATE TABLE locations(
	location_id INTEGER PRIMARY KEY AUTOINCREMENT,
	location_name TEXT,
	general_location TEXT,
	city TEXT
    );
    """
)
cur.execute(
    """
    CREATE TABLE prices(
	product_id INTEGER,
	location_id INTEGER,
	price REAL(9,2),
	price_per_unit REAL(9,2),
	currency TEXT,
	unit TEXT,
	price_date TEXT,
	PRIMARY KEY(product_id, location_id),
	FOREIGN KEY(product_id) REFERENCES products(product_id) ON DELETE CASCADE,
	FOREIGN KEY(location_id) REFERENCES locations(location_id) ON DELETE CASCADE
    );
    """
)

conn.commit()
conn.close()
