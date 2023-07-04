"""
 Write a py script that will get list of all customer emails for our website
Setup:
You need the ecom website.
You need API credentials.

Problem statement:
Write a script that will get a list of all users for the website.
Your script should output a csv file with list of email addresses.
"""

from woocommerce import API
import csv

wcapi = API(
    url = "http://localhost:8888/mysite2",
    consumer_key = "<add consumer key>",
    consumer_secret = "<add consumer secret>",
    version = "wc/v3"
)

page = 1
email_list = []
while True:
    r = wcapi.get("customers", params={"per_page": 100, "page": page})
    customers = r.json()
    output_file = 'list_of_user_email.csv'

    page += 1
    if not customers:
        break

    for customer in customers:
        customer_email = customer["email"]
        email_list.append([customer_email])

with open(output_file, 'w', newline= '') as f:
    writer = csv.writer(f)
    writer.writerow(["User Email Address:"])
    writer.writerows(email_list)