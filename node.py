import requests
from transaction import Transaction


class Node:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls(instanceExists=True)
        return cls._instance

    @classmethod
    def reset(cls):
        cls._instance = None

    def __init__(self, instanceExists: bool = False):
        if not instanceExists:
            raise RuntimeError(
                f"{self.__class__.__name__} is a singleton, use the getInstance class method."
            )

        nodes = []
        savedNodesFile = open("nodes.txt")
        for node in savedNodesFile.readlines():
            nodes.append(node.strip())

        savedNodesFile.close()

        self.nodes = nodes

        self.transactionPool = []

        for node in self.nodes:
            prospectiveNodes = requests.get(f"http://{node}/nodes/current")
            prospectiveTransactions = requests.get(
                f"http://{node}/transaction-pool/current"
            )
            self.processProspectiveNodes(prospectiveNodes)
            self.processProspectiveTransactions(prospectiveTransactions)

    def processProspectiveNodes(self, prospectiveNodes: list):
        newNodes = []

        savedNodesFile = open("nodes.txt", "a")

        for node in prospectiveNodes:
            if not node in self.nodes:
                newNodes.append(node)
                savedNodesFile.write(f"{node}/n")

        savedNodesFile.close()

        if newNodes:
            self.nodes.extend(newNodes)
            return True
        return False

    def processProspectiveTransactions(self, prospectiveTransactions: list):
        validateTransactionsResult = Transaction.validateTransactions(prospectiveTransactions)
        
        if validateTransactionsResult != True:
            return validateTransactionsResult
        
        self.transactionPool.extend(prospectiveTransactions)
        
        return True
