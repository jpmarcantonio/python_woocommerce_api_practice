"""
Working on a script to clean up demo store. delete all products without images.
Example command to run script: python Jenkins-dev-Frontiers_317_delete_products.py --confirm-delete yes
"""

import argparse
import logging
import os
from woocommerce import API

# defining argument parser
parser = argparse.ArgumentParser(description="Delete products with no images from the database")
parser.add_argument("--confirm-delete", choices=["yes", "no"], default="no", help="Confirm deletion (yes/no)")

# parse command-line arguments
args =parser.parse_args()
confirm_delete = args.confirm_delete.lower()

logging.basicConfig(level=logging.INFO)

# dev variables
woo_key = 'WOO_KEY'
woo_secret = 'WOO_SECRET'

# local variables
# woo_key = 'MYSITE2_API_KEY'
# woo_secret = 'MYSITE2_API_SECRET'

def check_env_variables(variable_name):
    try:
        os.environ[variable_name]
    except KeyError as e:
        error_message = f"The environment variable must be set: {e}"
        logging.exception(error_message)
        raise Exception(error_message)

check_env_variables(woo_key)
check_env_variables(woo_secret)

wcapi = API(
    url="http://dev.bootcamp.store.supersqa.com/",
    # url="http://localhost:8888/mysite2",
    consumer_key=os.getenv(woo_key),
    consumer_secret=os.getenv(woo_secret),
    version="wc/v3",
    timeout=60
)

# get all products from db
page = 1
while True:
    r = wcapi.get("products", params={"per_page": 100, 'page': page})
    products = r.json()
    page = page + 1
    if not products:  # no more products
        break

    # add products into lists. total products, and products with no images to be deleted
    total_products = [product['id'] for product in products]
    products_to_delete = [product['id'] for product in products if not product['images']]

# take user input and delete products
def delete_confirm():
    if confirm_delete == "yes":
        logging.info(f'Deleting products from database...')
        for i in products_to_delete:
            wcapi.delete(f"products/{i}", params={"force": True})
    else:
        logging.info(f"No products have been deleted.")

delete_confirm()
logging.info(f"{len(products_to_delete)} Products deleted. {len(total_products) - len(products_to_delete)} Products remaining in your store.")
