from hashlib import sha3_256
from ecdsa import SigningKey, SECP256k1
from transaction import Transaction


class Wallet:
    def __init__(self, publicKey=None, privateKey=None):
        if not publicKey or not privateKey:
            signingKey = SigningKey.generate(SECP256k1, hashfunc=sha3_256)
            verifyingKey = signingKey.verifying_key

            publicKey = verifyingKey.to_string("compressed").hex()
            privateKey = signingKey.to_string().hex()

        self.publicKey = publicKey
        self.privateKey = privateKey

    def transferCoins(self, amount, recipientPublicKey):
        transaction = Transaction(amount, self.publicKey, recipientPublicKey)

        transaction.signTransaction(self.privateKey)

        newTransaction = transaction.transactionData

        return newTransaction