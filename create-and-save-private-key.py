from wallet import Wallet

privateKeyPassword = input("Please enter your private key password: ")

wallet = Wallet.getInstance()
print(wallet.createPrivateKey())
print(wallet.savePrivateKey(privateKeyPassword))
