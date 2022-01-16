from flask import Flask
from blockchain import BlockChain
from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
from usefulFunctions import openFile
import sys
import requests

privateKeyPassword = input("Please enter your private key password: ")

blockchain = BlockChain.getInstance()
wallet = Wallet.getInstance()

savedPrivateKeyData = openFile("private-key.json", True)
# we only want to create and save a private key if the file does not exist, otherwise we could be overwriting an existing one
if savedPrivateKeyData == "No saved file found":
    print("Creating private key...")
    wallet.createPrivateKey()
    print("Done")
    print("Saving private key...")
    wallet.savePrivateKey(privateKeyPassword)
    print("Done")
elif type(savedPrivateKeyData) != str:
    savedEncryptedPrivateKey = savedPrivateKeyData["encryptedPrivateKey"]
    decryptionResult = wallet.decryptPrivateKey(
        savedEncryptedPrivateKey, privateKeyPassword
    )
    if decryptionResult == str:
        print(decryptionResult)
        sys.exit()
else:
    print(savedPrivateKeyData)
    sys.exit()

wallet.calculatePublicKey()
node = Node.getInstance()
print("\nSyncing nodes and transaction pool...")
syncResult = node.syncNodesAndTransactionPool()
if syncResult == "Offline":
    print("The network is unreachable, this probably means you're offline")
else:
    print("Done")

savedChainData = openFile("chain.json", True)
if type(savedChainData) != str:
    savedChain = savedChainData
else:
    print(savedChainData)
    savedChain = None

if savedChain:
    blockchain.chain = savedChain
elif not savedChain:
    print("Creating genesis block due to lack of or empty saved chain...")
    blockchain.createGenesis()
    print("Done")

print("\nValidating chain...")
blockchain.validateChain()
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
