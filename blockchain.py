import string
from block import Block
from transaction import Transaction
from wallet import Wallet
from node import Node
import requests
import json
import os


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
        lastBlock = Block()
        lastBlock.fromDict(self.chain[-1])
        return lastBlock

    def openFile(self, file: string, returnJson: bool = False, mode: string = "r"):
        # creates human readable name by removing extension
        dotIndex = file.find(".")
        if dotIndex == -1:
            return "Please provide the filename with its extension"
        fileHrName = file[0, dotIndex]

        if os.path.isfile(file):
            print(f"\nFound saved {fileHrName} file")
            print(f"Opening {fileHrName}...")
            try:
                savedFile = open(file, mode)
                if returnJson:
                    if file[-4, -1] == "json":
                        returnData = json.load(savedFile)
                    else:
                        savedFile.close()
                        return "File extension must be .json if returnJson is true"
                    savedFile.close()
                elif not returnJson:
                    returnData = savedFile
                print("Done")
                return returnData
            except:
                return f"Unable to load {fileHrName} file"
        else:
            return f"No saved {fileHrName} file found"

    def appendBlock(self, newBlock: object):
        blockDict = Block().toDict(newBlock)
        if type(blockDict) != dict:
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

    # replaces the current chain with the longest valid one to provide consensus of chain state
    def resolveConflicts(self):
        node = Node.getInstance()

        chainResponses = node.makeNetworkRequest("/chain")

        if chainResponses and type(chainResponses) != str:
            for chainResponse in chainResponses:
                prospectiveNewChain = chainResponse.json()

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

    # validate all data points for every block in a chain
    def validateChain(self):
        for blockDict in self.chain:
            block = Block()
            blockFromDictResult = block.fromDict(blockDict)
            if blockFromDictResult != True:
                return blockFromDictResult

            if block.index != 0:
                previousBlock = Block()
                previousBlockFromDictResult = previousBlock.fromDict(
                    self.chain[block.index - 1]
                )
                if previousBlockFromDictResult != True:
                    return previousBlockFromDictResult

                validateBlockResult = Block.validateBlocks(block, previousBlock)
                if validateBlockResult != True:
                    return validateBlockResult

                validateTransactionsResult = Transaction.validateTransactions(
                    block.transactionList
                )
                if validateTransactionsResult != True:
                    return validateTransactionsResult

            else:
                if block.blockHash != self.config["genesisBlock"]["hash"]:
                    return False

        return True

    @staticmethod
    def mine(previousProofNumber: int):
        proofNumber = 0

        while True:
            print(
                f"\r⛏️ Mining proof {proofNumber}...",
                end="",
            )
            if Block.verifyProof(proofNumber, previousProofNumber):
                print(f"\r⛏️ Proof found {proofNumber}\n")
                return proofNumber
            else:
                proofNumber += 1
