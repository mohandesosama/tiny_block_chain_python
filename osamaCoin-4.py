import hashlib
import json
from datetime import datetime
from time import time
from uuid import uuid4
from flask import Flask
from flask import jsonify
from pprint import pprint

class Block():
    def __init__(self,nonce,tstamp,transactionsList,prevhash='',hash=''):
        self.nonce=nonce
        self.tstamp=tstamp
        self.transactionsList=transactionsList # list of dictionary values
        self.prevhash=prevhash
        if hash == '':
            self.hash=self.calcHash()
        else:
            self.hash=hash
    def calcHash(self):
        block_string=json.dumps({"nonce":self.nonce,"tstamp":str(self.tstamp),"transacitons":self.transactionsList,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self,diffic):
        while(self.hash[:diffic] != "0"*diffic):
            self.nonce += 1
            self.hash=self.calcHash()
    def toDict(self):
        return {"nonce":self.nonce,"tstamp":str(self.tstamp),"transactionsList":self.transactionsList,"prevhash":self.prevhash,"hash":self.hash}


class BlockChain():
    def __init__(self):
        self.chain=[]
        self.pendingTransations=[]
        self.mining_reward=100
        self.difficulty=3
        self.generateGenesisBlock()

    def generateGenesisBlock(self):
        dect={"nonce":0,"tstamp":'01/01/2017',"transactionsList":[{"from_address":None,"to_address":None,"amount":0},],"hash":''}
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
        self.pendingTransations.append({
            'from_address': from_address,
            'to_address': to_address,
            'amount': amount,
        })
    
    def isChainValid(self):
        for index in range(1,len(self.chain)):
            currb=Block(**self.chain[index])
            prevb=Block(**self.chain[index-1])
            if currb.hash != currb.calcHash():
                return False
            if currb.prevhash != prevb.hash:
                return False
        return True

    def calcBalance(self,address):
        balance = 0
        for index in range(len(self.chain)):
            dicList= self.chain[index]["transactionsList"]
            for dic in dicList:
                if dic["to_address"]==address:
                    balance += dic["amount"]
                if dic["from_address"]==address:
                    balance -= dic["amount"]
        return balance
           


bchain=BlockChain()
bchain.createTransaction('add1','add2',100)
bchain.createTransaction('add2','add1',100)
bchain.minePendingTransatin('osama')
bchain.createTransaction('add1','add2',40)
bchain.createTransaction('add2','add1',30)
bchain.minePendingTransatin('osama')

app=Flask(__name__)

node_id=str(uuid4()).replace('-','')

@app.route("/mine",methods=['GET'])
def mine():
    return "we'll mine a new block"

@app.route('/transactions/new',methods=['POST'])
def new_transaction():
    return "we'll add a new transaction here"

@app.route('/chain',methods=['GET'])
def full_chain():
    response = {
        'chain':bchain.chain,
        'length':len(bchain.chain),
    }
    return jsonify(response), 200

@app.route("/")
def hello():
    return "Hello, you are in the main page of the node"

if __name__=="__main__":
    app.run()

