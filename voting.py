
import hashlib
import json
from time import time
from uuid import uuid4

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        self.nodes.add(address)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'votes': self.current_votes,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_votes = []

        self.chain.append(block)
        return block

    def new_vote(self, voter_id, candidate):
        self.current_votes.append({
            'voter': voter_id,
            'candidate': candidate,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Instantiate the Blockchain
blockchain = Blockchain()

# User Interface
def print_menu():
    print("1. Register Node")
    print("2. Add Vote")
    print("3. Mine Block")
    print("4. Print Blockchain")
    print("5. Exit")

# Example usage
blockchain.register_node('http://192.168.0.5:5000')
voter_id = str(uuid4())

while True:
    print_menu()
    choice = input("Enter your choice: ")

    if choice == '1':
        node_address = input("Enter node address: ")
        blockchain.register_node(node_address)
        print("Node registered successfully.")

    elif choice == '2':
        candidate = input("Enter candidate name: ")
        blockchain.new_vote(voter_id, candidate)
        print("Vote added successfully.")

    elif choice == '3':
        proof = blockchain.proof_of_work(blockchain.last_block['proof'])
        previous_hash = blockchain.hash(blockchain.last_block)
        blockchain.new_block(proof, previous_hash)
        print("Block mined successfully.")

    elif choice == '4':
        for block in blockchain.chain:
            print(block)

    elif choice == '5':
        break

    else:
        print("Invalid choice. Please try again.")