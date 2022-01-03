Explanations:

Block syntax:
{
"index": int,
"previousBlockHash": string,
"transactionList": list,
"timstamp": int,
"proofNumber": int,
}

Creating a transaction (pretty much just what the wallet transfer coins method does):
You create a dict of an unsigned transaction with the amount, sender public key and recipient public key
You then create a new transaction class instance and pass the dict to the unsignedTransactionFromDict method
This adds the values of the dict to the class instance, creating an object
You then call the sign transaction method, passing in your private key, which signs the unsigned transaction dict
This creates a new attribute called signedTransaction with the transaction dict and signature inside a new dict

    def processProspectiveTransactions(self, prospectiveTransactions: list):
        validateTransactionsResult = Transaction.validateTransactions(
            prospectiveTransactions
        )

        if validateTransactionsResult != True:
            return validateTransactionsResult

        transactionList = []

        for transaction in prospectiveTransactions:
            transactionToDictResult = Transaction().unsignedTransactionToDict(
                transaction
            )
            if transactionToDictResult != True:
                return transactionToDictResult

            transactionList.append(transactionToDictResult)

        self.transactionPool.extend(transactionList)

        return True

Adding your transaction to the blockchain:
You make a request to the transaction-pool/new endpoint of all the nodes, passing in a list of your prospective transactions
For each transaction, the blockchain validates the data types for every value and if the signature is valid
The transactions are then converted to dicts

Validator cli and gui:
Master container with main validator program, including basic wallet cli
Validator electron gui created using react with ionic
Gui will display validation statistics
Make request to master container api, requiring passing wallet password if a wallet exists
Master container will create api key for validator gui to use and respond to the api request with it
Validator gui saves api key and can now communicate with master container
Ability to add wallet via gui and secure gui

Wallet gui:
Validator electron gui created using react with ionic
Validator section in settings of pc edition to add existing chain file location saved by validator container
Wallet ui allows for transactions and implements cross device syncing of wallet

Possible wallet cli container structure (if there's enough demand):
Master container implementing wallet
Validator section to add existing chain file location saved by validator container
Wallet cli allows for transactions and implements cross device syncing of wallet
