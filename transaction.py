from Crypto.Hash import SHA3_256
from Crypto.Signature import pss


class Transaction:
    def __init__(self, amount, senderPublicKey, recipientPublicKey):
        self.amount = amount
        self.senderPublicKey = senderPublicKey
        self.recipientPublicKey = recipientPublicKey

    def createTransaction(self):
        return {
            "amount": self.amount,
            "senderPublicKey": self.senderPublicKey,
            "recipientPublicKey": self.recipientPublicKey,
        }

    @staticmethod
    def signTransaction(transaction, privateKey):
        hash = SHA3_256.new(transaction)
        signature = pss.new(privateKey).sign(hash)

        return signature

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