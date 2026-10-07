import hashlib
import datetime
import json

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash() # Calculate its own hash upon creation

    def calculate_hash(self):
        """Calculates the SHA256 hash of the block's contents."""
        # Ensure consistent string representation for hashing
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp), # Convert datetime to string
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode('utf-8') # sort_keys ensures consistent order
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    """Manages the chain of blocks."""
    def __init__(self):
        self.chain = []
        self.create_genesis_block() # Start with the first block

    def create_genesis_block(self):
        """Creates the very first block in the chain."""
        # The genesis block has index 0 and a previous_hash of "0"
        self.chain.append(Block(0, datetime.datetime.now(), "Genesis Block", "0"))

    def get_latest_block(self):
        """Returns the last block in the chain."""
        return self.chain[-1]

    def add_block(self, new_block_data):
        """Adds a new block to the blockchain."""
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_timestamp = datetime.datetime.now()
        new_previous_hash = previous_block.hash # Link to the previous block's hash

        # Create the new block and add it to the chain
        new_block = Block(new_index, new_timestamp, new_block_data, new_previous_hash)
        self.chain.append(new_block)
        print(f"Block #{new_block.index} added to the chain.")
        print(f"  Timestamp: {new_block.timestamp}")
        print(f"  Data: {new_block.data}")
        print(f"  Previous Hash: {new_block.previous_hash}")
        print(f"  Current Hash: {new_block.hash}\n")

    def is_chain_valid(self):
        """Verifies the integrity of the entire blockchain."""
        # Iterate through the chain, starting from the second block (index 1)
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # Check 1: Does the current block's stored hash match its actual content?
            # If data within current_block was changed without recalculating its hash, this fails.
            if current_block.hash != current_block.calculate_hash():
                print(f"Integrity check failed: Block {current_block.index}'s hash is incorrect.")
                return False

            # Check 2: Does the current block's previous_hash correctly point to the hash of the actual previous block?
            # If the previous block's data was changed (and its hash recalculated), or if the link was broken, this fails.
            if current_block.previous_hash != previous_block.hash:
                print(f"Integrity check failed: Block {current_block.index}'s previous_hash link is broken.")
                return False
        return True

# --- Main execution --- 
if __name__ == "__main__":
    # Initialize our simple blockchain
    my_blockchain = Blockchain()
    print("Blockchain initialized with Genesis Block.\n")

    # Add some blocks to the chain, demonstrating data storage
    # This simulates adding new transactions or data to the ledger, a core DLT concept.
    my_blockchain.add_block({"sender": "Alice", "receiver": "Bob", "amount": 10})
    my_blockchain.add_block({"sender": "Bob", "receiver": "Charlie", "amount": 5})
    my_blockchain.add_block("Dev News Digest: AI, ML, Cloud, DLT are key trends!") # Data can be any serializable object

    # Print the entire chain for verification
    print("--- Current Blockchain State ---")
    for block in my_blockchain.chain:
        print(f"Block {block.index}:")
        print(f"  Timestamp: {block.timestamp}")
        print(f"  Data: {block.data}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Hash: {block.hash}\n")

    # Verify the chain's integrity initially
    if my_blockchain.is_chain_valid():
        print("Blockchain is valid and untampered!\n")
    else:
        print("Blockchain integrity compromised! (Unexpected at this stage)\n")

    # --- Demonstrate Tampering ---
    print("--- Attempting to tamper with Block #1's data ---")
    # We will change the data of an existing block without re-mining it or subsequent blocks.
    # This simulates a malicious attempt to alter historical data.
    original_data_block1 = my_blockchain.chain[1].data
    my_blockchain.chain[1].data = {"sender": "Alice", "receiver": "Bob", "amount": 9999} # Change amount
    print(f"  Changed Block #1 data from {original_data_block1} to {my_blockchain.chain[1].data}")
    # Crucially, we do NOT recalculate my_blockchain.chain[1].hash here.
    # This means my_blockchain.chain[1].hash will still hold the OLD hash.

    # Now, re-verify the chain. It should detect the tampering.
    print("\n--- Re-verifying Blockchain after tampering attempt ---")
    if my_blockchain.is_chain_valid():
        print("Blockchain is valid after attempted tampering (this indicates a flaw in the demo or understanding!)")
    else:
        print("Blockchain integrity compromised after attempted tampering! (Expected behavior for DLTs)")
        print("This demonstrates how cryptographic linking makes DLTs resistant to unauthorized data changes.")