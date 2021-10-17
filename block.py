from Crypto.Hash import SHA3_256
import time


class Block:
    def __init__(self, previousHash, transactionList):
        self.previousHash = previousHash
        self.transactionList = transactionList
        
        self.blockData = "{}-{}-{}".format(self.previousHash, self.transactionList, time.time())

    @property
    def blockHash(self):
        hash = SHA3_256.new()
        hash.update(self.blockData.encode())
        hexHash = hash.hexdigest()

        print(self.blockData)
        print(hexHash)

        return hexHash
