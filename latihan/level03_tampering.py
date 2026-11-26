
import copy
import datetime
import hashlib
import json


# ====================== SUDAH DISEDIAKAN ======================
def hash_blok(block: dict) -> str:
    return hashlib.sha256(
        json.dumps(block, sort_keys=True).encode()
    ).hexdigest()


class Blockchain:
    """Blockchain gaya GfG + field data."""

    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        self.create_block(
            proof=1,
            previous_hash="0",
            data="GENESIS"
        )

    def create_block(self, proof, previous_hash, data):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

    def valid_proof(self, previous_proof, proof):
        h = hashlib.sha256(
            str(proof**2 - previous_proof**2).encode()
        ).hexdigest()
        return h.startswith("0" * self.difficulty)

    def mine_block(self, data):
        prev = self.chain[-1]
        proof = 1

        while not self.valid_proof(prev["proof"], proof):
            proof += 1

        return self.create_block(
            proof,
            hash_blok(prev),
            data
        )

    def chain_valid(self, chain):
        for i in range(1, len(chain)):
            if chain[i]["previous_hash"] != hash_blok(chain[i - 1]):
                return False

            if not self.valid_proof(
                chain[i - 1]["proof"],
                chain[i]["proof"]
            ):
                return False

        return True


# ============ BAGIAN YANG DIKERJAKAN ============

def ubah_blok(chain: list, posisi: int, field: str, nilai) -> list:
    """Mengubah data blok tanpa mengubah rantai asli."""

    palsu = copy.deepcopy(chain)

    palsu[posisi][field] = nilai

    return palsu


def cari_tautan_putus(chain: list):
    """Mencari indeks pertama yang tautannya terputus."""

    for i in range(1, len(chain)):
        if chain[i]["previous_hash"] != hash_blok(chain[i - 1]):
            return i

    return None


def sambung_ulang(chain: list, mulai: int) -> list:
    """Menyambungkan ulang hash antarblok tanpa mining ulang."""

    baru = copy.deepcopy(chain)

    for i in range(max(1, mulai), len(baru)):
        baru[i]["previous_hash"] = hash_blok(baru[i - 1])

    return baru


if __name__ == "__main__":
    bc = Blockchain(difficulty=3)

    for d in [
        "Ani -> Budi: 5",
        "Budi -> Citra: 2",
        "Citra -> Dodi: 1"
    ]:
        bc.mine_block(d)

    print("Asli valid?           ", bc.chain_valid(bc.chain))

    palsu = ubah_blok(
        bc.chain,
        1,
        "data",
        "Ani -> Budi: 500"
    )

    print("Setelah diubah valid? ", bc.chain_valid(palsu))
    print("Tautan putus di indeks", cari_tautan_putus(palsu))

    disambung = sambung_ulang(palsu, 2)

    print(
        "Setelah disambung ulang valid?",
        bc.chain_valid(disambung),
        "<-- masalah!"
    )
