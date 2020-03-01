from flask import Flask,render_template, request
from flask import jsonify
from block_chain import BlockChain, Transaction

osaCoin=BlockChain()
osaCoin.createTransaction(Transaction('address1','address2',100))
osaCoin.createTransaction(Transaction('address2','address1',50))

app = Flask(__name__)

@app.route("/mine",methods=['GET'])
def mine():
    return "we are going to mine the block with new transations here"

@app.route('/transactions/new',methods=['POST'])
def new_transation():
    return None

@app.route("/", methods=["GET", "POST"])
def hello():
    if request.method == "POST":
        osaCoin.minePendingTransaction("osamaaddress")
    return  render_template('index.html',pending_transactions=osaCoin.pendingTransations)

if __name__=="__main__":
    app.run(debug=True)
