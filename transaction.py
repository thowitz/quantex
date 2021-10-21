from hashlib import sha3_256
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
import json


class Transaction:
    def __init__(self, amount: int, senderPublicKey: str, recipientPublicKey: str):
        self.amount = amount
        self.senderPublicKey = senderPublicKey
        self.recipientPublicKey = recipientPublicKey

        self.unsignedTransaction = {
            "amount": self.amount,
            "senderPublicKey": self.senderPublicKey,
            "recipientPublicKey": self.recipientPublicKey,
        }

    def signTransaction(self, privateKey: str):
        signingKey = SigningKey.from_string(
            bytearray.fromhex(privateKey), SECP256k1, sha3_256
        )
        signature = signingKey.sign(
            json.dumps(self.unsignedTransaction).encode("utf-8")
        ).hex()

        self.signature = signature

    @property
    def signedTransaction(self):
        if not self.signature:
            return False

        return {
            "transaction": self.unsignedTransaction,
            "signature": self.signature,
        }

    @staticmethod
    def validateTransactions(transactionList: list):
        for signedTransaction in transactionList:
            if type(signedTransaction.transaction.amount) != float:
                return False
            elif type(signedTransaction.transaction.senderPublicKey) != str:
                return False
            elif type(signedTransaction.transaction.recipientPublicKey) != str:
                return False

            verifyingKey = VerifyingKey.from_string(
                signedTransaction.transaction.senderPublicKey
            )

            try:
                verifyingKey.verify(
                    signedTransaction.signature, signedTransaction, sha3_256
                )
            except (ValueError, TypeError, BadSignatureError):
                return False

        return True