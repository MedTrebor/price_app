import sqlite3
import io

def create_in_db(**kwargs):
    # connecting to db
    conn = sqlite3.connect('./db/price_app.sqlite3')
    cur = conn.cursor()

    # assigning values to variables
    product_type = kwargs.get('product_type')
    product_name = kwargs.get('product_name')
    picture = kwargs.get('picture', None)
    location_name = kwargs.get('location_name')
    city = kwargs.get('city')
    general_location = kwargs.get('general_location')
    price = kwargs.get('price')
    unit = kwargs.get('unit')
    date = kwargs.get('date')

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

    # inserting entry to products
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
                'picture': picture.getvalue()
            }
        )

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
                'product_name': product_name,
            }
        )
        product_id = cur.fetchone()[0]

    # getting location_id
    if location_id is None:
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
            :unit,
            :date
        );
        """,
        {
            'product_id': product_id,
            'location_id': location_id,
            'price': price,
            'unit': unit,
            'date': date
        }
    )

    conn.commit()

