import json
from block import Block

configFile = open("config.json")
config = json.load(configFile)
configFile.close()

genesisBlock = Block()
genesisBlock.fromDict(config["genesisBlock"]["blockData"])

config["genesisBlock"]["hash"] = genesisBlock.blockHash

configFile = open("config.json", "w")
json.dump(config, configFile, indent=2)
configFile.close()
