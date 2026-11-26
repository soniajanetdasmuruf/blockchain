
import hashlib
import time


def tambang(data: str, difficulty: int):
    """Mencari nonce hingga hash memenuhi difficulty."""

    nonce = 0
    jumlah_percobaan = 0

    while True:
        teks = f"{data}{nonce}"

        hasil_hash = hashlib.sha256(
            teks.encode("utf-8")
        ).hexdigest()

        jumlah_percobaan += 1

        if hasil_hash.startswith("0" * difficulty):
            return nonce, hasil_hash, jumlah_percobaan

        nonce += 1


def ekspektasi_percobaan(difficulty: int) -> int:
    """Menghitung rata-rata teoretis percobaan mining."""

    return 16 ** difficulty


def ukur_mining(difficulty: int, n: int = 5) -> dict:
    """Mengukur rata-rata percobaan dan waktu mining."""

    total_percobaan = 0

    waktu_mulai = time.perf_counter()

    for i in range(n):
        data = f"blok-{i}"

        nonce, hash_hex, percobaan = tambang(
            data,
            difficulty
        )

        total_percobaan += percobaan

    waktu_selesai = time.perf_counter()

    rata_percobaan = total_percobaan / n
    rata_detik = (waktu_selesai - waktu_mulai) / n

    return {
        "difficulty": difficulty,
        "rata_percobaan": rata_percobaan,
        "rata_detik": rata_detik
    }


def sesuaikan_difficulty(
    sekarang: int,
    waktu_aktual: float,
    waktu_target: float
) -> int:
    """Menyesuaikan difficulty berdasarkan waktu mining."""

    if waktu_aktual < waktu_target / 2:
        return sekarang + 1

    elif waktu_aktual > waktu_target * 2:
        return max(1, sekarang - 1)

    else:
        return sekarang


def eksperimen(daftar_difficulty=(1, 2, 3, 4), n: int = 5) -> list:
    """Melakukan eksperimen pada beberapa tingkat difficulty."""

    return [
        ukur_mining(d, n)
        for d in daftar_difficulty
    ]


if __name__ == "__main__":
    hasil = eksperimen((1, 2, 3, 4, 5), n=5)

    print(
        f"{'Diff':>4} | {'Rata percobaan':>15} | "
        f"{'Teori 16^d':>11} | {'Rata detik':>10}"
    )

    print("-" * 52)

    for h in hasil:
        print(
            f"{h['difficulty']:>4} | "
            f"{h['rata_percobaan']:>15.0f} | "
            f"{ekspektasi_percobaan(h['difficulty']):>11} | "
            f"{h['rata_detik']:>10.4f}"
        )

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        xs = [h["difficulty"] for h in hasil]

        plt.semilogy(
            xs,
            [h["rata_detik"] for h in hasil],
            "o-"
        )

        plt.xlabel("Difficulty (jumlah angka nol)")
        plt.ylabel("Rata-rata waktu mining (detik, skala log)")
        plt.title("Pengaruh difficulty terhadap waktu mining")
        plt.grid(True, which="both", alpha=0.3)

        plt.savefig(
            "grafik_difficulty.png",
            dpi=120,
            bbox_inches="tight"
        )

        print("Grafik disimpan: grafik_difficulty.png")

    except ImportError:
        print("(matplotlib belum terpasang — lewati grafik)")
