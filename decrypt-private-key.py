from wallet import Wallet

privateKeyPassword = input("Please enter your private key password: ")

wallet = Wallet.getInstance()

if wallet.checkExistingPrivateKey():
    print(wallet.readPrivateKey(privateKeyPassword))
