import hashlib
import json
import datetime
import os


# -------------------------------
# Block Class
# -------------------------------

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": str(self.timestamp),
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()


# -------------------------------
# Blockchain Class
# -------------------------------

class Blockchain:
    def __init__(self, ledger_file="blockchain_ledger.json"):
        self.ledger_file = ledger_file
        self.chain = []
        self.load_chain()

    # Create Genesis Block
    def create_genesis_block(self):
        return Block(
            index=0,
            timestamp=str(datetime.datetime.now()),
            data="Genesis Block",
            previous_hash="0"
        )

    # Load existing blockchain from file
    def load_chain(self):
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file, "r") as f:
                chain_data = json.load(f)

                for block_data in chain_data:
                    block = Block(
                        block_data["index"],
                        block_data["timestamp"],
                        block_data["data"],
                        block_data["previous_hash"]
                    )
                    block.hash = block_data["hash"]
                    self.chain.append(block)
        else:
            genesis_block = self.create_genesis_block()
            self.chain.append(genesis_block)
            self.save_chain()

    # Save blockchain to file
    def save_chain(self):
        with open(self.ledger_file, "w") as f:
            json.dump([block.__dict__ for block in self.chain], f, indent=4)

    # Get latest block
    def get_latest_block(self):
        return self.chain[-1]

    # Add new block
    def add_block(self, data):
        latest_block = self.get_latest_block()

        new_block = Block(
            index=len(self.chain),
            timestamp=str(datetime.datetime.now()),
            data=data,
            previous_hash=latest_block.hash
        )

        self.chain.append(new_block)
        self.save_chain()

        return new_block.hash

    # Validate entire chain
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            if current.hash != current.calculate_hash():
                return False

            if current.previous_hash != previous.hash:
                return False

        return True