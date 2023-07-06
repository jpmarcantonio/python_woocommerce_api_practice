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


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--number_of_users', required=True,
                    help='how many users to create')
args = parser.parse_args()
num_of_users = args.number_of_users

logging.basicConfig(filename='create_users.log', level=logging.DEBUG,
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


variable_key = "MYSITE2_API_KEY"
variable_secret = "MYSITE2_API_SECRET"

def check_env_variables():
    try:
        os.environ[variable_key]
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
    url="http://localhost:8888/mysite2",
    consumer_key=os.getenv(variable_key),
    consumer_secret=os.getenv(variable_secret),
    version="wc/v3",
    timeout=60
)

for i in range(int(num_of_users)):
    data = {'email': f'{uuid.uuid4()}@supersqa.com',
            'password': str(uuid.uuid4())}

    rs_api = wcapi.post("customers", data)
    rs_json = rs_api.json()
    email = rs_json['email']

    user_info = f"{i + 1} users added to website", f"User's email is: {email}"
    logging.info(user_info)
    print(user_info)