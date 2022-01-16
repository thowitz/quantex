from Crypto.Hash import SHA3_256
from Crypto.Hash import MD5
import time
import json


class Block:
    def __init__(self):
        self.index = None
        self.previousBlockHash = None
        self.transactionList = None
        self.proofNumber = None
        self.timestamp = None

    @property
    # easy access to hash of block
    def blockHash(self):
        hash = SHA3_256.new()

        # converts the object to a dict and then hashes as you can't really hash an object
        blockData = self.toDict(self)
        blockDataString = json.dumps(blockData)

        hash.update(blockDataString.encode())
        hexHash = hash.hexdigest()

        return hexHash

    # simple temporary algorithm to find a hash where the first 4 characters are 0000
    @staticmethod
    def verifyProof(proofNumber: int, previousProofNumber: int):
        guess = f"{proofNumber}{previousProofNumber}".encode()

        hash = MD5.new()
        hash.update(guess)
        attempt = hash.hexdigest()

        return attempt[:4] == "0000"

    def fromDict(self, blockDict: dict):
        # verify enough of the data points exist in the dict
        if (
            (not blockDict["index"] and blockDict["index"] != 0)
            or (
                not blockDict["previousBlockHash"]
                and blockDict["previousBlockHash"] != ""
            )
            or (not blockDict["transactionList"] and blockDict["transactionList"] != [])
            or (not blockDict["proofNumber"] and blockDict["proofNumber"] != 0)
        ):
            return "Not enough data points in dict"

        # the self variables get set and then self gets passed to validate types as it only takes objects
        self.index = blockDict["index"]
        self.previousBlockHash = blockDict["previousBlockHash"]
        self.transactionList = blockDict["transactionList"]
        self.proofNumber = blockDict["proofNumber"]
        if blockDict["timestamp"]:
            self.timestamp = round(blockDict["timestamp"])
        elif not blockDict["timestamp"]:
            self.timestamp = round(time.time())

        validateTypesResult = self.validateTypes(self)
        if validateTypesResult != True:
            self.index = None
            self.previousBlockHash = None
            self.transactionList = None
            self.proofNumber = None
            self.timestamp = None

        return validateTypesResult

    def toDict(self, blockObject: object):
        # verify enough of the data points exist in the object
        if (
            (not blockObject.index and blockObject.index != 0)
            or (
                not blockObject.previousBlockHash
                and blockObject.previousBlockHash != ""
            )
            or (not blockObject.transactionList and blockObject.transactionList != [])
            or (not blockObject.proofNumber and blockObject.proofNumber != 0)
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
            "timestamp": blockObject.timestamp,
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
        elif type(block.timestamp) != int:
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

        elif (
            block.timestamp <= previousBlock.timestamp
            or block.timestamp >= previousBlock.timestamp + 300
        ):
            return "Incorrect timestamp"

        return True
