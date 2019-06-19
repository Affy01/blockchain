import json


class Block():
    def __init__(self, index, timestamp, nonce, transactions, current_hash, previous_hash):
        """
        init method
        :param index: Index of the block
        :param timestamp: Timestamp of the block
        :param nonce: Nonce to be stored in the block
        :param transactions: Transactions accepted in the new block
        :param current_hash: Hash of this block
        :param previous_hash: Hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.nonce = nonce
        if transactions:
            self.transactions = transactions.copy()
        else:
            self.transactions = None
        self.current_hash = current_hash
        self.previous_hash = previous_hash

    def __str__(self):
        return f"Block(index={self.index}, timestamp={self.timestamp}, nonce={self.nonce}, \
        transactions={self.transactions}, current_hash={self.current_hash}, \
        previous_hash={self.previous_hash})"

    def __repr__(self):
        return {'index': self.index,
                'timestamp': self.timestamp,
                'nonce': self.nonce,
                'transactions': self.transactions,
                'current_hash': self.current_hash,
                'previous_hash': self.previous_hash}

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def get_hash(self):
        return self.current_hash
