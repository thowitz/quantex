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

        configFile = open("config.json")
        self.config = json.load(configFile)
        configFile.close()

        self.chain = []

    def createGenesis(self):
        self.appendBlock(self.config.genesisBlock.blockData)

    @property
    def lastBlock(self):
        lastBLock = Block().fromDict(self.chain[-1])
        return lastBLock

    def appendBlock(self, newBlock: dict):
        # todo call to dict block method
        
        self.chain.append(newBlock)

    def processProspectiveBlock(self, prospectiveNewBlock: object):
        validateBlockResult = Block.validateBlocks(prospectiveNewBlock, self.lastBlock())

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

                if (
                    len(prospectiveNewChain) > len(self.chain)
                    and self.validateChain(prospectiveNewChain) == True
                ):
                    self.chain = prospectiveNewChain

                    savedChainFile = open("chain.json", "w")
                    json.dump(self.chain, savedChainFile, indent=4)
                    savedChainFile.close()

                    return True

        return False

    def validateChain(self):
        for blockDict in self.chain:
            block = Block().fromDict(blockDict)
            if block != True:
                return block

            previousBlock = Block().fromDict(self.chain[block.index - 1])
            if previousBlock != True:
                return previousBlock

            if block.index != 0:
                validateBlockResult = Block.validateBlocks(block, previousBlock)
                if validateBlockResult != True:
                    return validateBlockResult

                validateTransactionsResult = Transaction.validateTransactions(
                    block.transactionList
                )
                if validateTransactionsResult != True:
                    return validateTransactionsResult

            else:
                if block.blockHash != self.config.genesisBlock.hash:
                    return False

        return True

    @staticmethod
    def mine(previousProofNumber: int):
        proofNumber = 0

        while True:
            print(f"⛏️ mining proof {proofNumber}...")
            if Block.verifyProof(proofNumber, previousProofNumber):
                return proofNumber
            else:
                proofNumber += 1
