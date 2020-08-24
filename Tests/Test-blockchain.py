from block import Block  
""" Evaluates entire file before going into code below
    To control it 
"""

class Blockchain:
    """"Blockchain is distributed ledger of transactions
        Implemented as list
    """
    def __init__(self):
        self.chain = []

    def __repr__(self):
        return f"Blockchain {self.chain}"

    def add_block(self,data):
        self.chain.append(Block(data))

if __name__ == '__main__':   
    blockchain = Blockchain()
    blockchain.add_block('1')
    blockchain.add_block('2')
    print(blockchain)
    print(f'blockchain.py __name__ : {__name__}') #Takes name of module it is executing - Used for debugging

"""
python3 blockchain.py
Output:
Block Data foo
blockchain.py __name__ : block <- module
Blockchain [Block Data 1, Block Data 2]
blockchain.py __name__ : __main__ <-module
"""