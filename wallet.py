from Crypto.PublicKey import RSA
from Crypto.Hash import SHA3_256
from Crypto.Signature import pss

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
    
    def transferCoins(self, amount, recipientPublicKey, blockchain):
        transaction = Transaction(amount, self.publicKey, recipientPublicKey)
        
        hash = SHA3_256.new(transaction)
        signature = pss.new(self.privateKey).sign(hash)
        
        blockchain.constructBlock(transaction, self.publicKey, signature)