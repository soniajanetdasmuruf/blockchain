
"""
TUGAS PERSONAL — Lima Modifikasi Level 1–5
"""

import copy

import level01_hash as L1
import level02_blok as L2
import level03_tampering as L3
import level04_transaksi as L4
import level05_pow_nonce as L5


# ============================================================== MODIFIKASI 1
def sidik_jari(nama: str, nim4: str, tanggal_lahir: str) -> str:
    """ID mahasiswa = 8 karakter pertama dari hash data pribadi."""
    data = f"{nim4}:{nama}:{tanggal_lahir}"
    return L1.sha256_hex(data)[:8]


# ============================================================== MODIFIKASI 2
class BlockchainPersonal(L2.Blockchain):
    """Blockchain personal dengan proof genesis dari NIM."""

    def __init__(self, nim4: str, id_mhs: str, difficulty: int = 4):
        self.difficulty = difficulty
        self.id_mhs = id_mhs
        self.chain = []

        # Genesis memakai proof dari empat digit terakhir NIM
        self.create_block(
            proof=int(nim4),
            previous_hash="0"
        )

    def create_block(self, proof: int, previous_hash: str) -> dict:
        # Buat blok menggunakan fungsi Level 2
        block = super().create_block(proof, previous_hash)

        # Tambahkan identitas pemilik pada setiap blok
        block["pemilik"] = self.id_mhs

        return block


# ============================================================== MODIFIKASI 3
def palsukan(chain: list, posisi: int):
    """
    Mengubah data pada satu blok, lalu menyambungkan ulang rantai.
    Rantai asli tidak boleh berubah.
    """
    data_asli = chain[posisi]["data"]
    data_palsu = data_asli + " (DIPALSUKAN)"

    # Ubah blok menggunakan fungsi Level 3
    palsu = L3.ubah_blok(
        chain,
        posisi,
        "data",
        data_palsu
    )

    # Sambungkan ulang mulai dari blok setelah blok yang dipalsukan
    disambung = L3.sambung_ulang(
        palsu,
        posisi + 1
    )

    return palsu, disambung


# ============================================================== MODIFIKASI 4
def ringkasan_saldo(bc, nama: str) -> dict:
    """Menghitung uang masuk, keluar, dan saldo bersih."""

    masuk = 0
    keluar = 0

    for _, tx in bc.riwayat(nama):
        if tx["recipient"] == nama:
            masuk += tx["amount"]

        if tx["sender"] == nama:
            keluar += tx["amount"]

    return {
        "masuk": masuk,
        "keluar": keluar,
        "bersih": masuk - keluar
    }


# ============================================================== MODIFIKASI 5
class BlockchainDeterministik(L5.Blockchain):
    """
    Blockchain Level 5 dengan timestamp tetap berdasarkan tanggal lahir.
    """

    def __init__(
        self,
        tanggal_lahir: str,
        id_mhs: str,
        difficulty: int = 4
    ):
        self.difficulty = difficulty
        self.tanggal_lahir = tanggal_lahir
        self.chain = []

        # Buat blok genesis deterministik
        genesis = {
            "index": 0,
            "timestamp": self.tanggal_lahir,
            "transactions": [f"GENESIS {id_mhs}"],
            "previous_hash": "0" * 64,
            "nonce": 0
        }

        # Lakukan proof of work dan masukkan genesis ke rantai
        self.proof_of_work(genesis)
        self.chain.append(genesis)

    def new_block(self, transactions: list) -> dict:
        """Membuat blok baru dengan timestamp deterministik."""

        previous_block = self.chain[-1]
        index = len(self.chain)

        block = {
            "index": index,
            "timestamp": f"{self.tanggal_lahir} #{index}",
            "transactions": transactions,
            "previous_hash": self.hash_block(previous_block),
            "nonce": 0
        }

        # Mining blok baru
        self.proof_of_work(block)

        # Masukkan blok ke rantai
        self.chain.append(block)

        return block
