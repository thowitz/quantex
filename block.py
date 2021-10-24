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
        guess = f"{proofNumber}{previousProofNumber}"

        hash = MD5.new()
        hash.update(guess)
        attempt = hash.hexdigest()

        return attempt[:4] == "0000"

    def validateBlocks(self, block: dict, previousBlock: dict):
        if type(block.index) != int:
            return False
        elif type(block.previousBlockHash) != str:
            return False
        elif type(block.transactionList) != list:
            return False
        elif type(block.timestamp) != float:
            return False

        if not self.verifyProof(block.proofNumber, previousBlock.proofNumber):
            return False

        if block.previousBlockHash != previousBlock.blockHash:
            return False

        elif block.index <= previousBlock.index:
            return False

        elif block.timestamp <= previousBlock.timestamp:
            return False

        return True
