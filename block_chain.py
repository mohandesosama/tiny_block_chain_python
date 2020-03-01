import hashlib
import json
from datetime import datetime
from time import time
#block chain created by me. 
class Block():
    def __init__(self,nonce, tstamp,transactionsList,prevhash='',hash=''):
        self.nonce=nonce
        self.tstamp=tstamp
        self.transactionsList=transactionsList
        self.prevhash=prevhash
        if hash == '':
            self.hash=self.calcHash()
        else:
            self.hash=hash
    def calcHash(self):
        block_string=json.dumps({"nonce":self.nonce,"tstamp":str(self.tstamp),"transaciton":self.transactionsList,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self,diffic):
        while(self.hash[:diffic] != str('').zfill(diffic)):
            self.nonce += 1
            self.hash=self.calcHash()
        print("Block mined ", self.hash)
    def toDict(self):
        return {"nonce":self.nonce,"tstamp":str(self.tstamp),"transactionsList":self.transactionsList,"prevhash":self.prevhash,'hash':self.hash}

class BlockChain():
    def __init__(self):
        self.chain=[]
        self.pendingTransations=[]
        self.mining_reward=70
        self.difficulty=3
        self.generateGenesisBlock()
    def generateGenesisBlock(self):
        dect={"nonce":0,"tstamp":'02/02/2017',"transactionsList":[{"from_address":None,"to_address":None,"amount":0},],"hash":''}
        b=Block(**dect)
        self.chain.append(b.toDict())
    def getLastBlock(self):
        return Block(**self.chain[-1])
    def minePendingTransatin(self,mining_reward_address):
        block=Block(0,str(datetime.now()),self.pendingTransations)
        block.prevhash=self.getLastBlock().hash
        block.mineBlock(self.difficulty)
        print("Block is mined to got reward", self.mining_reward)
        self.chain.append(block.toDict())
        self.pendingTransations=[{"from_address":None,"to_address":mining_reward_address,"amount":self.mining_reward},]

    def createTransaction(self,from_address,to_address,amount):
        self.pendingTransations.append({'from_address':from_address,'to_address':to_address,'amount':amount})
    def getBalance(self,address):
        balance=0
        for index in range(len(self.chain)):
            dictList=self.chain[index]["transactionsList"]
            for dic in dictList:
                if dic["to_address"] == address:
                    balance += dic["amount"]
                if dic["from_address"] == address:
                    balance -= dic["amount"]
        return balance 

    def isChainValid(self):
        for i in range(1,len(self.chain)):
            prevb=Block(**self.chain[i-1])
            currb=Block(**self.chain[i])
            if(currb.hash != currb.calcHash()):
                print("invalid block")
                return False
            if(currb.prevhash != prevb.hash):
                print("invalid chain")
                return False
        return True
        



