from wallet import Wallet

wallet = Wallet.getInstance()
wallet.createPrivateKey()
wallet.savePrivateKey("thanks for all the fish")
