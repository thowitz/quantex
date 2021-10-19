from flask import Blueprint
from blockchain import BlockChain
import json

blockchain = BlockChain.getInstance()

views = Blueprint(__name__, "views")


@views.route("/chain")
def returnChain():
    return json.dumps(blockchain.chain)


# @views.route("/nodes")
# def returnNodes():
#     return json.dumps(node.nodes)