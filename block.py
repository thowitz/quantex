from Crypto.Hash import SHA3_256
from Crypto.Hash import MD5
import time


class Block:
    def __init__(self):
        self.index = None
        self.previousBlockHash = None
        self.transactionList = None
        self.proofNumber = None
        self.timestamp = None

    @property
    def blockHash(self):
        hash = SHA3_256.new()
        hash.update(self.blockData.encode())
        hexHash = hash.hexdigest()

        return hexHash

    @staticmethod
    def verifyProof(proofNumber: int, previousProofNumber: int):
        guess = f"{proofNumber}{previousProofNumber}".encode()

        hash = MD5.new()
        hash.update(guess)
        attempt = hash.hexdigest()

        return attempt[:4] == "0000"

    def fromDict(self, blockDict: dict):
        if (
            not blockDict["index"]
            or not blockDict["previousBlockHash"]
            or not blockDict["transactionList"]
            or not blockDict["proofNumber"]
        ):
            return "Not enough data points in dict"

        self.index = blockDict["index"]
        self.previousBlockHash = blockDict["previousBlockHash"]
        self.transactionList = blockDict["transactionList"]
        self.proofNumber = blockDict["proofNumber"]
        if blockDict.timestamp:
            self.timestamp = blockDict["timestamp"]
        elif not blockDict.timestamp:
            self.timestamp = time.time()

        validateTypesResult = self.validateTypes(self)
        if validateTypesResult != True:
            self.index = None
            self.previousBlockHash = None
            self.transactionList = None
            self.proofNumber = None
            self.timestamp = None

        return validateTypesResult

    def toDict(self, blockObject: object):
        if (
            not blockObject.index
            or not blockObject.previousBlockHash
            or not blockObject.transactionList
            or not blockObject.proofNumber
            or not blockObject.timestamp
        ):
            return "Not enough data points in object"

        validateTypesResult = self.validateTypes(blockObject)
        if validateTypesResult != True:
            return validateTypesResult

        return {
            "index": blockObject.index,
            "previousBlockHash": blockObject.previousBlockHash,
            "transactionList": blockObject.transactionList,
            "timstamp": blockObject.timestamp,
            "proofNumber": blockObject.proofNumber,
        }

    @staticmethod
    def validateTypes(block: object):
        if type(block.index) != int:
            return "Incorrect index type"
        elif type(block.previousBlockHash) != str:
            return "Incorrect previous block hash type"
        elif type(block.transactionList) != list:
            return "Incorrect transaction list type"
        elif type(block.proofNumber) != int:
            return "Incorrect proof number type"
        elif type(block.timestamp) != float:
            return "Incorrect timestamp type"

        return True

    def validateBlocks(self, block: object, previousBlock: object):
        blockTypesResult = self.validateTypes(block)
        previousBlockTypesResult = self.validateTypes(previousBlock)

        if blockTypesResult != True:
            return blockTypesResult
        elif previousBlockTypesResult != True:
            return previousBlockTypesResult

        if not self.verifyProof(block.proofNumber, previousBlock.proofNumber):
            return "Incorrect proof"

        if block.previousBlockHash != previousBlock.blockHash:
            return "Incorrect previous block hash"

        elif block.index <= previousBlock.index:
            return "Incorrect index"

        elif block.timestamp <= previousBlock.timestamp:
            return "Incorrect timestamp"

        return True
