
import datetime
import hashlib
import json


class Blockchain:
    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []

        genesis = {
            "index": 0,
            "timestamp": str(datetime.datetime.now()),
            "transactions": [],
            "previous_hash": "0" * 64,
            "nonce": 0,
        }

        self.proof_of_work(genesis)
        self.chain.append(genesis)

    # ---------- BAGIAN YANG DIKERJAKAN ----------

    @staticmethod
    def hash_block(block: dict) -> str:
        """Hash seluruh isi blok tanpa menyertakan key hash."""

        data = {
            k: v for k, v in block.items()
            if k != "hash"
        }

        block_string = json.dumps(data, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, block: dict) -> int:
        """Mencari nonce sampai hash memenuhi difficulty."""

        nonce = 0
        percobaan = 0

        while True:
            block["nonce"] = nonce

            hasil_hash = self.hash_block(block)
            percobaan += 1

            if hasil_hash.startswith("0" * self.difficulty):
                block["hash"] = hasil_hash
                return percobaan

            nonce += 1

    def new_block(self, transactions: list) -> dict:
        """Membuat dan menambang blok baru."""

        previous_block = self.chain[-1]

        block = {
            "index": previous_block["index"] + 1,
            "timestamp": str(datetime.datetime.now()),
            "transactions": transactions,
            "previous_hash": previous_block["hash"],
            "nonce": 0,
        }

        self.proof_of_work(block)

        self.chain.append(block)

        return block

    def chain_valid(self) -> bool:
        """Memeriksa validitas seluruh rantai Blockchain."""

        for i, block in enumerate(self.chain):

            # Periksa hash blok
            if block.get("hash") != self.hash_block(block):
                return False

            # Periksa difficulty
            if not block["hash"].startswith("0" * self.difficulty):
                return False

            # Periksa hubungan dengan blok sebelumnya
            if i > 0:
                if block["previous_hash"] != self.chain[i - 1]["hash"]:
                    return False

        return True

    def tambang_ulang_dari(self, posisi: int) -> int:
        """Menambang ulang blok mulai dari posisi tertentu."""

        total_percobaan = 0

        for i in range(posisi, len(self.chain)):

            block = self.chain[i]

            # Perbarui previous_hash jika bukan genesis
            if i > 0:
                block["previous_hash"] = self.chain[i - 1]["hash"]

            # Mulai ulang nonce dan lakukan mining
            block["nonce"] = 0

            percobaan = self.proof_of_work(block)

            total_percobaan += percobaan

        return total_percobaan


if __name__ == "__main__":
    bc = Blockchain(difficulty=4)

    for tx in (
        ["Ani->Budi 5"],
        ["Budi->Citra 2"],
        ["Citra->Dodi 1"]
    ):
        b = bc.new_block(tx)

        print(
            f"Blok #{b['index']} "
            f"nonce={b['nonce']} "
            f"hash={b['hash'][:16]}..."
        )

    print("Valid?", bc.chain_valid())

    bc.chain[1]["transactions"] = ["Ani->Budi 500"]

    print("Setelah diubah valid?", bc.chain_valid())

    usaha = bc.tambang_ulang_dari(1)

    print(
        f"Penyerang menambang ulang dengan "
        f"{usaha} percobaan hash. Valid?",
        bc.chain_valid()
    )
