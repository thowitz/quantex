from block import Block
from transaction import Transaction


class BlockChain:
    def __init__(self):
        self.chain = []
        self.chain.append(Block(None, Transaction(100, "genesis", "tim")))

    @property
    def lastBlock(self):
        return self.chain[self.chain.len() - 1]

    def constructBlock(self, transaction, senderPublicKey, signature):
        newBlock = Block(self.lastBLock.hash, transaction)

        self.chain.append(newBlock)

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

    def newData(self, sender, recipient, quantity):
        self.currentData.append(
            {"sender": sender, "recipient": recipient, "quantity": quantity}
        )
        return True

    def proofOfStake():
        pass