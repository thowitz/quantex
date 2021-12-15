from wallet import Wallet

wallet = Wallet.getInstance()
print(wallet.createPrivateKey())
print(wallet.savePrivateKey("thanks for all the fish"))
