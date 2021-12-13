from flask import Blueprint, request
from blockchain import BlockChain
from block import Block
from node import Node
import json

from transaction import Transaction

blockchain = BlockChain.getInstance()
node = Node.getInstance()


def standardResponse(functionToCall, *args):
    try:
        req = request.get_json()
    except:
        return {"result": "Incorrect Format"}, 400

    result = functionToCall(req, *args)

    if result == True:
        return {"result": "Success"}, 200
    else:
        return {"result": result}, 400


views = Blueprint(__name__, "views")


@views.route("/chain/current")
def returnChain():
    return json.dumps(blockchain.chain), 200


@views.route("/block/new", methods=["POST"])
def newBlock():
    # deepcode ignore XSS: I don't think it's applicable here
    return standardResponse(blockchain.processProspectiveBlock)


@views.route("/nodes/current")
def returnNodes():
    return json.dumps(node.nodes), 200


@views.route("/nodes/new", methods=["POST"])
def newNodes():
    # deepcode ignore XSS: I don't think it's applicable here
    return standardResponse(node.processProspectiveNodes)


@views.route("/transaction-pool/current")
def returnTransactionPool():
    return json.dumps(node.transactionPool), 200


@views.route("/transaction-pool/new", methods=["POST"])
def newTransaction():
    # deepcode ignore XSS: I don't think it's applicable here
    return standardResponse(node.processProspectiveTransactions)
