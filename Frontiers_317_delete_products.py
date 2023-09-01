"""
Working on a script to clean up demo store. delete all products without images.
"""

from woocommerce import API

wcapi = API(
    url="http://localhost:8888/mysite2",
    consumer_key="<add consumer key>",
    consumer_secret="<add consumer secret>",
    version="wc/v3",
    timeout=60
)

page = 1
total_products = []
products_to_delete = []

# find products with no image to delete
while True:
    r = wcapi.get("products", params={"per_page": 100, 'page': page})
    products = r.json()
    page = page + 1
    if not products:  # no more products
        break

    # store products into lists
    for product in products:
        total_products.append(product['id'])
        if not product['images']:
            products_to_delete.append(product['id'])

# take user input
def delete_confirm():
    print(f"There are {len(total_products)} products currently in your store. ")
    delete = input(f"Are you sure you want to permanently delete {len(products_to_delete)} products? (Yes / N):")
    if delete == 'Yes':
        print(f'Deleting products from database...')
        for i in products_to_delete:
            wcapi.delete(f"products/{i}", params={"force": True})
    else:
        print(f"No products have been deleted.")


delete_confirm()
print(f"{len(products_to_delete)} Products deleted. {len(total_products) - len(products_to_delete)} Products remaining in your store.")

