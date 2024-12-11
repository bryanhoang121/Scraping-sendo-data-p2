import time
import json
from sendo_session import fetch_product_links
from sendo_extractor import fetch_product_details
from db_connection import save_products_to_db, reset_table  # Import reset_table function
import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('config.env')

# Retrieve database connection parameters from environment variables
hostname = os.getenv('DB_HOST')
database = os.getenv('DB_DATABASE')
username = os.getenv('DB_USERNAME')
pwd = os.getenv('DB_PASSWORD')
port_id = int(os.getenv('DB_PORT'))

def main(reset=False):
    # URL of the main page
    url = 'https://www.sendo.vn/cong-nghe?'

    # Reset the table if the reset flag is True
    if reset:
        try:
            print("Resetting the database table...")
            # Connect to the database
            with psycopg2.connect(
                host=hostname,
                dbname=database,
                user=username,
                password=pwd,
                port=port_id
            ) as conn:
                reset_table(conn)  # Pass the connection object to reset_table
            print("Table reset successfully.")
        except Exception as e:
            print(f"Error resetting the table: {e}")
            return

    # List to store scraped product data
    product_data = []

    # Fetch product links
    print("Fetching product links...")
    product_urls = fetch_product_links(url)
    print(f"Found {len(product_urls)} product URLs.")

    # Process individual products
    for index, product_url in enumerate(product_urls[:1]):  # Limit to 1 for testing
        try:
            # Ensure the URL starts with "http"
            if not product_url.startswith("http"):
                product_url = f"https://www.sendo.vn{product_url}"

            print(f"\nFetching product {index + 1}: {product_url}")
            product_details = fetch_product_details(product_url)
            product_data.append(product_details)

            # Debug: Print fetched product details
            print(f"Fetched product details: {product_details}")
            time.sleep(2)  # Avoid overloading the server
        except Exception as e:
            print(f"Error processing product {index + 1}: {e}")

    # Save the data to a JavaScript file
    js_file_path = "product_data.js"
    try:
        with open(js_file_path, "w", encoding="utf-8") as js_file:
            js_file.write("const productData = ")
            json.dump(product_data, js_file, ensure_ascii=False, indent=4)
            js_file.write(";")  # End JavaScript variable definition
        print(f"Data saved successfully to {js_file_path}")
    except Exception as e:
        print(f"Error saving to JavaScript file: {e}")

    # Save data to the database
    try:
        print("Saving data to the database...")
        save_products_to_db(product_data)  # Pass raw data directly to the database module
        print("Data saved to the database successfully.")
    except Exception as e:
        print(f"Error saving data to the database: {e}")

if __name__ == "__main__":
    # Set `reset=True` to reset the table on each run
    main(reset=True)