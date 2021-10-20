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

    @staticmethod
    def validateBlocks(block, previousBlock):
        if type(block.index) != int:
            return False
        elif type(block.previousBlockHash) != str:
            return False
        elif type(block.transactionList) != list:
            return False
        elif type(block.timestamp) != float:
            return False

        if block.previousBlockHash != previousBlock.blockHash:
            return False

        elif block.index <= previousBlock.index:
            return False

        elif block.timestamp <= previousBlock.timestamp:
            return False

        return True
