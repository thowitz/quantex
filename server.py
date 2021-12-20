from flask import Flask
from views import views
from blockchain import BlockChain
from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
import json
import requests

privateKeyPassword = "thanks for all the fish"

blockchain = BlockChain.getInstance()
wallet = Wallet.getInstance()

if wallet.checkExistingPrivateKey():
    wallet.readPrivateKey(privateKeyPassword)
else:
    wallet.createPrivateKey()
    wallet.savePrivateKey(privateKeyPassword)

wallet.calculatePublicKey()
node = Node.getInstance()

savedChainFile = open("chain.json")
savedChain = json.load(savedChainFile)

savedChainFile.close()

if savedChain:
    blockchain.chain = savedChain
elif not savedChain:
    blockchain.createGenesis()

blockchain.resolveConflicts()

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    # deepcode ignore RunWithDebugTrue: Temporary for testing
    app.run(debug=True, port=42069)
