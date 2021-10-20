from flask import Blueprint
from blockchain import BlockChain
from block import Block
from node import Node
import json

from transaction import Transaction

blockchain = BlockChain.getInstance()
node = Node.getInstance()


def standardResponse(conditional):
    if conditional:
        return True, 200
    else:
        return False, 400


views = Blueprint(__name__, "views")


@views.route("/chain/current")
def returnChain():
    return json.dumps(blockchain.chain), 200


@views.route("/chain/new", methods=["POST"])
def newChain():
    return standardResponse(blockchain.processProspectiveChain())


@views.route("/nodes/current")
def returnNodes():
    return json.dumps(node.nodes), 200


@views.route("/newBlock", methods=["POST"])
def newBlock():
    return standardResponse(blockchain.processProspectiveBlock())