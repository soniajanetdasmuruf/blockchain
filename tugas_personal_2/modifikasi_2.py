
"""
TUGAS PERSONAL 2 — Modifikasi Level 6–9
=======================================

Modifikasi:
6. Jejak difficulty
7. Kunci dan tanda tangan deterministik
8. Node personal dan kesepakatan jaringan
9. Blockchain dengan sistem halving
"""

import hashlib

from ecdsa import SECP256k1, SigningKey

import level06_difficulty as L6
import level07_tanda_tangan as L7
import level08_jaringan as L8
import level09_reward_saldo as L9


# ============================================================== MODIFIKASI 6
def jejak_difficulty(awal: int, daftar_waktu: list, target: float) -> list:
    """
    Menerapkan penyesuaian difficulty secara berulang.

    Mengembalikan daftar difficulty setelah setiap penyesuaian.
    """

    difficulty_sekarang = awal
    hasil = []

    for waktu in daftar_waktu:
        difficulty_sekarang = L6.sesuaikan_difficulty(
            difficulty_sekarang,
            waktu,
            target
        )

        hasil.append(difficulty_sekarang)

    return hasil


# ============================================================== MODIFIKASI 7
def kunci_dari_data(nama: str, nim4: str, tanggal_lahir: str):
    """
    Membuat pasangan kunci SECP256k1 secara deterministik
    berdasarkan nama, NIM, dan tanggal lahir.
    """

    data = f"{nim4}:{nama}:{tanggal_lahir}"

    hash_data = hashlib.sha256(
        data.encode("utf-8")
    ).hexdigest()

    secret = int(hash_data, 16) % SECP256k1.order

    if secret == 0:
        secret = 1

    sk = SigningKey.from_secret_exponent(
        secret,
        curve=SECP256k1
    )

    vk = sk.get_verifying_key()

    kunci_privat_hex = sk.to_string().hex()
    kunci_publik_hex = vk.to_string().hex()

    return kunci_privat_hex, kunci_publik_hex


def tanda_tangani_deterministik(
    tx: dict,
    kunci_privat_hex: str
) -> str:
    """
    Menandatangani transaksi secara deterministik menggunakan RFC 6979.
    """

    sk = SigningKey.from_string(
        bytes.fromhex(kunci_privat_hex),
        curve=SECP256k1
    )

    pesan = L7.pesan_transaksi(tx)

    tanda_tangan = sk.sign_deterministic(pesan)

    return tanda_tangan.hex()


# ============================================================== MODIFIKASI 8
class NodePersonal(L8.Node):
    """
    Node personal yang menambahkan identitas mahasiswa
    pada transaksi pertama setiap blok hasil mining.
    """

    def __init__(
        self,
        nama: str,
        nim4: str,
        difficulty: int = 2
    ):
        super().__init__(nama, difficulty)

        self.nim4 = nim4

    def tambang_blok(self, transactions) -> dict:
        """
        Menambang blok dengan penanda identitas mahasiswa
        pada posisi transaksi pertama.
        """

        penanda = f"{self.nama}#{self.nim4}"

        daftar_transaksi = [penanda] + list(transactions)

        return super().tambang_blok(daftar_transaksi)


def semua_sepakat(nodes: list) -> bool:
    """
    Memeriksa apakah semua node memiliki rantai yang sama persis.
    """

    if not nodes:
        return False

    rantai_awal = nodes[0].chain

    return all(
        node.chain == rantai_awal
        for node in nodes[1:]
    )


# ============================================================== MODIFIKASI 9
class BlockchainHalving(L9.Blockchain):
    """
    Blockchain Level 9 dengan hadiah mining yang berkurang separuh
    setiap interval blok tertentu.
    """

    def __init__(
        self,
        hadiah_awal: int,
        interval: int,
        difficulty: int = 2
    ):
        if interval <= 0:
            raise ValueError("Interval halving harus lebih dari 0")

        super().__init__(difficulty)

        self.hadiah_awal = hadiah_awal
        self.interval = interval

    def hadiah(self, index: int) -> int:
        """
        Menghitung hadiah mining berdasarkan nomor blok.

        Contoh:
        hadiah_awal = 40
        interval = 2

        Blok 1-2 = 40
        Blok 3-4 = 20
        Blok 5-6 = 10
        """

        jumlah_halving = (index - 1) // self.interval

        return self.hadiah_awal // (2 ** jumlah_halving)

    def mine(self, alamat_penambang: str) -> dict:
        """
        Menambang blok baru dengan hadiah sesuai aturan halving.
        """

        # Nomor blok baru
        index = self.chain[-1]["index"] + 1

        # Buat transaksi hadiah mining
        coinbase = {
            "sender": L9.SISTEM,
            "recipient": alamat_penambang,
            "amount": self.hadiah(index)
        }

        # Gabungkan hadiah dengan transaksi yang menunggu
        transactions = (
            [coinbase] + self.pending_transactions.copy()
        )

        # Ambil blok terakhir
        blok_terakhir = self.chain[-1]

        # Buat blok baru
        block = {
            "index": index,
            "transactions": transactions,
            "previous_hash": self.hash_block(blok_terakhir),
            "nonce": 0
        }

        # Lakukan Proof of Work
        self._tambang(block)

        # Masukkan blok ke blockchain
        self.chain.append(block)

        # Kosongkan transaksi yang sudah masuk blok
        self.pending_transactions = []

        return block

    def validasi_ekonomi(self) -> bool:
        """
        Memvalidasi seluruh transaksi ekonomi blockchain,
        termasuk hadiah mining yang mengikuti aturan halving.
        """

        saldo = {}

        # Genesis tidak memiliki transaksi ekonomi
        for block in self.chain[1:]:

            transactions = block["transactions"]

            # Setiap blok harus memiliki transaksi
            if not transactions:
                return False

            # Transaksi pertama harus berupa coinbase
            coinbase = transactions[0]

            if coinbase["sender"] != L9.SISTEM:
                return False

            # Hadiah harus sesuai aturan halving
            hadiah_seharusnya = self.hadiah(block["index"])

            if coinbase["amount"] != hadiah_seharusnya:
                return False

            # Tidak boleh ada transaksi sistem selain coinbase
            for tx in transactions[1:]:
                if tx["sender"] == L9.SISTEM:
                    return False

            # Periksa seluruh transaksi
            for tx in transactions:

                sender = tx["sender"]
                recipient = tx["recipient"]
                amount = tx["amount"]

                # Jumlah transaksi harus positif
                if amount <= 0:
                    return False

                # Coinbase menciptakan koin baru
                if sender == L9.SISTEM:

                    saldo[recipient] = (
                        saldo.get(recipient, 0) + amount
                    )

                else:

                    # Pengirim harus memiliki saldo cukup
                    if saldo.get(sender, 0) < amount:
                        return False

                    # Kurangi saldo pengirim
                    saldo[sender] = (
                        saldo.get(sender, 0) - amount
                    )

                    # Tambahkan saldo penerima
                    saldo[recipient] = (
                        saldo.get(recipient, 0) + amount
                    )

        return True
