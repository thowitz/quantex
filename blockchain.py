from block import Block
from transaction import Transaction


class BlockChain:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls(instanceExists=True)
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None

    def __init__(self, instanceExists=False):
        if not instanceExists:
            raise RuntimeError(
                f"{self.__class__.__name__} is a singleton use the getInstance class method."
            )

        self.chain = []
        self.chain.append(Block(0, None, [Transaction(100, "genesis", "tim")]))

    @property
    def lastBlock(self):
        return self.chain[-1]

    def appendBlock(self, newBlock):
        self.chain.append(newBlock)

    def validateChain(self):
        for block in self.chain:
            if block.index != 0:
                if not Block.validateBlocks(block, self.chain[block.index - 1]):
                    return False
                if not Transaction.validateTransactions(block.transactionList):
                    return False

        return True

    def proofOfStake():
        pass