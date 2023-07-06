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
import os
import logging

logging.basicConfig(filename='list_of_cust_emails.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

variable_key = "MYSITE2_API_KEY"
variable_secret = "MYSITE2_API_SECRET"

def check_env_variables():
    try:
        os.environ[variable_key]
        # print(variable_key)
    except Exception as e:
        logging.exception(f"The environment variable name must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception("The environment variable name must be set")

    try:
        os.environ[variable_secret]
    except Exception as e:
        logging.exception(f"The environment variable name must be set: {e}")
        print(f"Error has occurred: {e}")
        raise Exception("The environment variable name must be set")

check_env_variables()

wcapi = API(
    url = "http://localhost:8888/mysite2",
    consumer_key =os.getenv(variable_key),
    consumer_secret =os.getenv(variable_secret),
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
        # breakpoint()
        customer_email = customer["email"]
        email_list.append(customer_email)

#option 1: change to email_list.append([customer_email])
# with open(output_file, 'w', newline= '') as f:
#     writer = csv.writer(f)
#     writer.writerow(["User Email Address:"])
#     writer.writerows(email_list)

#option 2: writing email_list as a list of strings
with open(output_file, 'w', newline= '') as f:
    writer = csv.writer(f)
    writer.writerow(["User Email Address:"])
    for item in email_list:
        writer.writerow(item.split(','))