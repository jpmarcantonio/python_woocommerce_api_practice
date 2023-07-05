"""
Example Admas created on 6/29 office hours to create random email address and add a user.

Example command:
 $ python Create_users_on_website.py --number_of_users=5
"""
import woocommerce
from woocommerce import API
import uuid
import argparse
import logging
import os

# import sys
# arguments = sys.argv
# number_of_users = arguments[1]

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--number_of_users', required=True,
                    help='how many users to create')
args = parser.parse_args()
num_of_users = args.number_of_users

logging.basicConfig(filename='create_users.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')

api_key = os.getenv("MYSITE2_API_KEY")
api_secret = os.getenv("MYSITE2_API_SECRET")

wcapi = API(
    url="http://localhost:8888/mysite2",
    consumer_key=api_key,
    consumer_secret=api_secret,
    version="wc/v3",
    timeout = 60
)

counter = 0
rand_pass = str(uuid.uuid4())
for i in range(int(num_of_users)):
    data = {'email': f'{uuid.uuid4()}@supersqa.com',
            'password': rand_pass}

    rs_api = wcapi.post("customers", data)
    rs_json = rs_api.json()
    email = rs_json['email']

    counter += 1
    user_info = f"{counter} users added to website", f"User's email is: {email}"
    logging.info(user_info)
    print(user_info)