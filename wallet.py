from Crypto.PublicKey import RSA
from transaction import Transaction


class Wallet:
    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

        key = RSA.generate(2048)
        keyPair = key.export_key("PEM")

        publicKey = keyPair.publicKey
        privateKey = keyPair.privateKey

        print(keyPair)
        print(publicKey)
        print(privateKey)

    def transferCoins(self, amount, recipientPublicKey):
        transaction = Transaction(amount, self.publicKey, recipientPublicKey)

        newTransaction = transaction.createTransaction()

        signature = transaction.signTransaction(newTransaction, self.privateKey)

        return newTransaction, signature