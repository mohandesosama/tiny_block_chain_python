from flask import Flask,render_template
from flask import jsonify
from block_chain import BlockChain

osaCoin=BlockChain()
osaCoin.createTransaction('address1','address2',100)
osaCoin.createTransaction('address2','address1',50)
print("Starting mining")
osaCoin.minePendingTransatin("osamaaddress")
print("Osama miner blanace is ", osaCoin.getBalance("osamaaddress"))
print(osaCoin.isChainValid())

app = Flask(__name__)

@app.route("/mine",methods=['GET'])
def mine():
    return "we are going to mine the block with new transations here"

@app.route('/transactions/new',methods=['POST'])
def new_transation():
    return None

@app.route("/chain",methods=['GET'])
def display_full_chain():
    response={
        'chain':osaCoin.chain,
        'length':len(osaCoin.chain)
    }
    return jsonify(response),200

@app.route("/")
def hello():
    return  render_template('index.html',chain_length=len(osaCoin.chain))

if __name__=="__main__":
    app.run(debug=True)
