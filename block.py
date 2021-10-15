from Crypto.Hash import SHA3_256
import time


class Block:
    def __init__(self, previousHash, transaction, timestamp=None):
        self.previousHash = previousHash
        self.transaction = transaction
        self.timestamp = timestamp or time.time()

    @property
    def calculateHash(self):
        string = "{}{}{}{}{}".format(
            self.previousHash, self.transaction, self.timestamp
        )

        hash = SHA3_256.new()
        hash.update(string.encode())
        hexHash = hash.hexdigest()

        print(string)
        print(hexHash)

        return hexHash
