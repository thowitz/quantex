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

    def syncNodesAndTransactionPool(self):
        currentNodesResponses = self.makeNetworkRequest("/nodes/current")
        currentTransactionPoolResponses = self.makeNetworkRequest(
            "/transaction-pool/current"
        )

        if currentNodesResponses and type(currentNodesResponses) != str:
            for currentNodesResponse in currentNodesResponses:
                self.processProspectiveNodes(currentNodesResponse.content)
        else:
            return currentNodesResponses

        if (
            currentTransactionPoolResponses
            and type(currentTransactionPoolResponses) != str
        ):
            for currentTransactionPoolResponse in currentTransactionPoolResponses:
                self.processProspectiveTransactions(currentTransactionPoolResponse)
        else:
            return currentTransactionPoolResponses

    def makeNetworkRequest(self, path):
        possibleOfflineNodes = []
        responses = []

        if path[0] == "/":
            path = path[1:]

        print(f"Making request to network at /{path}")

        for validatorNode in self.nodes:
            try:
                response = requests.get(f"http://{validatorNode}/{path}", timeout=1)
                responses.append(response)
            except:
                possibleOfflineNodes.append(validatorNode)

            if len(possibleOfflineNodes) > 1:
                print(
                    f"\r{len(possibleOfflineNodes)} out of {len(self.nodes)} nodes unavailable",
                    end="",
                )

        if possibleOfflineNodes:
            print("")
            if possibleOfflineNodes != self.nodes:
                self.processPossibleOfflineValidators(possibleOfflineNodes)
            # if every validator is offline, chances are we're in fact the ones offline
            elif possibleOfflineNodes and possibleOfflineNodes == self.nodes:
                return "Offline"

        return responses

    def processProspectiveNodes(self, prospectiveNodes: list):
        # todo update before pos implementation
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

    def processPossibleOfflineNodes(self, possibleOfflineNodes: list):
        # todo finish before pos implementation
        pass

    # this function is here because it appends to the transaction pool which is part of the node class,
    # it could be put in the transaction class if you're really that ocd about it
    # maybe I'll change it after I've checked off some more things on the to do list
    def processProspectiveTransactions(self, prospectiveTransactions: list):
        validateTransactionsResult = Transaction.validateTransactions(
            prospectiveTransactions, blockRewardAllowed=False
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
