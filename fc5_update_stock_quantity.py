"""
Working on a script to update the stock quantity of all items in the store. The script will update the quantity
of each item to a random number between 0 - 50

"manage_stock" must be True in order to update stock quantity
"""
from woocommerce import API
import random
import os
import logging

variable_key = "WOO_KEY"
variable_secret = "WOO_SECRET"
url = "URL"

def check_environment_variables():
    try:
        os.environ[variable_key]
    except Exception as e:
        logging.exception(f"The environment variable name must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception(f"The environment variable name {e} must be set")

    try:
        os.environ[variable_secret]
    except Exception as e:
        logging.exception(f"The environment variable name must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception(f"The environment variable name {e} must be set")

    try:
        os.environ[url]
    except Exception as e:
        logging.exception(f"The environment variable name must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception(f"The environment variable name {e} must be set")

check_environment_variables()

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
