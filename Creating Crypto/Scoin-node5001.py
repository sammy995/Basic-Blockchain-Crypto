# -*- coding: utf-8 -*-
#Module 2 -Create Scoin - A cryptoCurrency

#Import libraries
import datetime
import hashlib
import json
import requests
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse

#Part 1 - Building a blockchain

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.mempool = []
        self.create_block(proof = 1, previous_hash = '0') # transactions should precede this step
        self.nodes = set()
        
        
    def create_block(self, proof, previous_hash):
        block = {'index' : len(self.chain) + 1, 
                 'timestamp' : str(datetime.datetime.now()),
                 'proof' : proof,
                 'previous_hash' : previous_hash,
                 'transactions' : self.mempool
                 #Add new keys here to make specific blockchain
                 }
        self.mempool = []
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1] # return last block of the chain
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        
       #Proof-of-Work Function
        while check_proof is False:
            #define puzzle for miner. More 0's more difficulty
             #harder the hash_operation, harder to mine a block
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:3] == '000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    #Create hash of new block
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode() #dumps conerts object into string
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
            if hash_operation[:3] != '000':
                return False 
            previous_block = block
            block_index +=1
        return True
    
    def add_transaction(self, sender, receiver, amount):
        self.mempool.append({'sender':sender, 
                             'receiver' : receiver, 
                             'amount': amount})
        previous_block = self.get_previous_block() 
        return previous_block['index'] +1  #As transactions will be added to next mined block
    
    
    def add_node(self, address):
        parsed_url = urlparse(address) # parsed_url will have all details of url..params,args,netloc
        self.nodes.add(parsed_url.netloc) #netloc - has exact url . 
        
    
    def replace_chain(self):
        network = self.nodes #network of all nodes in the world
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = requests.get(f'http://{node}/get_chain') #f string method
            if response.status_code == 200:
                length = response.json()['length'] #Get the length of current nodes' chain
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
                    
        if longest_chain:
            self.chain = longest_chain
            return True
        return False
        
                    
        
    
    
    
#Part 2 
#Create web app using Flask
app = Flask(__name__)

#Create a node on port 5000
node_address = str(uuid4()).replace('-','')  #First node address
    
#Create Blockchain instance
blockchain = Blockchain()
    
#Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender = node_address, receiver = 'Shubham', amount = 1)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message' : 'congo, added a block!',
                'index' : block['index'],
                'timestamp' : block['timestamp'],
                'proof' : block['proof'],
                'previous_hash' : block['previous_hash'],
                'transactions' : block['transactions']}
    
    return jsonify(response), 200
    
    
    
    
#Getting full blockchain displayed in PostMan

@app.route('/get_chain' , methods = ['GET'])
def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)}
    return jsonify(response), 200
    


#Validating if blockchain is valid or not
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : "BlockChain is VALID!"}
    else:
        response = {'message' : "BlockChain is INVALID!"}
    return jsonify(response), 200


#Adding transaction in the BlockChain
@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver','amount']
    if not all(key in json for key in transaction_keys):
        return 'Issue in inputs of transaction' , 400
    index = blockchain.add_transaction(json['sender'], json['receiver'], json['amount'])
    response = { 'message' : f'Trasaction is Successful and is added to {index} block'}
    return jsonify(response) , 201

#Connecting new nodes
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes') #Contains address of all the nodes in json file
    if nodes is None:
        return "No node found" , 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message' : 'new node/s have been added in the chain and Scoin now has following nodes:',
                'total_nodes' : list(blockchain.nodes) }
    return jsonify(response) , 201

#Replacing the chain with longest chain (if needed)
@app.route('/replace_chain', methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message' : 'BlockChain is REPALCED with longest chain',
                    'new_chain' : blockchain.chain}
    else:
        response = {'message' : 'BlockChain is not replaced and current chain is the longest!',
                    'actual_chain' : blockchain.chain}
    return jsonify(response), 200

#Running the app
app.run(host = '0.0.0.0', port = 5001)
