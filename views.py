from flask import Blueprint
from blockchain import BlockChain
from block import Block
from node import Node
import json

from transaction import Transaction

blockchain = BlockChain.getInstance()
node = Node.getInstance()

views = Blueprint(__name__, "views")


@views.route("/chain")
def returnChain():
    return json.dumps(blockchain.chain)


@views.route("/nodes")
def returnNodes():
    return json.dumps(node.nodes)


@views.route("/newBlock", methods=["POST"])
def newBlock():
    return blockchain.processProspectiveBlock()