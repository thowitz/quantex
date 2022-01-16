from hashlib import sha3_256
from ecdsa import SigningKey, SECP256k1
from Crypto.Hash import SHA3_256
from cryptography.fernet import Fernet, InvalidToken
from transaction import Transaction
import json
import base64
import os


class Wallet:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls(instanceExists=True)
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None

    def __init__(
        self,
        instanceExists: bool = False,
    ):
        if not instanceExists:
            raise RuntimeError(
                f"{self.__class__.__name__} is a singleton, use the getInstance class method."
            )

        self.publicKey = None
        self.privateKey = None

    def createPrivateKey(self):
        if not self.privateKey:
            signingKey = SigningKey.generate(SECP256k1, hashfunc=sha3_256)

            privateKey = signingKey.to_string().hex()
            self.privateKey = privateKey

            return self.privateKey

    def privateKeyPasswordToObject(self, privateKeyPassword: str):
        hash = SHA3_256.new()
        hash.update(privateKeyPassword.encode())

        privateKeyPasswordB64Bytes = base64.urlsafe_b64encode(hash.digest())
        privateKeyPasswordObject = Fernet(privateKeyPasswordB64Bytes)

        return privateKeyPasswordObject

    def calculatePublicKey(self, privateKey: str = None):
        if not privateKey:
            privateKey = self.privateKey

        signingKey = SigningKey.from_string(
            bytearray.fromhex(privateKey), curve=SECP256k1, hashfunc=sha3_256
        )
        verifyingKey = signingKey.verifying_key

        publicKey = verifyingKey.to_string("compressed").hex()
        self.publicKey = publicKey

        return self.publicKey

    def decryptPrivateKey(self, savedEncryptedPrivateKey: str, privateKeyPassword: str):
        privateKeyPasswordObject = self.privateKeyPasswordToObject(privateKeyPassword)

        try:
            privateKey = privateKeyPasswordObject.decrypt(
                savedEncryptedPrivateKey.encode()
            )
        except InvalidToken:
            return "Token is malformed or does not have a valid signature"
        except TypeError:
            return "Incorrect token type"

        self.privateKey = privateKey.decode()

        return True

    def savePrivateKey(self, privateKeyPassword: str, privateKey: str = None):
        if not privateKey:
            privateKey = self.privateKey

        privateKeyPasswordObject = self.privateKeyPasswordToObject(privateKeyPassword)

        try:
            encryptedPrivateKey = privateKeyPasswordObject.encrypt(privateKey.encode())
        except TypeError:
            return "Incorrect data type"

        savedPrivateKeyFile = open("private-key.json", "w")
        privateKeyJson = {"encryptedPrivateKey": encryptedPrivateKey.decode()}
        savedPrivateKeyFile.write(json.dumps(privateKeyJson, indent=4))
        savedPrivateKeyFile.close()

        return encryptedPrivateKey

    def transferCoins(self, amount: int, recipientPublicKey: str):
        if not self.publicKey or not self.privateKey:
            return "Public key or private key not part of this instance"

        unsignedTransactionDict = {
            "amount": amount,
            "senderPublicKey": self.publicKey,
            "recipientPublicKey": recipientPublicKey,
        }

        transaction = Transaction()
        transactionFromDictResult = transaction.unsignedTransactionFromDict(
            unsignedTransactionDict
        )

        if transactionFromDictResult != True:
            return transactionFromDictResult

        transaction.signTransaction(self.privateKey)

        newTransaction = transaction.signedTransaction

        return newTransaction
