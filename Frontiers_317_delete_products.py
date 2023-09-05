"""
Working on a script to clean up demo store. delete all products without images.
"""

import logging
import os
from woocommerce import API

logging.basicConfig(level=logging.INFO)

env_variable_key = 'MYSITE2_API_KEY'
env_variable_secret = 'MYSITE2_API_SECRET'

def check_env_variables(variable_name):
    try:
        os.environ[variable_name]
    except KeyError as e:
        error_message = f"The environment variable must be set: {e}"
        logging.exception(error_message)
        raise Exception(error_message)

check_env_variables(env_variable_key)
check_env_variables(env_variable_secret)

wcapi = API(
    url="http://localhost:8888/mysite2",
    consumer_key=os.getenv(env_variable_key),
    consumer_secret=os.getenv(env_variable_secret),
    version="wc/v3",
    timeout=60
)

page = 1
total_products = []
products_to_delete = []

# get all products from db
while True:
    r = wcapi.get("products", params={"per_page": 100, 'page': page})
    products = r.json()
    page = page + 1
    if not products:  # no more products
        break

    # add products into lists. total products and products with no images to be deleted
    for product in products:
        total_products.append(product['id'])
        if not product['images']:
            products_to_delete.append(product['id'])

# take user input and delete products
def delete_confirm():
    logging.info(f"There are {len(total_products)} products currently in your store.")
    delete = input(f"Are you sure you want to permanently delete {len(products_to_delete)} products? (Yes / N):").lower()

    if delete in ['yes', 'y']:
        logging.info(f'Deleting products from database...')
        for i in products_to_delete:
            wcapi.delete(f"products/{i}", params={"force": True})
    else:
        logging.info(f"No products have been deleted.")

delete_confirm()
logging.info(f"{len(products_to_delete)} Products deleted. {len(total_products) - len(products_to_delete)} Products remaining in your store.")
