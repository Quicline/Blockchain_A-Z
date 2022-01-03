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
        self.create_block(proof = 1, previous_hash = '0')
        
        
    def create_block(self, proof, previous_hash):
        
        # creating block object
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
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
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode())
            
# Part 2 - Mining our Blockchain