from sendo_database import insert_product_data, psycopg2, hostname, username, pwd, port_id


def reset_table(conn):
    """
    Resets (truncates) the `products` table in the database.

    Parameters:
        conn (psycopg2 connection): Active database connection.
    """
    try:
        with conn.cursor() as cur:
            # Truncate the table and reset the primary key sequence
            cur.execute("TRUNCATE TABLE products RESTART IDENTITY;")
            conn.commit()
            print("Table `products` truncated successfully.")
    except psycopg2.Error as db_error:
        print("Database error while truncating table:", db_error)
    except Exception as e:
        print("Unexpected error while truncating table:", e)


def save_products_to_db(products, reset_flag=False):
    """
    Connects to the database and saves product data.
    Optionally resets the table before saving.

    Parameters:
        products (list of tuples or dicts): List of product data to insert into the database.
        reset_flag (bool): If True, resets the table before inserting data.
    """
    try:
        # Connect to the database
        with psycopg2.connect(
            host=hostname,
            dbname='sendo_practice_database',
            user=username,
            password=pwd,
            port=port_id
        ) as conn:
            print("Database connection established successfully.")

            # Reset the table if reset_flag is True
            if reset_flag:
                print("Resetting the database table...")
                reset_table(conn)

            # Insert the products
            insert_product_data(conn, products)
            print("Data saved to the database successfully.")
    except psycopg2.Error as db_error:
        print("Database error while saving products:", db_error)
    except Exception as e:
        print("Unexpected error while saving products:", e)