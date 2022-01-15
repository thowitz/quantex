from flask import Flask
from blockchain import BlockChain
from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
import json
import requests

privateKeyPassword = input("Please enter your private key password: ")

blockchain = BlockChain.getInstance()
wallet = Wallet.getInstance()

if wallet.checkExistingPrivateKey():
    print("\nFound saved private key")
    print("Reading private key...")
    wallet.readPrivateKey(privateKeyPassword)
    print("Done")
else:
    print("\nNo saved private key found")
    print("Creating private key...")
    wallet.createPrivateKey()
    print("Done")
    print("Saving private key...")
    wallet.savePrivateKey(privateKeyPassword)
    print("Done")

wallet.calculatePublicKey()
node = Node.getInstance()
print("\nSyncing nodes and transaction pool...")
syncResult = node.syncNodesAndTransactionPool()
if syncResult == "Offline":
    print("The network is unreachable, this probably means you're offline")
else:
    print("Done")

print("\nLoading saved chain file...")
try:
    savedChainFile = open("chain.json")
    savedChain = json.load(savedChainFile)
    savedChainFile.close()
    print("Done")
except:
    print("Unable to load saved chain file")
    savedChain = None

if savedChain:
    blockchain.chain = savedChain
elif not savedChain:
    print("\nCreating genesis block due to lack of or empty saved chain...")
    blockchain.createGenesis()
    print("Done")

print("\nResolving chain conflicts...")
blockchain.resolveConflicts()
print("Done\n")

blockchain.mine(blockchain.lastBlock.proofNumber)

from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    # deepcode ignore RunWithDebugTrue: Temporary for testing
    app.run(debug=False, port=42069)
