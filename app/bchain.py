import datetime
import hashlib
import json
from flask import Flask, jsonify, request, render_template
import requests
from uuid import uuid4
from urllib.parse import urlparse



class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions': self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    def add_status(self, courier_id, current_location, status):
        self.transactions.append({'courier_id': courier_id,
                                  'current_location': current_location,
                                  'status': status})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def sign_up(self, user_id, name, address, email, phone):
        self.transactions.append({'user_id': user_id,
                                  'name': name,
                                  'address': address,
                                  'email': email,
                                  'phone': phone})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def product_id(self, product_id, product_name, amount, quantity):
        self.transactions.append({'product_id': product_id,
                                  'product_name': product_name,
                                  'amount': amount,
                                  'quantity': quantity})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def coureir_id(self, courier_id, sender_id, receiver_id, product_id):
        self.transactions.append({'courier_id': courier_id,
                                  'sender_id': sender_id,
                                  'receiver_id': receiver_id,
                                  'product_id': product_id})
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
