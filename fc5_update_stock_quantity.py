"""
Working on a script to update the stock quantity of all items in the store. The script will update the quantity
of each item to a random number between 0 - 50

"manage_stock" must be True in order to update stock quantity
"""
from woocommerce import API
import random

wcapi = API(
    url="http://dev.bootcamp.store.supersqa.com/",
    consumer_key="CONSUMER_KEY",
    consumer_secret="CONSUMER_SECRET",
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
# for each product, check product type, add to list for logging, update qty
    for product in products:
        product_id = product["id"]
        stock_quantity = product["stock_quantity"]
        manage_stock = product["manage_stock"]
        product_type = product["type"]
        invalid_product_types = ['external', 'grouped']

    # update valid product ids with a random stock quantity
        if product_type not in invalid_product_types:
            product_ids.append(product_id)

            data = {'manage_stock': True,
                    'stock_quantity': random.randrange(51)}

            r3 = wcapi.put(f'products/{product_id}', data)

            updated_product = r3.json()
            status_code = r3.status_code
            response_body = r3.content
            if status_code != 200:
                raise Exception(f"Expected status code 200. Got status code {status_code}"
                                f"For more information about your error, see: {response_body}")
            print(f"Product Type: {product_type}, Product ID: {product_id}, Stock Quantity: {stock_quantity}")

        else:
            invalid_product_ids.append(product_id)
print(f"Did not update stock quantity on product ids: {invalid_product_ids} due to being invalid for stock management.")
