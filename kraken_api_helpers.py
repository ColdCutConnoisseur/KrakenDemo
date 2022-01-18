"""This module provides the main functionality for interacting with the Kraken API 
   (i.e. only query_account_balances as of right now)
"""

import time
import os
import urllib.parse
import hashlib
import hmac
import base64

import requests
from requests.auth import AuthBase

import app_constants

class KrakenAuth(AuthBase):
    """Append authorization headers to API requests"""
    def __init__(self, api_key, signature):

        self.api_key = api_key
        self.signature = signature

    def __call__(self, r):
        r.headers['API-Key'] = self.api_key
        r.headers['API-Sign'] = self.signature
        return r


def create_nonce():
    """Return unix timestamp in milliseconds"""
    unix_timestamp_in_mils = int(time.time() * 1000)
    timestamp_as_string = str(unix_timestamp_in_mils)
    return timestamp_as_string

def read_credentials():
    """Get user credentials from environment variables"""
    api_key = None
    api_sec = None

    try:
        api_key = os.environ['API_KEY_KRAKEN']
        api_sec = os.environ['API_SEC_KRAKEN']
    
    except KeyError:
        print("Please make sure you have entered both your API key as well as your secret as" +\
              " environment variables.")

    return [api_key, api_sec]

def get_kraken_signature(urlpath, data, secret):
    """Return Kraken signature for API requests.
        Taken from Kraken API documentation.
    """
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()

def query_account_balances():
    """Return all balances for user account"""
    #Create data payload of 'nonce'
    nonce = create_nonce()
    payload = {"nonce" : nonce}
    
    #Retrieve user credentials
    api_key, api_secret = read_credentials()

    if (not api_key) or (not api_secret):
        return 0

    #Set url paths from app_constants.py
    kraken_base_url = app_constants.KRAKEN_API_URL
    urlpath = app_constants.ACCOUNT_BALANCES_URI_PATH

    #Sign message
    signature = get_kraken_signature(urlpath, payload, api_secret)

    #Make request
    full_url = kraken_base_url + urlpath
    r = requests.post(full_url, auth=KrakenAuth(api_key, signature), data=payload)    

    #Check for successful call
    if r.status_code == 200:
        json_response = r.json()
        response_errors = json_response['error'] #Unique to Kraken in that a 200 status code can still be a bad call
        if len(response_errors) > 0:
            print(f"Error(s) returned in call to 'query_account_balances': {response_errors}")
            return None
        
        else:

            print(json_response)

            try: #Check for 'result' key
                result = json_response['result']
                return result

            except KeyError: #No 'result' key
                return None

    #Status code other than 200
    else:
        print(f"Call to 'query_account_balances' returned status code: {r.status_code}")
        return None

def query_coin_balance(coin):
    """Return the balance for a given coin"""
    response = query_account_balances()
    if not response:
        print("Bad call in call to 'query_account_balances'")
        return 0

    coins_with_balance = response.keys()

    if coin not in coins_with_balance:
        print("Coin balance not found.  Make sure it is a non-zero balance and that case matches" +\
              " that of Kraken.")

    else:
        coin_balance = response[coin]
        print(f"{coin} balance: {coin_balance}")


if __name__ == "__main__":
    query_account_balances()
