import os
import sqlite3


# getting db location
directory = os.path.dirname(os.path.realpath(__file__))
db = os.path.join(directory, 'db', 'price_app.sqlite3')


def create_in_db(**kwargs):
    # connecting to db
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # assigning values to variables
    product_type = kwargs.get('product_type')
    product_name = kwargs.get('product_name')
    location_name = kwargs.get('location_name')
    city = kwargs.get('city')
    general_location = kwargs.get('general_location')
    price = kwargs.get('price')
    currency = kwargs.get('currency')
    unit = kwargs.get('unit')
    date = kwargs.get('date')
    picture = kwargs.get('picture', None)

    # searching for same entry in products
    cur.execute(
        """
        SELECT product_id FROM products
        WHERE product_type = :product_type AND
            product_name = :product_name;
        """,
        {
            'product_type': product_type,
            'product_name': product_name
        }
    )
    try:
        product_id = cur.fetchone()[0]
    except TypeError:
        product_id = None

    # inserting entry to products with no picture
    if product_id is None and picture is None:
        cur.execute(
            """
            INSERT INTO products(product_type, product_name) VALUES(
                :product_type,
                :product_name
            );
            """,
            {
                'product_type': product_type,
                'product_name': product_name
            }
        )
    # inserting entry to products with picture
    elif product_id is None and picture is not None:
        cur.execute(
            """
            INSERT INTO products(product_type, product_name, picture) VALUES(
                :product_type,
                :product_name,
                :picture
            );
            """,
            {
                'product_type': product_type,
                'product_name': product_name,
                'picture': picture
            }
        )

    # getting product_id
    if product_id is None:
        cur.execute(
            """
            SELECT product_id FROM products
            WHERE product_type = :product_type AND
                product_name = :product_name;
            """,
            {
                'product_type': product_type,
                'product_name': product_name
            }
        )
        product_id = cur.fetchone()[0]

    # searching for same entry in locations
    cur.execute(
        """
        SELECT location_id FROM locations
        WHERE location_name = :location_name AND
            city = :city AND
            general_location = :general_location;
        """,
        {
            'location_name': location_name,
            'city': city,
            'general_location': general_location
        }
    )
    try:
        location_id = cur.fetchone()[0]
    except TypeError:
        location_id = None

    # inserting entry to locations
    if location_id is None:
        cur.execute(
            """
            INSERT INTO locations(location_name, city, general_location) VALUES(
                :location_name,
                :city,
                :general_location
            );
            """,
            {
                'location_name': location_name,
                'city': city,
                'general_location': general_location
            }
        )

    # getting location_id
    cur.execute(
        """
        SELECT location_id FROM locations
        WHERE location_name = :location_name AND
            city = :city AND
            general_location = :general_location;
        """,
        {
            'location_name': location_name,
            'city': city,
            'general_location': general_location
        }
    )
    location_id = cur.fetchone()[0]

    # inserting into prices
    cur.execute(
        """
        REPLACE INTO prices VALUES(
            :product_id,
            :location_id,
            :price,
            :currency,
            :unit,
            :date
        );
        """,
        {
            'product_id': product_id,
            'location_id': location_id,
            'price': price,
            'currency': currency,
            'unit': unit,
            'date': date
        }
    )

    conn.commit()
    conn.close()


def search_db(search_phrase):
    # connecting to db
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # searching for entries in db
    cur.execute(
        """
        SELECT products.product_name, products.product_type,
            prices.price, prices.currency, prices.unit, locations.location_name,
            locations.general_location, prices.price_date, locations.city,  
            prices.product_id, prices.location_id, products.picture
        FROM locations
        JOIN prices
        ON locations.location_id = prices.location_id
        JOIN products
        ON prices.product_id = products.product_id
        WHERE locations.location_id IN (
	        SELECT prices.location_id
	        FROM prices
	        WHERE prices.product_id IN (
		        SELECT products.product_id
		        FROM products
		        WHERE product_type LIKE :product_type
	        )
        )
        AND products.product_type LIKE :product_type
        ORDER BY prices.price DESC;
        """,
        {
            'product_type': '%' + search_phrase + '%'
        }
    )
    query = cur.fetchall()
    if query == []:
        cur.execute(
            """
        SELECT products.product_name, products.product_type,
            prices.price, prices.currency, prices.unit, locations.location_name,
            locations.general_location, prices.price_date, locations.city,  
            prices.product_id, prices.location_id, products.picture
        FROM locations
        JOIN prices
        ON locations.location_id = prices.location_id
        JOIN products
        ON prices.product_id = products.product_id
        WHERE locations.location_id IN (
	        SELECT prices.location_id
	        FROM prices
	        WHERE prices.product_id IN (
		        SELECT products.product_id
		        FROM products
		        WHERE product_name LIKE :product_name
	        )
        )
        AND products.product_name LIKE :product_name
        ORDER BY prices.price DESC;
            """,
            {
                'product_name': '%' + search_phrase + '%'
            }
        )
        query = cur.fetchall()

    conn.close()
    return query


# UPDATE PRICE
def update_price_db(**kwargs):
    # connecting to db
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # assigning values to variables
    price = kwargs.get('price')
    currency = kwargs.get('currency')
    unit = kwargs.get('unit')
    price_date = kwargs.get('price_date')
    product_id = kwargs.get('product_id')
    location_id = kwargs.get('location_id')

    # updating prices
    cur.execute(
        """
        UPDATE prices
        SET
            price = :price,
            currency = :currency,
            unit = :unit,
            price_date = :price_date
        WHERE product_id = :product_id AND location_id = :location_id;
        """,
        {
            'price': price,
            'currency': currency,
            'unit': unit,
            'price_date': price_date,
            'product_id': product_id,
            'location_id': location_id
        }
    )
    conn.commit()
    conn.close()


# UPDATE PRODUCT
def update_product_db(**kwargs):
    # connecting to db
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # assigning values to variables
    product_name = kwargs.get('product_name')
    product_type = kwargs.get('product_type')
    product_id = kwargs.get('product_id')
    picture = kwargs.get('picture', None)

    # updating product with no picture
    if picture is None:
        cur.execute(
            """
            UPDATE products
            SET product_name = :product_name, product_type = :product_type
            WHERE product_id = :product_id;
            """,
            {
                'product_name': product_name,
                'product_type': product_type,
                'product_id': product_id
            }
        )

    # updating product with picture
    else:
        cur.execute(
            """
            UPDATE products
            SET
                product_name = :product_name,
                product_type = :product_type,
                picture = :picture
            WHERE product_id = :product_id;
            """,
            {
                'product_name': product_name,
                'product_type': product_type,
                'product_id': product_id,
                'picture': picture
            }
        )
    conn.commit()
    conn.close()

# UPDATE LOCATION


def update_location_db(**kwargs):
    # connecting to db
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # assigning values to variables
    location_name = kwargs.get('location_name')
    city = kwargs.get('city')
    general_location = kwargs.get('general_location')
    location_id = kwargs.get('location_id')

    # updating location
    cur.execute(
        """
        UPDATE locations
        SET
            location_name = :location_name,
            city = :city,
            general_location = :general_location
        WHERE location_id = :location_id;
        """,
        {
            'location_name': location_name,
            'city': city,
            'general_location': general_location,
            'location_id': location_id
        }
    )
    conn.commit()
    conn.close()

# DELETE ENTRY


def delete_db(**kwargs):
    # connecting to db
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    # assigning values to variables
    product_id = kwargs.get('product_id')
    location_id = kwargs.get('location_id')

    # deleting price
    cur.execute(
        """
        DELETE FROM prices
        WHERE product_id = :product_id AND location_id = :location_id;
        """,
        {
            'product_id': product_id,
            'location_id': location_id
        }
    )

    # checking for same product
    cur.execute(
        """
        SELECT product_id
        FROM prices
        WHERE product_id = :product_id;
        """,
        {'product_id': product_id}
    )
    # if no prices for product, deleting product
    if cur.fetchall() == []:
        cur.execute(
            """
            DELETE FROM products
            WHERE product_id = :product_id;
            """,
            {'product_id': product_id}
        )

    # checking for same location
    cur.execute(
        """
        SELECT location_id
        FROM prices
        WHERE location_id = :location_id;
        """,
        {'location_id': location_id}
    )
    # if no prices for location, deleting location
    if cur.fetchall() == []:
        cur.execute(
            """
                DELETE FROM locations
                WHERE location_id = :location_id;
                """,
            {'location_id': location_id}
        )
    conn.commit()
    conn.close()
