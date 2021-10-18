from hashlib import sha3_256
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
import json


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
        signingKey = SigningKey.from_string(
            bytearray.fromhex(privateKey), SECP256k1, sha3_256
        )
        signature = signingKey.sign(
            json.dumps(self.rawTransactionData).encode("utf-8")
        ).hex()

        self.signature = signature

    @property
    def transactionData(self):
        if not self.signature:
            return False

        return {
            "transaction": self.rawTransactionData,
            "signature": self.signature,
        }

    @staticmethod
    def validateTransactions(transactionList):
        for transaction in transactionList:
            verifyingKey = VerifyingKey.from_string(transaction.senderPublicKey)

            try:
                verifyingKey.verify(transaction.signature, transaction, sha3_256)
            except (ValueError, TypeError, BadSignatureError):
                return False

        return True