from flask import Flask
from views import views
from blockchain import BlockChain
from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
import json
import requests

blockchain = BlockChain.getInstance()
wallet = Wallet.getInstance()
node = Node.getInstance()

savedChainFile = open("chain.json")
savedChain = json.load(savedChainFile)

if savedChain:
    blockchain.chain = savedChain

blockchain.createGenesis()

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    app.run(debug=True, port=42069)
