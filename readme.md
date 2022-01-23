Important notice:

This is by no means ready for production, it's just a small, fun project. I will probably not continue development as it would take a metric butt ton of work to be even slightly useful as a cryptocurrency and I want to move on to other things. The quantex file and other files that tie the methods together are pretty rubbish, but some of the classes may be useful to someone looking to create their own cryptocurrency.




Explanations:

Block syntax:
{
"index": int,
"previousBlockHash": str,
"transactionList": list,
"timestamp": int,
"proofNumber": int,
}

Creating a transaction (pretty much just what the wallet transfer coins method does):
You create a dict of an unsigned transaction with the amount, sender public key and recipient public key
You then create a new transaction class instance and pass the dict to the unsignedTransactionFromDict method
This adds the values of the dict to the class instance, creating an object
You then call the sign transaction method, passing in your private key, which signs the unsigned transaction dict
This creates a new attribute called signedTransaction with the transaction dict and signature inside a new dict

Adding your transaction to the blockchain:
You make a request to the transaction-pool/new endpoint of all the nodes, passing in a list of your prospective transactions
For each transaction, the blockchain validates the data types for every value and if the signature is valid
The transactions are then converted to dicts and added to the mining pool
