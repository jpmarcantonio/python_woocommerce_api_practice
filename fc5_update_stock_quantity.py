"""
This script utilizes the WooCommerce API to update the stock quantity of all products in the store.
It sets 'manage_stock' to True and assigns a random stock quantity between 0 and 50 to each product.

Requirements:
- WooCommerce API credentials (consumer_key, consumer_secret) and store URL must be set as environment variables.
  - Set 'WOO_KEY', 'WOO_SECRET', and 'URL' environment variables with the appropriate values.

Usage:
1. Ensure the required environment variables are set.
2. Execute the script to update the stock quantity for all products.

Script Flow:
1. Checks and retrieves WooCommerce API credentials and store URL from environment variables.
2. Creates a WooCommerce API instance using the provided credentials.
3. Retrieves all products from the store in batches of 100 products per page.
4. For each product, checks if the product type is valid for stock management. Only 'simple' and 'variable' product
   types are valid.
5. If valid, sets 'manage_stock' to True and updates the stock quantity with a random value.
6. Logs the details of the updated products.
7. Prints the total number of products whose stock quantity has been updated and the list of invalid product IDs.
"""

from woocommerce import API
import random
import os
import logging

variable_key = "WOO_KEY"
variable_secret = "WOO_SECRET"
url = "URL"

def check_environment_variables(var):
    try:
        os.environ[var]
    except Exception as e:
        logging.exception(f"The environment variable name must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception(f"The environment variable name {e} must be set")

check_environment_variables(variable_key)
check_environment_variables(variable_secret)
check_environment_variables(url)

wcapi = API(
    url=os.getenv(url),
    consumer_key=os.getenv(variable_key),
    consumer_secret=os.getenv(variable_secret),
    version="wc/v3",
    timeout=60
)

page = 1
product_ids = []
invalid_product_ids = []

# get all products from the store
while True:
    r = wcapi.get("products", params={"per_page": 100, 'page': page})
    products = r.json()

    status_code = r.status_code
    response_body = r.content
    if status_code != 200:
        raise Exception(f"Expected status code 200. Got status code {status_code}"
                        f"For more information about your error, see: {response_body}")
    page = page + 1
    if not products:
        break

# for each product check product type, sort to list for logging, make API call to set 'manage_stock' to True and update stock quantity
    for product in products:
        product_id = product["id"]
        stock_quantity = product["stock_quantity"]
        manage_stock = product["manage_stock"]
        product_type = product["type"]
        invalid_product_types = ['external', 'grouped']

        if product_type not in invalid_product_types:
            product_ids.append(product_id)

            data = {'manage_stock': True,
                    'stock_quantity': random.randrange(51)}

            r3 = wcapi.put(f'products/{product_id}', data)

            updated_product = r3.json()
            status_code = r3.status_code
            response_body = r3.content
            if status_code != 200:
                raise Exception(f"Expected status code 200. Got status code {status_code} "
                                f"For more information about your error, see: {response_body}")
            print(f"Product Type: {product_type}, Product ID: {product_id}, Stock Quantity: {updated_product['stock_quantity']}")

        else:
            invalid_product_ids.append(product_id)

print(f"Updated stock quantity on {len(product_ids)} items. \n"
      f"Did not update stock quantity on product ids: {invalid_product_ids} due to being invalid for stock management.")
