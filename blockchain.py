from block import Block

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

    def newData(self, sender, recipient, quantity):
        self.currentData.append(
            {"sender": sender, "recipient": recipient, "quantity": quantity}
        )
        return True

    def proofOfStake():
        pass