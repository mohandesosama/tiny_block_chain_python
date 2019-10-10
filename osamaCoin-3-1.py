import hashlib
import json
from datetime import datetime
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask

class Block():
    def __init__(self,nonce,tstamp,transactionsList,prevhash=''):
        self.nonce=nonce
        self.tstamp=tstamp
        self.transactionsList=transactionsList # list of dictionary values
        self.prevhash=prevhash
        self.hash=self.calcHash()
    def calcHash(self):
        block_string=json.dumps({"nonce":self.nonce,"tstamp":str(self.tstamp),"transacitons":self.transactionsList,"prevhash":self.prevhash},sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    def mineBlock(self,diffic):
        while(self.hash[:diffic] != str('').zfill(diffic)):
            self.nonce += 1
            self.hash=self.calcHash()
        return [self.hash,self.nonce]


class BlockChain():
    def __init__(self):
        self.chain=[self.generateGenesisBlock(),]
        self.pendingTransations=[]
        self.mining_reward=100
        self.difficulty=3
    def generateGenesisBlock(self):
        return {"nonce":0,"tstamp":'01/01/2017',"transactionsList":{"from_address":None,"to_address":None,"amount":0}}
    def getLastBlock(self):
        return self.chain[-1]
    def minePendingTransatin(self,mining_reward_address):
        block=Block(0,str(datetime.now()),self.pendingTransations)
        [h,n]=block.mineBlock(self.difficulty)
        print("Block is mined to got reward", self.mining_reward)
        self.chain.append({"nonce":n,"tstamp":block.tstamp,"transactionsList":block.transactionsList,"hash":h})
        self.pendingTransations={"from_address":None,"to_address":mining_reward_address,"amount":self.mining_reward}

    def createTransaction(self,from_address,to_address,amount):
        self.pendingTransations.append({
            'from_address': from_address,
            'to_address': to_address,
            'amount': amount,
        })



bchain=BlockChain()
bchain.createTransaction('add1','add2',100)
bchain.minePendingTransatin('osama')


node_id=str(uuid4()).replace('-','')
app=Flask(__name__)

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
        'length':len(bchain.chain)
    }
    return json.dumps(response).encode(),200

@app.route("/")
def hello():
    return "Hello World!"

if __name__=="__main__":
    app.run()


