from Crypto.Hash import SHA3_256
from Crypto.Signature import pss
from block import Block
from transaction import Transaction


class BlockChain:
    def __init__(self):
        self.chain = []
        self.chain.append(Block(None, [Transaction(100, "genesis", "tim")]))

    @property
    def lastBlock(self):
        return self.chain[-1]

    def appendBlock(self, newBlock):
        self.chain.append(newBlock)

    @staticmethod
    def validateTransactions(transactionList):
        for transaction in transactionList:
            hash = SHA3_256.new(transaction)
            verifier = pss.new(transaction.senderPublicKey)

            try:
                verifier.verify(hash, transaction.signature)
            except (ValueError, TypeError):
                return False

        return True

    @staticmethod
    def validateBlocks(block, previousBlock):
        if block.previousBlockHash != previousBlock.blockHash:
            return False
        
        elif block.index <= previousBlock.index:
            return False

        elif block.timestamp <= previousBlock.timestamp:
            return False

        return True

    def validateChain(self):
        for block in self.chain:
            if block.index != 0:
                if not self.validateBlocks(block, self.chain[block.index - 1]):
                    return False
                if not self.validateTransactions(block.transactionList):
                    return False
                
        return True

    def proofOfStake():
        pass