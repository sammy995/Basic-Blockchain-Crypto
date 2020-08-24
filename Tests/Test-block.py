import time

def mine_block(last_block, data):
    """
    Mines a block based on given inputs
    """
    timestamp = time.time_ns()
    last_hash = last_block.hash
    hash = f'{timestamp} ***{last_hash}'

    return Block(timestamp, last_hash, hash, data)

def genesis():
    """
    Create Genesis block for blockchain
    """
    return Block(1, 'genesis_last_hash', 'genesis_hash' ,[])


class Block:
    """
    Block is unit of storage. Stores transactions
    """
    def __init__(self, timestamp, last_hash, hash, data):
        self.timestamp = timestamp
        self.last_hash = last_hash
        self.hash = hash
        self.data = data

    def __repr__(self):
        return( 
            'Block('
            f'timestamp : {self.timestamp},'
            f'last_hash : {self.last_hash},'
            f'hash : {self.hash},'
            f'data : {self.data}'
        )

def main():
    block = Block('foo')
    print(block)
    print(f'blockchain.py __name__ : {__name__}') #Takes name of module it is executing - Used for debugging

    genesis_block = genesis()
    block = mine_block(genesis_block)
    print(block)


if __name__ == '__main__': 
    main() # used to execute only if main is called   
"""
python3 blockchain.py
Output:
Block Data foo
blockchain.py __name__ : block <- module
Blockchain [Block Data 1, Block Data 2]
blockchain.py __name__ : __main__ <-module
"""