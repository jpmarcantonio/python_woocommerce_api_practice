"""
Example command:
 $ python create_products_on_website.py --number_of_products=5
"""

from woocommerce import API
import random
import string
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--number_of_products', required=True,
                    help='how many products to create')
args = parser.parse_args()
num_of_products = args.number_of_products

# one way to do command line argument. add number of users right after file.py in cmd then enter.
#also change to: for i in range(number_of_products):
# import sys
# arguments = sys.argv
# number_of_products = int(arguments[1])

wcapi = API(
    url="http://localhost:8888/mysite2",
    consumer_key="<add consumer key>",
    consumer_secret="<add consumer secret>",
    version="wc/v3",
    timeout = 60
)


for i in range(int(num_of_products)):
    length = 15
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(length))

    random_float = round(random.uniform(1, 100), 2)

    data = {
        "name": random_string,
        "regular_price": str(random_float),
        "price": random_float
    }

    rs_api = wcapi.post("products", data)
    rs_json = rs_api.json()
    name = rs_json['name']
    price = rs_json['price']
    print(f"{i + 1} of {num_of_products} products created: ", name, price)

