#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# Module 1: Create a Blockchain
"""
Created on Mon Dec  6 01:40:02 2021

@author: armandofrancisco
"""
# importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchain

class Blockchain:
    
    def __init__(self):
        
        # creating the blockchain
        self.chain = []
        # creating genesis block
        self.create_block(proof = 1, hash1 = '0', previous_hash = '0')
        
        
    def create_block(self, proof, hash1, previous_hash):
        
        # creating block object
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'hash': hash1,
                 'previous_hash': previous_hash}
        
        # pushing the new block to the list
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        # returning last block on the chain
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        
        new_proof = 1
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            # check if hash_operation has the first 4 zeroes
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                
        return new_proof, hash_operation
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
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
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
        
# Part 2 - Mining our Blockchain

# Creating a Web app

app = Flask(__name__)


# Creating the blockchain

blockchain = Blockchain()

# Mining a new Block

@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof,hash1 = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, hash1, previous_hash)
    
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'hash': block['hash'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
        }
    return jsonify(response), 200
    

# Getting the full Blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
        }
    return jsonify(response), 200
    

# Check if blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:    
        response = {'message': 'The blockchain is valid!'}
    else:
        response = {'message': 'Oh no, the blockchain is invalid!'}
    return jsonify(response), 200

# Running the app

app.run(host= '0.0.0.0', port = 5001)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
