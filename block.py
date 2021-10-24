from Crypto.Hash import SHA3_256
from Crypto.Hash import MD5
import time


class Block:
    def __init__(
        self,
        index: int,
        previousBlockHash: str,
        transactionList: list,
        proofNumber: int,
    ):
        self.index = index
        self.previousBlockHash = previousBlockHash
        self.transactionList = transactionList
        self.proofNumber = proofNumber

        self.blockData = {
            "index": self.index,
            "previousBlockHash": self.previousBlockHash,
            "transactionList": self.transactionList,
            "timestamp": time.time(),
            "proofNumber": proofNumber,
        }

    @property
    def blockHash(self):
        hash = SHA3_256.new()
        hash.update(self.blockData.encode())
        hexHash = hash.hexdigest()

        print(self.blockData)
        print(hexHash)

        return hexHash

    @staticmethod
    def verifyProof(proofNumber, previousProofNumber):
        guess = f"{proofNumber}{previousProofNumber}".encode()

        hash = MD5.new()
        hash.update(guess)
        attempt = hash.hexdigest()

        return attempt[:4] == "0000"

    @staticmethod
    def validateBlocks(block: dict, previousBlock: dict):
        print(type(block["transactionList"]))
        if type(block["index"]) != int:
            return "Incorrect index type"
        elif type(block["previousBlockHash"]) != str:
            return "Incorrect previous block hash type"
        elif type(block["transactionList"]) != list:
            return "Incorrect transaction list type"
        elif type(block["timestamp"]) != float:
            return "Incorrect timestamp type"

        if not Block.verifyProof(block["proofNumber"], previousBlock["proofNumber"]):
            return "Incorrect proof"

        if block["previousBlockHash"] != previousBlock["blockHash"]:
            return "Incorrect previous block hash"

        elif block["index"] <= previousBlock["index"]:
            return "Incorrect index"

        elif block["timestamp"] <= previousBlock["timestamp"]:
            return "Incorrect timestamp"

        return True
