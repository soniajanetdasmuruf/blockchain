
import hashlib
import json

SISTEM = "0"
MINING_REWARD = 10


class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.difficulty = difficulty
        self.pending_transactions = []
        genesis = {
            "index": 0,
            "transactions": [],
            "previous_hash": "0" * 64,
            "nonce": 0
        }
        self._tambang(genesis)
        self.chain = [genesis]

    @staticmethod
    def hash_block(block):
        isi = {k: v for k, v in block.items() if k != "hash"}
        return hashlib.sha256(
            json.dumps(isi, sort_keys=True).encode()
        ).hexdigest()

    def _tambang(self, block):
        block["nonce"] = 0
        while not self.hash_block(block).startswith("0" * self.difficulty):
            block["nonce"] += 1
        block["hash"] = self.hash_block(block)
        return block

    def saldo(self, alamat: str, termasuk_pending: bool = True) -> float:
        total = 0

        # Hitung transaksi yang sudah masuk ke blockchain
        for block in self.chain:
            for tx in block["transactions"]:
                if tx["recipient"] == alamat:
                    total += tx["amount"]

                if tx["sender"] == alamat:
                    total -= tx["amount"]

        # Hitung transaksi yang masih menunggu jika diminta
        if termasuk_pending:
            for tx in self.pending_transactions:
                if tx["recipient"] == alamat:
                    total += tx["amount"]

                if tx["sender"] == alamat:
                    total -= tx["amount"]

        return total

    def add_transaction(self, sender: str, recipient: str, amount) -> None:
        # 1. Sistem tidak boleh mengirim transaksi biasa
        if sender == SISTEM:
            raise ValueError("Transaksi dari sistem hanya boleh dibuat saat mining")

        # 2. Jumlah transaksi harus lebih dari nol
        if amount <= 0:
            raise ValueError("Jumlah transaksi harus lebih dari 0")

        # 3. Saldo pengirim harus mencukupi
        if self.saldo(sender, termasuk_pending=True) < amount:
            raise ValueError("Saldo tidak mencukupi")

        self.pending_transactions.append({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        })

    def mine(self, alamat_penambang: str) -> dict:
        # Buat transaksi hadiah mining di posisi pertama
        coinbase = {
            "sender": SISTEM,
            "recipient": alamat_penambang,
            "amount": MINING_REWARD
        }

        # Gabungkan coinbase dengan transaksi yang menunggu
        transactions = [coinbase] + self.pending_transactions.copy()

        # Ambil blok terakhir
        blok_terakhir = self.chain[-1]

        # Buat blok baru
        block = {
            "index": len(self.chain),
            "transactions": transactions,
            "previous_hash": self.hash_block(blok_terakhir),
            "nonce": 0
        }

        # Lakukan mining
        self._tambang(block)

        # Masukkan blok ke blockchain
        self.chain.append(block)

        # Kosongkan transaksi yang sudah masuk blok
        self.pending_transactions = []

        return block

    def total_suplai(self) -> float:
        total = 0

        for block in self.chain:
            for tx in block["transactions"]:
                if tx["sender"] == SISTEM:
                    total += tx["amount"]

        return total

    def validasi_ekonomi(self) -> bool:
        saldo = {}

        # Genesis tidak memiliki transaksi ekonomi
        for block in self.chain[1:]:
            transactions = block["transactions"]

            # Setiap blok harus memiliki transaksi
            if not transactions:
                return False

            # Transaksi pertama harus berupa coinbase yang benar
            coinbase = transactions[0]

            if coinbase["sender"] != SISTEM:
                return False

            if coinbase["amount"] != MINING_REWARD:
                return False

            # Tidak boleh ada transaksi sistem selain coinbase
            for tx in transactions[1:]:
                if tx["sender"] == SISTEM:
                    return False

            # Putar ulang seluruh transaksi dalam urutan blok
            for tx in transactions:
                sender = tx["sender"]
                recipient = tx["recipient"]
                amount = tx["amount"]

                if amount <= 0:
                    return False

                # Transaksi coinbase menciptakan coin baru
                if sender == SISTEM:
                    saldo[recipient] = saldo.get(recipient, 0) + amount

                else:
                    # Pengirim harus memiliki saldo yang cukup
                    if saldo.get(sender, 0) < amount:
                        return False

                    saldo[sender] = saldo.get(sender, 0) - amount
                    saldo[recipient] = saldo.get(recipient, 0) + amount

        return True


if __name__ == "__main__":
    bc = Blockchain()

    bc.mine("ani")
    bc.add_transaction("ani", "budi", 4)
    bc.mine("citra")

    for nama in ("ani", "budi", "citra"):
        print(f"Saldo {nama}: {bc.saldo(nama)}")

    print("Total suplai:", bc.total_suplai())

    try:
        bc.add_transaction("budi", "dodi", 100)
    except ValueError as e:
        print("Ditolak:", e)

    print("Validasi ekonomi:", bc.validasi_ekonomi())
