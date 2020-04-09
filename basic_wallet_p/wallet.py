import json
import sys
import requests
from datetime import datetime

from flask import Flask, jsonify, request, render_template


class User(object):
    def __init__(self, ID,):
        self.ID = ID
        self.balance = 0
        self.transactions = []


# Instantiate our Node
app = Flask(__name__)

@app.route('/home', methods=['GET'])
def get_home_page():

    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # get entire block chain
    r = requests.get(url=node + "/chain")
    # turn it into a json
    data = r.json()
    # get the chain list object from the data json
    chain = data['chain']

    # go through each block
    for block in chain:
        # look at each transaction
        for transaction in block['transactions']:
            # if we recieved money add it to our wallet
            if transaction['recipient'] == user.ID:
                user.balance += transaction['amount']
                user.transactions.append(transaction)
            # if we spent money subtract it from our wallet
            if transaction['sender'] == user.ID:
                user.balance -= transaction['amount']
                user.transactions.append(transaction)
    
    # construct the json the user will see containing their ID, balance, and all transactions
    response = {
        'ID': user.ID,
        'balance': user.balance,
        'transactions': user.transactions
    }
    
    return jsonify(response), 200


if __name__ == '__main__':
# Run the app on default port
    user_id = input("Enter your User ID: ")
    # Instantiate the user
    user = User(user_id)
    # run the Flask app
    app.run(host='0.0.0.0', port=3000)

