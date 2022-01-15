from wallet import Wallet

privateKeyPassword = input("Please enter your private key password: ")

wallet = Wallet.getInstance()

if wallet.checkExistingPrivateKey():
    print("\nPrivate key:")
    print(wallet.readPrivateKey(privateKeyPassword))
    print("\nPublic key:")
    print(wallet.calculatePublicKey())
