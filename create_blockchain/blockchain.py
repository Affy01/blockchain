import hashlib
import json
import random
import requests
import logging
from uuid import uuid4
from datetime import datetime, timezone
from urllib.parse import urlparse
from block import Block

node_address = str(uuid4()).replace('-', '')
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Blockchain(object):
    """docstring for Blockchain"""

    def __init__(self):
        self.chain = []
        self.transaction = []
        self.nodes = set()
        self.create_block()

    def create_block(self, data=None):
        """
        Creates a block and adds to the chain
        :param data: transactions
        """
        block_transactions = []
        previous_block = self.get_previous_block()
        if previous_block is None:
            previous_hash = '0'
            block_transactions = None
        else:
            previous_hash = previous_block["current_hash"]
            block_transactions = self.transaction.copy()

        timestamp, nonce, current_hash = self.proof_of_work(block_transactions)

        block = Block(len(self.chain), str(timestamp), nonce,
                      block_transactions, current_hash, previous_hash)

        self.chain.append(block.__dict__)
        self.add_transaction(node_address, node_address, 1.0, 1.0)
        if block_transactions:
            self.remove_transactions(block_transactions)
            del block_transactions[:]
        return self.chain

    def get_previous_block(self):
        """
        Gets the last block from the chain
        """
        if len(self.chain) == 0:
            return None
        return self.chain[-1]

    def proof_of_work(self, data=None):
        """
        Finds the proof required to mine the block
        :param data: Data that needs to be go into the calculation of hash
        :returns: dictionary with {timestamp, nonce and data}, hash
        """
        found = False
        while found is not True:
            nonce = random.randint(1, 999999)
            timestamp = datetime.now()
            timestamp = timestamp.replace(tzinfo=timezone.utc).timestamp()
            input = {'timestamp': str(timestamp),
                     'nonce': nonce,
                     'data': data}
            encoded_input = json.dumps(input, sort_keys=True).encode()
            new_hash = hashlib.sha256(encoded_input).hexdigest()
            if new_hash[:4] == '0000':
                found = True

        return timestamp, nonce, new_hash

    def get_hash(self, block):
        """
        Calculates the hash value for a block
        :param block: Block to caluclate the has for
        :returns: hash value
        """
        input = {'timestamp': block['timestamp'],
                 'nonce': block['nonce'],
                 'data': block['data']}
        encoded_input = json.dumps(input, sort_keys=True).encode()
        return hashlib.sha256(encoded_input).hexdigest()

    def verify_chain(self):
        """
        Verifies if the blockchain is good
        """
        status = True
        for index, block in enumerate(self.chain):
            if block["index"] == 0:
                if block["current_hash"][:4] != "0000":
                    status = False
                    break
                continue
            else:
                if block["current_hash"][:4] != "0000":
                    status = False
                    break
                elif block["previous_hash"] != self.chain[index - 1]["current_hash"]:
                    logger.error(f"block's {block} previous hash doesn't match with previous block")
                    status = False
        return status

    def get_chain(self):
        """
        Gets the chain
        """
        logger.debug(f"get_chain: {self.chain}")
        if self.verify_chain():
            return self.chain
        else:
            return None

    def add_transaction(self, sender, receiver, amount_tx, amount_rx):
        """
        Adds transaction to the pool
        :param sender: Sender's address
        :param receiver: Receiver's address
        :param amount_tx: Amount to be transferred
        :param amount_rx: Amount added in the transaction
        """
        fee = float(amount_rx) - float(amount_tx)
        transaction_id = str(uuid4())
        self.transaction.append({'id': transaction_id,
                                 'sender': sender,
                                 'receiver': receiver,
                                 'amount': amount_tx,
                                 'fee': fee})
        return transaction_id

    def remove_transactions(self, transactions):
        """
        Removes a transaction from the pool
        :param transactions:
        """
        for transaction in transactions:
            self.transaction.remove(transaction)

    def add_node(self, address):
        """
        Adds a new node to the network
        :param address: address of the node to be added. Eg https://127.0.0.1:5000/
        """
        url = urlparse(address)
        self.nodes.add(url.netloc)

    def update_chain(self, chain):
        """
        Updates existing chain
        :param chain: New chain
        """
        self.chain = chain

    def sync_chain(self):
        """
        Syncs the chain across nodes
        """
        highest_length = len(self.chain)
        longest_chain = self.chain
        synced = True
        for node in self.nodes:
            logger.debug(f"Sending GET request to {node}")
            response = requests.get(f"http://{node}/get-chain")
            if response.status_code == 200:
                length = response.json()["length"]
                chain = response.json()["chain"]
                logger.debug(f"Length for node {node} {length}")
                if length > highest_length:
                    highest_length = length
                    longest_chain = chain
                    synced = False
            else:
                logger.error(f"Error getting chain from node {node}")
        if not synced:
            self.chain = longest_chain
        return synced


