
import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.difficulty = difficulty
        self.chain = []
        # Blok genesis (blok pertama)
        self.create_block(proof=1, previous_hash="0")

    # ---------- SUDAH DISEDIAKAN ----------
    def create_block(self, proof: int, previous_hash: str) -> dict:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

    def last_block(self) -> dict:
        return self.chain[-1]

    # ---------- BAGIAN YANG DIKERJAKAN ----------
    def hash(self, block: dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_proof(self, previous_proof: int, proof: int) -> bool:
        value = proof**2 - previous_proof**2

        guess = str(value).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash.startswith("0" * self.difficulty)

    def proof_of_work(self, previous_proof: int) -> int:
        new_proof = 1

        while not self.valid_proof(previous_proof, new_proof):
            new_proof += 1

        return new_proof

    def mine_block(self) -> dict:
        previous_block = self.last_block()

        previous_proof = previous_block["proof"]

        proof = self.proof_of_work(previous_proof)

        previous_hash = self.hash(previous_block)

        block = self.create_block(proof, previous_hash)

        return block

    def chain_valid(self, chain: list) -> bool:
        for i in range(1, len(chain)):
            current_block = chain[i]
            previous_block = chain[i - 1]

            # Periksa hubungan hash antarblok
            if current_block["previous_hash"] != self.hash(previous_block):
                return False

            # Periksa Proof of Work
            if not self.valid_proof(
                previous_block["proof"],
                current_block["proof"]
            ):
                return False

        return True


if __name__ == "__main__":
    bc = Blockchain(difficulty=4)

    for _ in range(4):
        b = bc.mine_block()
        print(f"Blok #{b['index']} ditambang, proof={b['proof']}")

    print(json.dumps(bc.chain, indent=2))
    print("Rantai valid?", bc.chain_valid(bc.chain))
