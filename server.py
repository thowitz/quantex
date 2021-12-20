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

print("\nLoading saved chain file...")
savedChainFile = open("chain.json")
savedChain = json.load(savedChainFile)
savedChainFile.close()
print("Done")

if savedChain:
    blockchain.chain = savedChain
elif not savedChain:
    print("\nCreating genesis block due to empty saved chain...")
    blockchain.createGenesis()
    print("Done")

print("\nResolving chain conflicts...")
blockchain.resolveConflicts()
print("Done\n")

from views import views

app = Flask(__name__)
app.register_blueprint(views, url_prefix="/")

if __name__ == "__main__":
    # deepcode ignore RunWithDebugTrue: Temporary for testing
    app.run(debug=True, port=42069)
