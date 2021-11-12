from hashlib import sha3_256
from ecdsa import SigningKey, VerifyingKey, SECP256k1, BadSignatureError
import json


class Transaction:
    def __init__(self):
        self.amount = None
        self.senderPublicKey = None
        self.recipientPublicKey = None

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
        if not self.signature or not self.unsignedTransactionDict:
            return False

        return {
            "transaction": self.unsignedTransactionDict,
            "signature": self.signature,
        }

    def unsignedTransactionFromDict(self, unsignedTransactionDict: dict):
        if (
            not unsignedTransactionDict["amount"]
            or not unsignedTransactionDict["senderPublicKey"]
            or not unsignedTransactionDict["recipeintPublicKey"]
        ):
            return "Not enough data points in dict"

        self.amount = unsignedTransactionDict["amount"]
        self.senderPublicKey = unsignedTransactionDict["senderPublicKey"]
        self.recipientPublicKey = unsignedTransactionDict["recipeintPublicKey"]

        validateTypesResult = self.validateTypes(self)
        if validateTypesResult != True:
            self.amount = None
            self.senderPublicKey = None
            self.recipientPublicKey = None

        return validateTypesResult

    def unsignedTransactionToDict(self, unsignedTransactionObject: object):
        if (
            not unsignedTransactionObject.amount
            or not unsignedTransactionObject.senderPublicKey
            or not unsignedTransactionObject.recipeintPublicKey
        ):
            return "Not enough data points in object"

        validateTypesResult = self.validateTypes(unsignedTransactionObject)
        if validateTypesResult != True:
            return validateTypesResult
        
        self.unsignedTransactionDict = {
            "amount": unsignedTransactionObject.amount,
            "senderPublicKey": unsignedTransactionObject.senderPublicKey,
            "recipientPublicKey": unsignedTransactionObject.recipientPublicKey,
        }

        return self.unsignedTransactionDict

    @staticmethod
    def validateTypes(transaction: object):
        if type(transaction.amount) != float:
            return "Incorrect transaction amount type"
        elif type(transaction.senderPublicKey) != str:
            return "Incorrect sender public key type"
        elif type(transaction.recipientPublicKey) != str:
            return "Incorrect recipient public key type"

        return True

    def validateTransactions(self, transactionList: list):
        for signedTransaction in transactionList:
            transactionTypesResult = self.validateTypes(signedTransaction.transaction)
            if transactionTypesResult != True:
                return transactionTypesResult

            verifyingKey = VerifyingKey.from_string(
                signedTransaction.transaction.senderPublicKey
            )

            try:
                verifyingKey.verify(
                    signedTransaction.signature, signedTransaction, sha3_256
                )
            except (ValueError, TypeError, BadSignatureError):
                return "Incorrect signature"

        return True