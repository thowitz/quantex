import hashlib
import time

class Block:
    def __init__(self, index, proofNumber, previousHash, data, timestamp=None):
        self.index = index
        self.proofNumber = proofNumber
        self.previousHash = previousHash
        self.data = data
        self.timestamp = timestamp or time.time()

    @property
    def calculateHash(self):
        blockOfString = "{}{}{}{}{}".format(
            self.index, self.proofNumber, self.previousHash, self.data, self.timestamp
        )

        return hashlib.sha3_256(blockOfString.encode()).hexdigest()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(
            self.index, self.proofNumber, self.previousHash, self.data, self.timestamp
        )