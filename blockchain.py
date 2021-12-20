from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
import requests
import json


class BlockChain:
    # singleton to prevent mismatches in chain state between instances
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
        genesisBlockObject = Block()
        genesisBlockObject.fromDict(self.config["genesisBlock"]["blockData"])
        self.appendBlock(genesisBlockObject)

    @property
    def lastBlock(self):
        lastBlock = Block().fromDict(self.chain[-1])
        return lastBlock

    def appendBlock(self, newBlock: object):
        blockDict = Block().toDict(newBlock)
        if blockDict != True:
            return blockDict

        self.chain.append(blockDict)

    def processProspectiveBlock(self, prospectiveNewBlock: object):
        validateBlockResult = Block.validateBlocks(
            prospectiveNewBlock, self.lastBlock()
        )

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

    # replaces the current chain with the longest one to provide consensus of chain state
    def resolveConflicts(self):
        node = Node.getInstance()
        possibleOfflineValidators = []

        for validator in node.nodes:
            try:
                response = requests.get(f"http://{validator}/chain", timeout=1)
            except:
                possibleOfflineValidators.append(validator)
                continue

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

        # if every validator is offline, chances are we're in fact the ones offline
        if possibleOfflineValidators and possibleOfflineValidators != node.nodes:
            node.processPossibleOfflineValidators(possibleOfflineValidators)

        return False

    # validate all data points for every block in a chain
    def validateChain(self):
        for blockDict in self.chain:
            block = Block()
            blockFromDictResult = block.fromDict(blockDict)
            if blockFromDictResult != True:
                return blockFromDictResult

            previousBlock = Block()
            previousBlockFromDictResult = previousBlock.fromDict(
                self.chain[block.index - 1]
            )
            if previousBlockFromDictResult != True:
                return previousBlockFromDictResult

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
                if block.blockHash != self.config["genesisBlock"]["blockData"]:
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
