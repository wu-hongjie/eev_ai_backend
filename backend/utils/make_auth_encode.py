'''
Make HTTP base authentication encoded.

1. Retrieve client id and client secret using below site.

   http://127.0.0.1:8000/oauth/applications/register/

2. Run this python script with client id and client secret

   python make_auth_encode.py [client id] [client secret]

3. authentication encoded
'''

import argparse
import base64

if __name__ == "__main__":

    # parse args
    parser = argparse.ArgumentParser(description='Make HTTP base authentication encoded')
    parser.add_argument('client_id', help='client id from /oauth/applications/register/')
    parser.add_argument('client_secret',  help='client secret from /oauth/applications/register/')
    args = parser.parse_args()

    # make HTTP base authentication encoded
    credential = "{0}:{1}".format(args.client_id, args.client_secret)   
    auth_encode = base64.b64encode(credential.encode("utf-8"))

    # print HTTP base authentication encoded
    print(auth_encode)