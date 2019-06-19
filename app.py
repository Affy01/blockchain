import os
import logging
from flask import Flask, jsonify, request
from create_blockchain.blockchain import Blockchain

app = Flask(__name__)
PORT = os.environ.get('PORT', 5000)

logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.DEBUG)
logger = logging.getLogger(__name__)

bc = Blockchain()


@app.route("/mine", methods=['POST'])
def mine():
    logger.debug("Mining a new block")
    try:
        blockchain = bc.create_block()
        response = {"message": "Congratulations! You successfully mined a block.",
                    "blockchain": blockchain}
        return jsonify(response), 201
    except Exception as e:
        response = "Error mining the block. Error {}".format(e)
        logger.error(response)
        return jsonify(response), 500


@app.route("/verify", methods=['GET'])
def verify():
    logger.debug("Verifying a new block")
    try:
        status = bc.verify_chain()
        return jsonify(status), 200
    except Exception as e:
        response = "Error finding the status of the chain. Error {}".format(e)
        logger.error(response)
        return jsonify(response), 500


@app.route("/get-chain", methods=['GET'])
def get_chain():
    logger.debug("GET chain called")
    try:
        chain = bc.get_chain()
        response = {"chain": chain, "length": len(chain)}
        return jsonify(response), 200
    except Exception as e:
        response = "Error getting the chain. Error {}".format(e)
        logger.error(response)
        return jsonify(response), 500


@app.route("/add-transaction", methods=['POST'])
def add_transaction():
    logger.debug("Add transaction called")
    try:
        data = request.json
        transaction_id = bc.add_transaction(data["sender"], data["receiver"], data["amount_tx"], data["amount_rx"])
        response = {"transaction_id": transaction_id}
        return jsonify(response), 201
    except Exception as e:
        response = "Error adding transaction. Error {}".format(e)
        logger.error(response)
        return jsonify(response), 500


@app.route("/add-node", methods=['POST'])
def add_node():
    logger.debug("Add node called")
    try:
        data = request.json
        if data:
            nodes = data["nodes"]
        for node in nodes:
            bc.add_node(node)
        response = {"message": "Nodes added successfully", "nodes": list(bc.nodes)}
        return jsonify(response), 201
    except Exception as e:
        response = "Error adding nodes. Error {}".format(e)
        logger.error(response)
        return jsonify(response), 500


@app.route("/sync-chain", methods=['PATCH'])
def sync_chain():
    logger.debug("sync chain node called")
    try:
        synced = bc.sync_chain()
        if not synced:
            response = {"message": "Chain syned successfully",
                        "chain": bc.chain}
            return jsonify(response), 200
        else:
            response = {"message": "Chain did not require syncing"}
            return jsonify(response), 200
    except Exception as e:
        response = "Error syncing chains. Error {}".format(e)
        logger.error(response)
        return jsonify(response), 500


if __name__ == "__main__":
    app.debug = True
    app.run(host='127.0.0.1', port=PORT)
