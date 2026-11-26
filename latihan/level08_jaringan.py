
"""
LEVEL 8 — Jaringan Banyak Node dan Konsensus "Rantai Terpanjang" (LATIHAN)
===============================================================================

Artikel GfG hanya punya satu node. Blockchain sesungguhnya terdiri dari
banyak node yang saling bertukar blok. Di sini jaringan disimulasikan di dalam
satu proses Python (objek Node saling memanggil), agar mudah dites.
Versi HTTP sungguhan dengan Flask ada di level08_server.py (demo).

Tujuan belajar:
  * Peer, siaran (broadcast) blok, dan validasi blok yang diterima.
  * Aturan konsensus: rantai VALID terpanjang yang menang.
  * Fork dan cara jaringan kembali sepakat.

Jalankan tes:  python cek_nilai.py 8
"""

import copy
import hashlib
import json

GENESIS_HASH_PREV = "0" * 64


class Node:
    # ====================== SUDAH DISEDIAKAN ======================

    def __init__(self, nama: str, difficulty: int = 2):
        self.nama = nama
        self.difficulty = difficulty
        self.peers = []

        # Genesis dibuat deterministik agar semua node memiliki genesis sama
        genesis = {
            "index": 0,
            "transactions": [],
            "previous_hash": GENESIS_HASH_PREV,
            "nonce": 0,
            "miner": "genesis"
        }

        self._tambang(genesis)
        self.chain = [genesis]

    @staticmethod
    def hash_block(block):
        isi = {
            k: v
            for k, v in block.items()
            if k != "hash"
        }

        return hashlib.sha256(
            json.dumps(isi, sort_keys=True).encode()
        ).hexdigest()

    def _tambang(self, block):
        block["nonce"] = 0

        while not self.hash_block(block).startswith(
            "0" * self.difficulty
        ):
            block["nonce"] += 1

        block["hash"] = self.hash_block(block)

        return block

    def blok_valid(self, block, blok_sebelumnya) -> bool:
        """Cek satu blok terhadap blok sebelumnya."""

        return (
            block.get("hash") == self.hash_block(block)
            and block["hash"].startswith("0" * self.difficulty)
            and block["previous_hash"] == blok_sebelumnya["hash"]
            and block["index"] == blok_sebelumnya["index"] + 1
        )

    def rantai_valid(self, chain) -> bool:
        """Memeriksa apakah seluruh rantai valid."""

        if not chain or chain[0] != self.chain[0]:
            return False

        return all(
            self.blok_valid(chain[i], chain[i - 1])
            for i in range(1, len(chain))
        )

    def tambang_blok(self, transactions) -> dict:
        """Tambang blok baru di atas rantai sendiri tanpa menyiarkan."""

        last = self.chain[-1]

        block = {
            "index": last["index"] + 1,
            "transactions": transactions,
            "previous_hash": last["hash"],
            "nonce": 0,
            "miner": self.nama
        }

        self._tambang(block)
        self.chain.append(block)

        return block

    def tambang_dan_siarkan(self, transactions) -> dict:
        """Tambang blok baru lalu siarkan kepada semua peer."""

        block = self.tambang_blok(transactions)
        self.siarkan_blok(block)

        return block

    # ============ BAGIAN YANG DIKERJAKAN (TODO) ============

    def hubungkan(self, node_lain: "Node") -> None:
        """Menghubungkan dua node secara dua arah."""

        if node_lain is self:
            return

        if node_lain not in self.peers:
            self.peers.append(node_lain)

        if self not in node_lain.peers:
            node_lain.peers.append(self)

    def terima_blok(self, block: dict) -> bool:
        """Menerima blok jika valid sebagai kelanjutan rantai."""

        if self.blok_valid(block, self.chain[-1]):
            self.chain.append(copy.deepcopy(block))
            return True

        return False

    def siarkan_blok(self, block: dict) -> int:
        """Menyiarkan blok kepada seluruh peer."""

        jumlah_diterima = 0

        for peer in self.peers:
            if peer.terima_blok(block):
                jumlah_diterima += 1

        return jumlah_diterima

    def resolve_conflicts(self) -> bool:
        """Memilih rantai valid terpanjang dari seluruh peer."""

        rantai_terbaik = self.chain

        for peer in self.peers:
            if (
                self.rantai_valid(peer.chain)
                and len(peer.chain) > len(rantai_terbaik)
            ):
                rantai_terbaik = peer.chain

        if len(rantai_terbaik) > len(self.chain):
            self.chain = copy.deepcopy(rantai_terbaik)
            return True

        return False


# ====================== SIMULASI JARINGAN ======================

if __name__ == "__main__":

    a, b, c = Node("A"), Node("B"), Node("C")

    # Menghubungkan ketiga node
    a.hubungkan(b)
    b.hubungkan(c)
    a.hubungkan(c)

    # Node A menambang dan menyiarkan blok
    a.tambang_dan_siarkan(["tx1"])

    print(
        "Panjang setelah A menambang & menyiarkan:",
        [len(n.chain) for n in (a, b, c)]
    )

    # Fork: B dan C menambang tanpa menyiarkan
    b.tambang_blok(["tx-B"])

    c.tambang_blok(["tx-C1"])
    c.tambang_blok(["tx-C2"])

    print(
        "Saat fork:",
        [len(n.chain) for n in (a, b, c)]
    )

    # Setiap node menyelesaikan konflik
    for n in (a, b, c):
        n.resolve_conflicts()

    print(
        "Setelah resolve_conflicts:",
        [len(n.chain) for n in (a, b, c)],
        "| semua sama?",
        a.chain == b.chain == c.chain
    )
