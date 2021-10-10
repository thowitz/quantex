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


class BlockChain:
    def __init__(self):
        self.chain = []
        self.currentData = []
        self.nodes = set()
        self.constructGenesis()

    def constructGenesis(self):
        self.constructBlock(proofNumber=0, previousHash=0)

    def constructBlock(self, proofNumber, previousHash):
        block = Block(
            index=len(self.chain),
            proofNumber=proofNumber,
            previousHash=previousHash,
            data=self.currentData,
        )
        self.currendData = []

        self.chain.append(block)
        return block

    @staticmethod
    def checkValidity(block, previousBlock):
        if previousBlock.index + 1 != block.index:
            return False

        elif previousBlock.calculateHash != block.previousHash:
            return False

        elif not BlockChain.verifyingProof(
            block.proofNumber, previousBlock.proofNumber
        ):
            return False

        elif block.timestamp <= previousBlock.timestamp:
            return False

        return True