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
        self.pending_transactions: List[Dict[str, Any]] = []  # This is the correct name
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

    def add_transaction(self, transaction: Dict[str, Any]) -> bool:
        try:
            # Extended required fields
            required_fields = ["sender", "recipient", "amount"]
            optional_fields = ["purpose", "approved_by", "extra_info"]
            
            if not all(field in transaction for field in required_fields):
                print("Missing required fields")
                return False

            # Convert amount to float
            amount = float(transaction["amount"])

            # Allow negative amounts but ensure sender has sufficient balance
            if transaction["sender"] != "SYSTEM":
                sender_balance = self.calculate_wallet_balance(transaction["sender"])
                if sender_balance + amount < 0:
                    print(f"Insufficient balance: {sender_balance} + {amount} < 0")
                    return False

            # Create transaction with enhanced details
            new_transaction = {
                "sender": transaction["sender"],
                "recipient": transaction["recipient"],
                "amount": amount,
                "timestamp": transaction.get("timestamp") or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "date": time.strftime("%Y-%m-%d", time.gmtime()),
                "purpose": transaction.get("purpose", "No purpose specified"),
                "approved_by": transaction.get("approved_by", "Not specified"),
                "extra_info": transaction.get("extra_info", ""),
                "transaction_id": hashlib.sha256(f"{time.time()}{transaction['sender']}{transaction['recipient']}".encode()).hexdigest()[:16]
            }

            self.pending_transactions.append(new_transaction)
            return True

        except (KeyError, ValueError, TypeError) as e:
            print(f"Invalid transaction: {e}")
            return False

    async def mine_block(self, miner_address, active_connections):
        try:
            block = Block(
                block_id=str(len(self.chain)),
                timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                previous_hash=self.chain[-1].current_hash if self.chain else "0",
                transactions=self.pending_transactions,
                validator=miner_address
            )
            
            # Add block to chain and clear pending transactions
            self.chain.append(block)
            self.pending_transactions = []
            
            # Broadcast the new block to all connected clients
            if active_connections:
                message = {
                    "type": "new_block",
                    "data": {
                        "block_id": block.block_id,
                        "transactions": block.transactions,
                        "timestamp": block.timestamp,
                        "validator": block.validator
                    }
                }
                
                # Get list of disconnected clients
                disconnected_clients = []
                
                # Send to all connected clients
                for wallet_address, connection in active_connections.items():
                    try:
                        await connection.send_json(message)
                    except Exception as e:
                        print(f"Failed to send to {wallet_address}: {e}")
                        disconnected_clients.append(wallet_address)
                
                # Remove disconnected clients
                for wallet_address in disconnected_clients:
                    active_connections.pop(wallet_address, None)
            
            return block
        except Exception as e:
            print(f"Error mining block: {e}")
            raise

    def get_all_wallet_balances(self) -> Dict[str, float]:
        balances = {}
        
        # Process all blocks in chronological order
        for block in self.chain:
            for transaction in block.transactions:
                sender = transaction["sender"]
                recipient = transaction["recipient"]
                amount = abs(float(transaction["amount"]))  # Convert to positive float
                
                # Skip invalid transactions
                if amount <= 0:
                    continue
                    
                # Initialize wallets if they don't exist
                if sender not in balances:
                    balances[sender] = 0.0
                if recipient not in balances:
                    balances[recipient] = 0.0
                    
                # Verify sender has sufficient balance
                if sender != "SYSTEM" and balances[sender] < amount:
                    continue  # Skip invalid transaction
                    
                # Process the transaction
                if sender != "SYSTEM":  # Don't deduct from SYSTEM account
                    balances[sender] -= amount
                balances[recipient] += amount
                
        return balances

    def calculate_wallet_balance(self, wallet: str) -> float:
        balance = 0.0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == wallet:
                    balance -= transaction["amount"]  # Deduct amount sent
                if transaction["recipient"] == wallet:
                    balance += transaction["amount"]  # Add amount received
        return balance

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
        Each transaction includes enhanced transaction details.
        """
        transactions_all = []
        for block in self.chain:
            for transaction_all in block.transactions:
                sender = transaction_all["sender"]
                recipient = transaction_all["recipient"]
                amount = transaction_all["amount"]

                # Prepare base transaction details
                transaction_details = {
                    "transaction_id": transaction_all.get("transaction_id", "N/A"),
                    "date": transaction_all.get("date", "N/A"),
                    "purpose": transaction_all.get("purpose", "No purpose specified"),
                    "approved_by": transaction_all.get("approved_by", "Not specified"),
                    "extra_info": transaction_all.get("extra_info", ""),
                    "timestamp": transaction_all.get("timestamp", "N/A")
                }

                if sender == wallet:
                    transactions_all.append({
                        "type": "outgoing",
                        "counterparty": recipient,
                        "amount": -amount,
                        **transaction_details
                    })

                if recipient == wallet:
                    transactions_all.append({
                        "type": "incoming",
                        "counterparty": sender,
                        "amount": amount,
                        **transaction_details
                    })

        return transactions_all

    def validate_chain(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            
            # Validate block hash
            if current.previous_hash != previous.current_hash:
                return False
                
            # Validate all transactions in block
            balances = {}
            for tx in current.transactions:
                sender = tx["sender"]
                amount = abs(float(tx["amount"]))
                
                if sender != "SYSTEM":
                    balances[sender] = balances.get(sender, 0) - amount
                    if balances[sender] < 0:
                        return False
                        
        return True