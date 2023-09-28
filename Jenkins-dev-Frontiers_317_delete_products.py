"""
Working on a script to clean up demo store. delete all products without images.
Example command to run script: python Jenkins-dev-Frontiers_317_delete_products.py --confirm-delete yes

To run this script you must set these environment variables in your system environment:
woo_key = <your Woocommerce consumer key as 'WOO_KEY'>,
woo_secret = <your Woocommerce consumer secret as 'WOO_SECRET',
url = <the url for the site on which you will run this script as 'URL'>.

URL for dev site: http://dev.bootcamp.store.supersqa.com/

"""

import argparse
import logging
import os
from woocommerce import API

# dev environment variables
woo_key = 'WOO_KEY'
woo_secret = 'WOO_SECRET'
url = 'URL'

# local environment variables
# woo_key = 'MYSITE2_API_KEY'
# woo_secret = 'MYSITE2_API_SECRET'
# url = 'URL'

# environment variable descriptions for logging purposes
description_woo_key = 'Woocommerce Consumer Key'
description_woo_secret = 'Woocommerce Consumer Secret'
description_url = 'URL to the site on which you will perform this operation'


def check_env_variables(variable_name, variable_desc):
    try:
        os.environ[variable_name]
    except KeyError as e:
        error_message = f"The environment variable must be set: {e}. You must set your {variable_desc} in your system environment. \n" \
                        f"Here is information on how to generate an API key for your woocommerce site: " \
                        f"https://woocommerce.com/document/woocommerce-rest-api/#section-2 \n" \
                        f"Please see provided information on how to set environment variables for your specific environment. \n" \
                        f"Windows: https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/set_1 \n" \
                        f"Ubuntu Linux: https://askubuntu.com/questions/730/how-do-i-set-environment-variables \n" \
                        f"Mac: https://support.apple.com/guide/terminal/use-environment-variables-apd382cc5fa-4f58-4449-b20a-41c53c006f8f/mac"

        logging.exception(error_message)
        raise Exception(error_message)

check_env_variables(woo_key, description_woo_key)
check_env_variables(woo_secret, description_woo_secret)
check_env_variables(url, description_url)

wcapi = API(
    url=os.getenv(url),
    consumer_key=os.getenv(woo_key),
    consumer_secret=os.getenv(woo_secret),
    version="wc/v3",
    timeout=60
)

total_products = []
products_to_delete = []

# get all products from db
page = 1
while True:
    r = wcapi.get("products", params={"per_page": 100, 'page': page})
    products = r.json()
    page = page + 1
    if not products:  # no more products
        break

    # append all products into lists. Total products and products with no images to be deleted
    for product in products:
        product_id = product['id']
        image = product['images']

        total_products.append(product_id)

        if not image:
            products_to_delete.append(product_id)


def define_and_parse_command_line_args():
    # defining argument parser
    parser = argparse.ArgumentParser(description="Delete products that contain no images from the database")
    parser.add_argument("--confirm-delete", choices=["yes", "no"], default="no",  type=str.lower,
                        help=f"Confirm deletion (yes/no). \n"
                             f"There are {len(products_to_delete)} products to be deleted. "
                             f"By selecting '--confirm-delete no' you will not deleted any products. "
                             f"By selecting '--confirm-delete yes' you will delete {len(products_to_delete)} products.")

    # parse command-line arguments
    args = parser.parse_args()
    global confirm_delete
    confirm_delete = args.confirm_delete.lower()

    logging.basicConfig(level=logging.INFO)

# check user input and delete products
def delete_confirm():
    if confirm_delete == "yes":
        logging.info(f'Deleting products from database...')
        for i in products_to_delete:
            wcapi.delete(f"products/{i}", params={"force": True})
    else:
        logging.info(f"No products have been deleted. There are {len(products_to_delete)} products containing no image that"
                     f"are eligible for deletion.")

define_and_parse_command_line_args()
delete_confirm()
logging.info(f"{len(products_to_delete)} Products deleted. {len(total_products) - len(products_to_delete)} Products remaining in your store.")
