"""
Example Admas created on 6/29 office hours to create random email address and add a user.

Example command:
 $ python Create_users_on_website.py --number_of_users=5
"""

from woocommerce import API
import uuid
import argparse
# import sys
# arguments = sys.argv
# number_of_users = arguments[1]
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--number_of_users', required=True,
                    help='how many users to create')
args = parser.parse_args()
num_of_users = args.number_of_users

wcapi = API(
    url="http://localhost:8888/mysite2",
    consumer_key="<add consumer key>",
    consumer_secret="<add consumer secret>",
    version="wc/v3",
    timeout = 60
)
rand_pass = str(uuid.uuid4())
for i in range(int(num_of_users)):
    data = {'email': f'{uuid.uuid4()}@supersqa.com',
            'password': rand_pass}

    rs_api = wcapi.post("customers", data)

    rs_json = rs_api.json()
    email = rs_json['email']
    print(email)