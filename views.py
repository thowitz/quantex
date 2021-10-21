from flask import Blueprint, Request
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


@views.route("/block/new", methods=["POST"])
def newBlock():
    return standardResponse(blockchain.processProspectiveBlock(Request.get_json()))


@views.route("/nodes/current")
def returnNodes():
    return json.dumps(node.nodes), 200


@views.route("/nodes/new", methods=["POST"])
def newNodes():
    return standardResponse(node.processProspectiveNodes(Request.get_json()))
