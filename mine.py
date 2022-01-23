import threading
import time

from numpy import block
from block import Block


def startMining(blockchainInstance, nodeInstance):
    global blockchain
    blockchain = blockchainInstance
    global node
    node = nodeInstance
    blockchain.miningThread = threading.Thread(target=mine)
    blockchain.miningThread.start()


def mine():
    proofNumber = blockchain.mine(blockchain.lastBlock.proofNumber)
    lastBlock = blockchain.lastBlock
    transactionList = []
    transactionList.extend(node.transactionPool)
    transactionList.append(
        {
            "amount": 50,
            "senderPublicKey": "blockReward",
            "recipientPublicKey": "03e278af2e41aaf2a255958adc60d4edb41fc9f1dd1c3fc902980202ebb5cd6ea7",
        }
    )

    newBlockDict = {
        "index": lastBlock.index + 1,
        "previousBlockHash": lastBlock.blockHash,
        "transactionList": transactionList,
        "timestamp": round(time.time()),
        "proofNumber": proofNumber,
    }
    newBlock = Block()
    newBlock.fromDict(newBlockDict)

    print("Block ready to be broadcast to network")

    node.makeNetworkRequest("/block/new")
    blockchain.appendBlock(newBlock)
