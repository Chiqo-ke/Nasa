from gok import Blockchain, TransactionType

def add_funds_to_national_wallet():
    # Initialize blockchain (load from file)
    blockchain = Blockchain(save_file="blockchain.json")

    # Prompt the user for the amount to add
    try:
        amount = float(input("Enter the amount to add to the national wallet: "))
        if amount <= 0:
            print("Amount must be greater than 0.")
            return
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    # Create a transaction to add funds to the national wallet
    transaction = {
        "sender": "SYSTEM",  # Special sender for adding funds
        "recipient": blockchain.fixed_nodes["national_govt"],  # National wallet
        "amount": amount,
        "type": TransactionType.FUNDS_RECEIVED.value,
        "ministry_code": "NG-001"  # National government code
    }

    # Add the transaction to the blockchain
    blockchain.add_transaction(transaction)

    # Mine the pending transactions
    blockchain.mine_pending_transactions(
        ministry={"name": "National Government"},
        funding_sources={},
        expenditures={},
        remaining_budget=amount,  # Update the remaining budget
        auditor_remarks="Added funds to national wallet",
        smart_contract={}
    )

    print(f"Added {amount} to the national wallet.")

def send_funds(sender_wallet: str, recipient_wallet: str, amount: float):
    # Initialize blockchain (load from file)
    blockchain = Blockchain(save_file="blockchain.json")

    # Check if the sender and recipient wallets are valid
    valid_wallets = list(blockchain.fixed_nodes["ministries"].values()) + \
                    list(blockchain.fixed_nodes["parastatals"].values()) + \
                    [blockchain.fixed_nodes["national_govt"]]
    
    if sender_wallet not in valid_wallets:
        print(f"Invalid sender wallet: {sender_wallet}.")
        return
    if recipient_wallet not in valid_wallets:
        print(f"Invalid recipient wallet: {recipient_wallet}.")
        return

    # Create a transaction
    transaction = {
        "sender": sender_wallet,
        "recipient": recipient_wallet,
        "amount": amount,
        "type": TransactionType.FUNDS_RECEIVED.value,
        "ministry_code": "NG-001"  # Default ministry code
    }

    # Add the transaction to the blockchain
    if blockchain.add_transaction(transaction):
        # Mine the pending transactions
        blockchain.mine_pending_transactions(
            ministry={"name": "National Government"},
            funding_sources={},
            expenditures={},
            remaining_budget=amount,  # Update the remaining budget
            auditor_remarks=f"Sent funds from {sender_wallet} to {recipient_wallet}",
            smart_contract={}
        )
        print(f"Sent {amount} from {sender_wallet} to {recipient_wallet}.")

def list_validators():
    # Initialize blockchain (load from file)
    blockchain = Blockchain(save_file="blockchain.json")

    # Get the list of validators
    validators = blockchain.get_validators()

    if not validators:
        print("No validators registered.")
        return

    print("Registered Validators:")
    for address, validator in validators.items():
        print(f"Address: {address}")

def register_validator():
    # Initialize blockchain (load from file)
    blockchain = Blockchain(save_file="blockchain.json")

    # Prompt the user for validator details
    address = input("Enter the validator's wallet address: ")

    # Register the validator
    blockchain.register_validator(address)
    
def display_all_wallet_balances():
    # Initialize blockchain (load from file)
    blockchain = Blockchain(save_file="blockchain.json")

    # Get all wallet balances
    balances = blockchain.get_all_wallet_balances()

    if not balances:
        print("No wallets found.")
        return

    print("\nWallet Balances:")
    for wallet, balance in balances.items():
        print(f"{wallet}: {balance}")

# Example usage
if __name__ == "__main__":
    while True:
        print("\n1. Add funds to national wallet")
        print("2. Send funds between wallets")
        print("3. List validators")
        print("4. Register validator")
        print("5. Display all wallet balances")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_funds_to_national_wallet()
        elif choice == "2":
            sender_wallet = input("Enter the sender's wallet address: ")
            recipient_wallet = input("Enter the recipient's wallet address: ")
            try:
                amount = float(input("Enter the amount to send: "))
                if amount <= 0:
                    print("Amount must be greater than 0.")
                else:
                    send_funds(sender_wallet, recipient_wallet, amount)
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == "3":
            list_validators()
        elif choice == "4":
            register_validator()
        elif choice == "5":
            display_all_wallet_balances()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")