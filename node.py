from core.transaction import Transaction
from core.mempool import Mempool
from core.chain import Blockchain
from ai.ai_core import AstraAI

mempool = Mempool()
chain = Blockchain()
ai = AstraAI()

def cli():
    while True:
        cmd = input("\nEnter command (send/mine/status/exit): ").strip().lower()
        
        if cmd == "send":
            sender = input("Sender: ")
            receiver = input("Receiver: ")
            amount = float(input("Amount: "))
            tx = Transaction(sender, receiver, amount)
            mempool.add_tx(tx)
            print(f"Transaction added: {tx.tx_id}")

        elif cmd == "mine":
            if not mempool.transactions:
                print("No transactions to mine.")
                continue
            risk, bot = ai.analyze_block(mempool.transactions)
            print(f"Average risk: {risk:.2f}")
            print(f"Bot detected: {bot}")
            if not bot and ai.filter.approve_block(risk):
                chain.add_block(mempool.transactions)
                mempool.clear()
                print("Block mined successfully!")
            else:
                print("Block rejected by AI.")

        elif cmd == "status":
            print(f"Chain length: {len(chain.chain)}")
            print(f"Mempool size: {len(mempool.transactions)}")

        elif cmd == "exit":
            print("Exiting...")
            break
        else:
            print("Unknown command. Use: send, mine, status, exit")

if __name__ == "__main__":
    print("=== AstraNet Core Node with AI ===")
    cli()
