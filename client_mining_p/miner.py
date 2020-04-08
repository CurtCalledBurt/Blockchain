import hashlib
import requests

import sys
import json


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    # get the block as a string
    block_string = json.dumps(block, sort_keys=True)
    # initialize proof guess
    proof = 0
    # search for a valid proof
    while not valid_proof(block_string, proof):
        # increment our proof guess
        proof += 1
    return proof


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    # construct our guess from the block's string and our current proof guess
    guess = f"{block_string}{proof}".encode()
    # get the hash of our guess in hexadecimal
    guess_hash = hashlib.sha256(guess).hexdigest()
    # set the difficulty of what hashes we are looking for
    difficulty = "000"
    # return if our guess's hash has the correct number of zeroes at the beginning
    return guess_hash[:len(difficulty)] == difficulty


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins_mined = 0
    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        # get a new proof for the current last block
        new_proof = proof_of_work(data)

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}
        r = requests.post(url=node + "/mine", json=post_data)
        
        # get the server's response from our post
        try:
            data = r.json()
        except ValidationError:
            print(r)

        # after sending a successful proof to the server, get a response back 
        # and increment our personal count of new blocks we've forged
        if data['message'] == 'New Block Forged':
            coins_mined += 1
            print('Coins Mined: ', coins_mined)
            print('Proof of new coin: ', new_proof)
        # the block wasn't forged, print the server's message to us
        else:
            print(data['message'])
