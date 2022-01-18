# KrakenDemo
Demo call to Kraken API.  Returns user's account balances.

## Setup

### Installing Dependencies
Run **pip install -r requirements.txt** in the terminal to install project dependencies.  The only current dependecy is _requests_
 which is used to make the POST call for retrieving account balances.
 
### Setting Environment Variables
The Kraken API uses an api key + private key to authenticate the user and sign messages.  These correspond respectively
to the two environment variables 'API_KEY_KRAKEN' and 'API_SEC_KRAKEN'.
 
Set these two environment variables in your terminal as follows (don't put the brackets around your keys):

    export API_KEY_KRAKEN=[your_kraken_api_key_here]
    export API_SEC_KRAKEN=[your_kraken_api_private_key_here]
    
**NOTE:** These are session specific variables and will have to be set each time a new terminal is used.

## Running
Type **python kraken_api_helpers.py** to run the script. This currently defaults to a call to _query_account_balances()_

If you want to use specific functions of the module (of which there currently exists only two:
    query_account_balances() and
    query_coin_balance(coin)
) in one of your scripts, you can import as follows:

    from kraken_api_helpers import query_account_balances, query_coin_balance


