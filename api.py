from flask import Flask, request, jsonify
from core.transaction import Transaction
from core.mempool import Mempool
from core.chain import Blockchain
from ai.ai_core import AstraAI

app = Flask(__name__)

mempool = Mempool()
chain = Blockchain()
ai = AstraAI()

@app.route("/send_tx", methods=["POST"])
def send_tx():
    data = request.json
    tx = Transaction(data["sender"], data["receiver"], data["amount"])
    mempool.add_tx(tx)
    return jsonify({"tx_id": tx.tx_id, "status": "added"})

@app.route("/mine", methods=["POST"])
def mine():
    if not mempool.transactions:
        return jsonify({"error": "No transactions"}), 400
    risk, bot = ai.analyze_block(mempool.transactions)
    if not bot and ai.filter.approve_block(risk):
        chain.add_block(mempool.transactions)
        mempool.clear()
        return jsonify({"status": "Block mined", "risk": risk})
    return jsonify({"status": "Block rejected", "risk": risk, "bot_detected": bot})

@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "chain_length": len(chain.chain),
        "mempool_size": len(mempool.transactions)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
