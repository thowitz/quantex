from blockchain import BlockChain
from block import Block
from transaction import Transaction
from wallet import Wallet

blockchain = BlockChain.getInstance()

wallet = Wallet()

newTransaction = Transaction(100, "genesis", "tim")
newTransaction.signTransaction(wallet.privateKey)

blockchain.appendBlock(Block(0, None, [newTransaction.transactionData]).blockData)

print(blockchain.chain)