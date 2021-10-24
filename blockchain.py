from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
import requests
import json


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

    def __init__(self, instanceExists: bool = False):
        if not instanceExists:
            raise RuntimeError(
                f"{self.__class__.__name__} is a singleton, use the getInstance class method."
            )

        self.chain = []

    def createGenesis(self):
        # todo proper placeholder private key

        wallet = Wallet.getInstance()

        newTransaction = Transaction(100, "genesis", "tim")
        newTransaction.signTransaction(wallet.privateKey)

        self.appendBlock(
            Block(0, None, [newTransaction.signedTransaction], 0).blockData
        )

    @property
    def lastBlock(self):
        return self.chain[-1]

    def appendBlock(self, newBlock: dict):
        self.chain.append(newBlock)

    def processProspectiveBlock(self, prospectiveNewBlock: dict):
        # todo check for correct validator public key

        validateBlockResult = Block.validateBlocks(prospectiveNewBlock, self.chain[-1])

        if validateBlockResult != True:
            return validateBlockResult

        validateTransactionsResult = Transaction.validateTransactions(
            prospectiveNewBlock.transactionList
        )
        if validateTransactionsResult != True:
            return validateTransactionsResult

        self.appendBlock(prospectiveNewBlock)

        # todo notify other validators

        return True

    def resolveConflicts(self):
        node = Node.getInstance()

        for node in node.nodes:
            try:
                response = requests.get(f"http://{node}/chain")
            except requests.exceptions.RequestException as error:
                return error

            if response.status_code == 200:
                prospectiveNewChain = response.json()

                if len(prospectiveNewChain) > len(self.chain) and self.validateChain(
                    prospectiveNewChain
                ):
                    self.chain = prospectiveNewChain

                    savedChainFile = open("chain.json", "w")
                    json.dump(self.chain, savedChainFile, indent=4)

                    return True

        return False

    def validateChain(self):
        for block in self.chain:
            if block.index != 0:
                if not Block.validateBlocks(block, self.chain[block.index - 1]):
                    return False
                if not Transaction.validateTransactions(block.transactionList):
                    return False

        return True

    @staticmethod
    def mine(previousProofNumber):
        proofNumber = 0

        while True:
            print(f"⛏️ mining proof {proofNumber}...")
            if Block.verifyProof(proofNumber, previousProofNumber):
                return proofNumber
            else:
                proofNumber += 1
