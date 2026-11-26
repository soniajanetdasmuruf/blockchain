
import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        self.pending_transactions = []
        self.create_block(proof=1, previous_hash="0")

    # ---------- SUDAH DISEDIAKAN ----------
    def hash(self, block):
        return hashlib.sha256(
            json.dumps(block, sort_keys=True).encode()
        ).hexdigest()

    def valid_proof(self, previous_proof, proof):
        h = hashlib.sha256(
            str(proof**2 - previous_proof**2).encode()
        ).hexdigest()
        return h.startswith("0" * self.difficulty)

    def proof_of_work(self, previous_proof):
        proof = 1
        while not self.valid_proof(previous_proof, proof):
            proof += 1
        return proof

    def last_block(self):
        return self.chain[-1]

    # ---------- BAGIAN YANG DIKERJAKAN ----------

    def create_block(self, proof: int, previous_hash: str) -> dict:
        """Membuat blok baru dan memasukkan transaksi tertunda."""

        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "transactions": list(self.pending_transactions),
            "proof": proof,
            "previous_hash": previous_hash,
        }

        self.chain.append(block)

        # Kosongkan transaksi tertunda
        self.pending_transactions = []

        return block

    def add_transaction(self, sender: str, recipient: str, amount) -> int:
        """Menambahkan transaksi ke dalam mempool."""

        # Validasi sender
        if not isinstance(sender, str) or sender.strip() == "":
            raise ValueError("Sender harus berupa string dan tidak boleh kosong")

        # Validasi recipient
        if not isinstance(recipient, str) or recipient.strip() == "":
            raise ValueError("Recipient harus berupa string dan tidak boleh kosong")

        # Sender dan recipient tidak boleh sama
        if sender == recipient:
            raise ValueError("Sender dan recipient tidak boleh sama")

        # Validasi amount
        if isinstance(amount, bool) or not isinstance(amount, (int, float)):
            raise ValueError("Amount harus berupa angka")

        if amount <= 0:
            raise ValueError("Amount harus lebih besar dari 0")

        # Simpan transaksi
        transaksi = {
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }

        self.pending_transactions.append(transaksi)

        # Kembalikan index blok yang akan memuat transaksi
        return self.last_block()["index"] + 1

    def mine_block(self) -> dict:
        """Menambang blok baru yang berisi transaksi tertunda."""

        previous_block = self.last_block()

        previous_proof = previous_block["proof"]

        proof = self.proof_of_work(previous_proof)

        previous_hash = self.hash(previous_block)

        block = self.create_block(proof, previous_hash)

        return block

    def riwayat(self, nama: str) -> list:
        """Mencari riwayat transaksi berdasarkan nama."""

        hasil = []

        for block in self.chain:
            for tx in block["transactions"]:

                if tx["sender"] == nama or tx["recipient"] == nama:
                    hasil.append((block["index"], tx))

        return hasil


if __name__ == "__main__":
    bc = Blockchain()

    bc.add_transaction("Ani", "Budi", 5)
    bc.add_transaction("Budi", "Citra", 2)

    bc.mine_block()

    bc.add_transaction("Citra", "Ani", 1)

    bc.mine_block()

    print(json.dumps(bc.chain, indent=2))

    print("Riwayat Budi:", bc.riwayat("Budi"))
