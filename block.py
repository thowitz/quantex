from Crypto.Hash import SHA3_256
import time


class Block:
    def __init__(self, index, previousBlockHash, transactionList):
        self.index = index
        self.previousBlockHash = previousBlockHash
        self.transactionList = transactionList

        self.blockData = {
            "index": self.index,
            "previousBlockHash": self.previousBlockHash,
            "transactionList": self.transactionList,
            "timestamp": time.time(),
        }

    @property
    def blockHash(self):
        hash = SHA3_256.new()
        hash.update(self.blockData.encode())
        hexHash = hash.hexdigest()

        print(self.blockData)
        print(hexHash)

        return hexHash
