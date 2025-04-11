import hashlib
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from enum import Enum
import random
import json  # For saving and loading the blockchain and validators

# Enum for transaction types
class TransactionType(Enum):
    EXPENDITURE = "Expenditure"
    FUNDS_RECEIVED = "Funds Received"
    SALARY = "Salary"
    GRANT = "Grant"
    LOAN = "Loan"
    INVESTMENT = "Investment"

# Validator class
@dataclass
class Validator:
    address: str
    last_validation: float = 0
    reputation: float = 1.0

# Block class
class Block:
    def __init__(self, block_id: str, timestamp: str, previous_hash: str, ministry: Dict[str, Any], 
                 transactions: List[Dict[str, Any]], funding_sources: Dict[str, Any], 
                 expenditures: Dict[str, Any], remaining_budget: float, auditor_remarks: str, 
                 smart_contract: Dict[str, Any], validator: str):
        self.block_id = block_id
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.ministry = ministry
        self.transactions = transactions
        self.funding_sources = funding_sources
        self.expenditures = expenditures
        self.remaining_budget = remaining_budget
        self.auditor_remarks = auditor_remarks
        self.smart_contract = smart_contract
        self.validator = validator
        self.nonce = 0
        self.current_hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = (
            f"{self.block_id}{self.timestamp}{self.previous_hash}"
            f"{str(self.ministry)}{str(self.transactions)}"
            f"{str(self.funding_sources)}{str(self.expenditures)}"
            f"{str(self.remaining_budget)}{self.auditor_remarks}"
            f"{str(self.smart_contract)}{self.validator}{self.nonce}"
        )
        return hashlib.sha256(block_string.encode()).hexdigest()

# Blockchain class
class Blockchain:

    def get_all_wallet_balances(self) -> Dict[str, float]:
        """Calculate the balance of all wallets by replaying all transactions in the blockchain."""
        balances = {}
        for block in self.chain:
            for transaction in block.transactions:
                sender = transaction["sender"]
                recipient = transaction["recipient"]
                amount = transaction["amount"]

                # Deduct amount from sender's balance
                if sender in balances:
                    balances[sender] -= amount
                else:
                    balances[sender] = -amount

                # Add amount to recipient's balance
                if recipient in balances:
                    balances[recipient] += amount
                else:
                    balances[recipient] = amount

        # Ensure all fixed wallets are included, even if they have a zero balance
        for wallet in self.fixed_nodes["ministries"].values():
            if wallet not in balances:
                balances[wallet] = 0.0
        for wallet in self.fixed_nodes["parastatals"].values():
            if wallet not in balances:
                balances[wallet] = 0.0
        if self.fixed_nodes["national_govt"] not in balances:
            balances[self.fixed_nodes["national_govt"]] = 0.0

        return balances
    
    def __init__(self, save_file: str = "blockchain.json", validators_file: str = "validators.json"):
        self.chain: List[Block] = []
        self.pending_transactions: List[Dict[str, Any]] = []
        self.validators: Dict[str, Validator] = {}  # Key: wallet address, Value: Validator object
        self.save_file = save_file
        self.validators_file = validators_file
        
        # Fixed nodes (ministries, parastatals, and national government)
        self.fixed_nodes = {
            "national_govt": "NG-001",
            "ministries": {
                "education": "EDU-001",
                "health": "HLT-001",
                "finance": "FIN-001",
                "ict": "ICT-001",
                "agriculture": "AGR-001"
            },
            "parastatals": {
                "kemsa": "KEMSA-001",
                "kenha": "KENHA-001",
                "kebs": "KEBS-001",
                "universities": "UNIV-001",
                "iebs": "IEBS-001"
            }
        }
        
        # Define ministry rules
        self.ministry_rules = {
            "NG-001": {"max_transaction": 100000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value]},
            "EDU-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "HLT-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "FIN-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "AGR-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "ICT-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
        }
        
        # Define parastatal rules
        self.parastatals_rules = {
            "KEMSA-001": {"max_transaction": 100000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value]},
            "KENHA-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "KEBS-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "UNIV-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
            "IEBS-001": {"max_transaction": 5000000, "allowed_types": [TransactionType.FUNDS_RECEIVED.value, TransactionType.EXPENDITURE.value]},
        }
        
        # Load blockchain from file if it exists
        self.load_blockchain()
        if not self.chain:
            self.create_genesis_block()

        # Load validators from file if it exists
        self.load_validators()

    def calculate_wallet_balance(self, wallet: str) -> float:
        """Calculate the balance of a wallet by replaying all transactions in the blockchain."""
        balance = 0.0
        for block in self.chain:
            for transaction in block.transactions:
                if transaction["sender"] == wallet:
                    balance -= transaction["amount"]
                if transaction["recipient"] == wallet:
                    balance += transaction["amount"]
        return balance

    def create_genesis_block(self):
        genesis_block = Block(
            block_id="0",
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            previous_hash="0",
            ministry={},
            transactions=[],
            funding_sources={},
            expenditures={},
            remaining_budget=0.0,
            auditor_remarks="Genesis Block",
            smart_contract={},
            validator="SYSTEM"
        )
        self.chain.append(genesis_block)
        self.save_blockchain()  # Save the blockchain after creating the genesis block

    def save_blockchain(self):
        """Save the blockchain to a file."""
        with open(self.save_file, "w") as f:
            # Convert blocks to dictionaries
            chain_data = [block.__dict__ for block in self.chain]
            json.dump(chain_data, f, indent=4)

    def load_blockchain(self):
        """Load the blockchain from a file."""
        try:
            with open(self.save_file, "r") as f:
                chain_data = json.load(f)
                for block_data in chain_data:
                    # Convert dictionaries back to Block objects
                    block = Block(
                        block_id=block_data["block_id"],
                        timestamp=block_data["timestamp"],
                        previous_hash=block_data["previous_hash"],
                        ministry=block_data["ministry"],
                        transactions=block_data["transactions"],
                        funding_sources=block_data["funding_sources"],
                        expenditures=block_data["expenditures"],
                        remaining_budget=block_data["remaining_budget"],
                        auditor_remarks=block_data["auditor_remarks"],
                        smart_contract=block_data["smart_contract"],
                        validator=block_data["validator"]
                    )
                    block.nonce = block_data["nonce"]
                    block.current_hash = block_data["current_hash"]
                    self.chain.append(block)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty blockchain
            self.chain = []

    def save_validators(self):
        """Save validators to a file."""
        with open(self.validators_file, "w") as f:
            # Convert validators to a dictionary
            validators_data = {address: validator.__dict__ for address, validator in self.validators.items()}
            json.dump(validators_data, f, indent=4)

    def load_validators(self):
        """Load validators from a file."""
        try:
            with open(self.validators_file, "r") as f:
                validators_data = json.load(f)
                for address, validator_data in validators_data.items():
                    # Convert dictionaries back to Validator objects
                    self.validators[address] = Validator(**validator_data)
        except FileNotFoundError:
            # If the file doesn't exist, start with an empty validators dictionary
            self.validators = {}

    def get_latest_block(self) -> Block:
        if not self.chain:
            return None
        return self.chain[-1]

    def register_validator(self, address: str):
        """Register a validator with a wallet address."""
        if address in self.validators:
            print(f"Validator with address {address} already exists.")
            return
        self.validators[address] = Validator(address=address)
        self.save_validators()  # Save validators to file
        print(f"Registered validator {address}.")

    def get_validators(self) -> Dict[str, Validator]:
        """Return a dictionary of validators and their details."""
        return self.validators

    def select_validator(self) -> str:
        if not self.validators:
            raise ValueError("No validators registered")
        return random.choice(list(self.validators.keys()))

    def validate_transaction(self, transaction: Dict[str, Any]) -> bool:
        # Check ministry rules (if applicable)
        if transaction.get("ministry_code") in self.ministry_rules:
            rules = self.ministry_rules[transaction["ministry_code"]]
            if "max_transaction" in rules and transaction["amount"] > rules["max_transaction"]:
                return False
            if "allowed_types" in rules and transaction["type"] not in rules["allowed_types"]:
                return False
        
        # Check parastatal rules (if applicable)
        if transaction.get("ministry_code") in self.parastatals_rules:
            rules = self.parastatals_rules[transaction["ministry_code"]]
            if "max_transaction" in rules and transaction["amount"] > rules["max_transaction"]:
                return False
            if "allowed_types" in rules and transaction["type"] not in rules["allowed_types"]:
                return False
        
        # Check if the sender has sufficient balance
        sender_balance = self.calculate_wallet_balance(transaction["sender"])
        if sender_balance < transaction["amount"]:
            print(f"Insufficient balance in sender wallet: {transaction['sender']}.")
            return False
        
        return True

    def add_transaction(self, transaction: Dict[str, Any]):
        # Check if the sender and recipient are valid wallets
        valid_wallets = list(self.fixed_nodes["ministries"].values()) + \
                        list(self.fixed_nodes["parastatals"].values()) + \
                        [self.fixed_nodes["national_govt"]]
        
        if transaction.get("sender") not in valid_wallets:
            print(f"Invalid sender wallet: {transaction.get('sender')}.")
            return False
        if transaction.get("recipient") not in valid_wallets:
            print(f"Invalid recipient wallet: {transaction.get('recipient')}.")
            return False

        # Validate the transaction
        if not self.validate_transaction(transaction):
            raise ValueError("Transaction validation failed")
        
        # Add the transaction to the pending list
        self.pending_transactions.append(transaction)
        return True

    def mine_pending_transactions(self, ministry: Dict[str, Any], funding_sources: Dict[str, Any],
                                expenditures: Dict[str, Any], remaining_budget: float,
                                auditor_remarks: str, smart_contract: Dict[str, Any]):
        validator_address = self.select_validator()
        latest_block = self.get_latest_block()
        previous_hash = latest_block.current_hash if latest_block else "0"
        
        new_block = Block(
            block_id=str(len(self.chain)),
            timestamp=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            previous_hash=previous_hash,
            ministry=ministry,
            transactions=self.pending_transactions,
            funding_sources=funding_sources,
            expenditures=expenditures,
            remaining_budget=remaining_budget,
            auditor_remarks=auditor_remarks,
            smart_contract=smart_contract,
            validator=validator_address
        )

        while not new_block.current_hash.startswith('0'):
            new_block.nonce += 1
            new_block.current_hash = new_block.calculate_hash()

        self.chain.append(new_block)
        self.pending_transactions = []
        self.save_blockchain()  # Save the blockchain after mining a new block