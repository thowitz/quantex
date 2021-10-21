from hashlib import sha3_256
from ecdsa import SigningKey, SECP256k1
from transaction import Transaction


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
        publicKey: str = None,
        privateKey: str = None,
        instanceExists: bool = False,
    ):
        if not instanceExists:
            raise RuntimeError(
                f"{self.__class__.__name__} is a singleton, use the getInstance class method."
            )

        if not publicKey or not privateKey:
            signingKey = SigningKey.generate(SECP256k1, hashfunc=sha3_256)
            verifyingKey = signingKey.verifying_key

            publicKey = verifyingKey.to_string("compressed").hex()
            privateKey = signingKey.to_string().hex()

        self.publicKey = publicKey
        self.privateKey = privateKey

    def transferCoins(self, amount: int, recipientPublicKey: str):
        transaction = Transaction(amount, self.publicKey, recipientPublicKey)

        transaction.signTransaction(self.privateKey)

        newTransaction = transaction.transactionData

        return newTransaction