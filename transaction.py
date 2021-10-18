from Crypto.Hash import SHA3_256
from Crypto.Signature import pss


class Transaction:
    def __init__(self, amount, senderPublicKey, recipientPublicKey):
        self.amount = amount
        self.senderPublicKey = senderPublicKey
        self.recipientPublicKey = recipientPublicKey

        self.rawTransactionData = {
            "amount": self.amount,
            "senderPublicKey": self.senderPublicKey,
            "recipientPublicKey": self.recipientPublicKey,
        }

    def signTransaction(self, privateKey):
        hash = SHA3_256.new(self.rawTransactionData)
        signature = pss.new(privateKey).sign(hash)

        self.signature = signature

    @property
    def transactionData(self):
        return {
            "transaction": self.rawTransactionData,
            "signature": self.signature,
        }

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