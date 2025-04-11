# blockchain.py

import hashlib
import time
from typing import List, Dict, Any
from utils import notify_user

class Block:
    def __init__(self, block_id: str, timestamp: str, previous_hash: str, transactions: List[Dict[str, Any]], validator: str):
        self.block_id = block_id
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.validator = validator
        self.nonce = 0
        self.current_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = (
            f"{self.block_id}{self.timestamp}{self.previous_hash}"
            f"{str(self.transactions)}{self.validator}{self.nonce}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(
            block_id="0",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            previous_hash="0",
            transactions=[],
            validator="SYSTEM"
        )
        self.chain.append(genesis_block)

    def add_transaction(self, transaction: Dict[str, Any]):
        self.pending_transactions.append(transaction)

    async def mine_block(self, miner_address, active_connections):
        try:
            block = Block(
                index=len(self.chain),
                transactions=self.current_transactions,
                timestamp=time.time(),
                previous_hash=self.chain[-1].hash if self.chain else None,
                miner=miner_address
            )
            
            # Compute proof of work
            block.hash = block.compute_hash()
            
            # Reset the current list of transactions
            self.chain.append(block)
            self.current_transactions = []
            
            # Broadcast the new block to all connected clients
            if active_connections:
                message = {
                    "type": "new_block",
                    "data": {
                        "index": block.index,
                        "transactions": block.transactions,
                        "timestamp": block.timestamp,
                        "miner": block.miner
                    }
                }
                
                dead_connections = set()
                for connection in active_connections:
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        print(f"Failed to send to connection: {e}")
                        dead_connections.add(connection)
                
                # Remove dead connections
                for dead in dead_connections:
                    active_connections.remove(dead)
            
            return block
        except Exception as e:
            print(f"Error mining block: {e}")
            raise

    def get_all_wallet_balances(self) -> Dict[str, float]:
        balances = {}
        for block in self.chain:
            for transaction in block.transactions:
                sender = transaction["sender"]
                recipient = transaction["recipient"]
                amount = transaction["amount"]
                balances[sender] = balances.get(sender, 0) - amount
                balances[recipient] = balances.get(recipient, 0) + amount
        return balances

    def calculate_wallet_balance(self, wallet: str) -> float:
        return self.get_all_wallet_balances().get(wallet, 0.0)

    def get_transactions_for_wallet(self, wallet: str) -> List[Dict[str, Any]]:
        transactions = []
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == wallet or transaction["recipient"] == wallet:
                    transactions.append(transaction)
        return transactions


    def get_detailed_wallet_transactions(self, wallet: str) -> List[Dict[str, Any]]:
        """
        Get a detailed list of transactions for a specific wallet.
        Each transaction includes the sender, recipient, and amount (positive or negative).
        """
        transactions_all = []
        for block in self.chain:
            for transaction_all in block.transactions:
                sender = transaction_all["sender"]
                recipient = transaction_all["recipient"]
                amount = transaction_all["amount"]

                # If the wallet is the sender, record the transaction as negative
                if sender == wallet:
                    transactions_all.append({
                        "type": "outgoing",
                        "counterparty": recipient,
                        "amount": -amount
                    })

                # If the wallet is the recipient, record the transaction as positive
                if recipient == wallet:
                    transactions_all.append({
                        "type": "incoming",
                        "counterparty": sender,
                        "amount": amount
                    })

        return transactions_all