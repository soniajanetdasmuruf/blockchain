
"""
Skrip pengecek otomatis latihan Blockchain.

Pemakaian:
    python cek_nilai.py
    python cek_nilai.py 3
    python cek_nilai.py 1 2 5
    python cek_nilai.py --kunci
"""

import contextlib
import io
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
TESTS = os.path.join(ROOT, "tests")

JUDUL = {
    1: "Fungsi hash SHA-256",
    2: "Blockchain dasar (GfG)",
    3: "Eksperimen tampering",
    4: "Transaksi dalam blok",
    5: "PoW dengan nonce",
    6: "Eksperimen difficulty",
    7: "Tanda tangan digital",
    8: "Jaringan & konsensus",
    9: "Reward & saldo",
}


class Pencatat:
    """Plugin pytest untuk menghitung tes lulus dan gagal."""

    def __init__(self):
        self.lulus = 0
        self.total = 0

    def pytest_runtest_logreport(self, report):
        # Hasil utama setiap pengujian
        if report.when == "call":
            self.total += 1
            if report.passed:
                self.lulus += 1

        # Jika pengujian gagal saat persiapan
        elif report.when == "setup" and report.failed:
            self.total += 1

    def pytest_collectreport(self, report):
        # Error ketika mengimpor atau mengumpulkan file tes
        if report.failed:
            self.total += 1


def file_tes(level):
    """Mencari file pengujian berdasarkan nomor level."""

    if not os.path.isdir(TESTS):
        return None

    awalan = f"test_level{level:02d}_"

    for nama in sorted(os.listdir(TESTS)):
        if nama.startswith(awalan) and nama.endswith(".py"):
            return os.path.join(TESTS, nama)

    return None


def jalankan_tes(path, detail):
    """Menjalankan pytest dan mengembalikan hasilnya."""

    import pytest

    pencatat = Pencatat()

    opsi = [
        "-q",
        "-p", "no:cacheprovider",
        "--rootdir", ROOT,
        "--tb=short" if detail else "--tb=no",
        "--no-header",
    ]

    mulai = time.time()

    with contextlib.redirect_stdout(io.StringIO()):
        exit_code = pytest.main(
            opsi + [path],
            plugins=[pencatat]
        )

    durasi = time.time() - mulai

    return (
        pencatat.lulus,
        pencatat.total,
        durasi,
        exit_code
    )


def main():
    argumen = sys.argv[1:]

    # Tentukan mode pengujian
    mode_kunci = "--kunci" in argumen

    if mode_kunci:
        argumen.remove("--kunci")
        os.environ["BC_KUNCI"] = "1"
    else:
        os.environ.pop("BC_KUNCI", None)

    # Validasi nomor level
    if argumen:
        try:
            levels = [int(a) for a in argumen]
        except ValueError:
            print("Error: nomor level harus berupa angka.")
            return

        if any(lv not in JUDUL for lv in levels):
            print("Error: level hanya tersedia dari 1 sampai 9.")
            return

        # Hilangkan nomor level yang duplikat
        levels = list(dict.fromkeys(levels))

    else:
        levels = list(JUDUL.keys())

    detail = len(levels) == 1

    folder = "kunci_jawaban" if mode_kunci else "latihan"

    print(f"\nMemeriksa kode di folder: {folder}/\n")

    if not os.path.isdir(TESTS):
        print(f"ERROR: Folder pengujian tidak ditemukan: {TESTS}")
        return

    hasil = []

    for lv in levels:
        path = file_tes(lv)

        if path is None:
            print(f"Level {lv}: file pengujian tidak ditemukan.")
            hasil.append((lv, 0, 0, 0))
            continue

        print(f"Memeriksa Level {lv}...")

        lulus, total, durasi, exit_code = jalankan_tes(
            path,
            detail
        )

        hasil.append((lv, lulus, total, durasi))

        if detail:
            if total == 0:
                print("Tidak ada tes yang berhasil dihitung.")
            elif lulus == total:
                print("Semua pengujian level ini lulus.")
            else:
                print(f"Hasil: {lulus}/{total} tes lulus.")

    # Tampilkan tabel hasil
    print("\n" + "=" * 62)
    print(f"{'Level':<6}{'Materi':<28}{'Lulus':>10}{'Status':>12}")
    print("-" * 62)

    total_lulus = 0
    total_tes = 0
    persentase_level = []

    for lv, lulus, total, durasi in hasil:

        if total == 0:
            status = "ERROR"
        elif lulus == total:
            status = "SELESAI"
        elif lulus == 0:
            status = "belum"
        else:
            status = "sebagian"

        print(
            f"{lv:<6}"
            f"{JUDUL[lv]:<28}"
            f"{f'{lulus}/{total}':>10}"
            f"{status:>12}"
        )

        total_lulus += lulus
        total_tes += total

        if total > 0:
            persentase_level.append(100 * lulus / total)

    print("-" * 62)

    if persentase_level:
        nilai = sum(persentase_level) / len(persentase_level)
    else:
        nilai = 0

    print(
        f"{'TOTAL':<34}"
        f"{f'{total_lulus}/{total_tes}':>10}"
        f"{f'{nilai:.0f}%':>12}"
    )

    print("=" * 62)

    if not detail:
        print(
            "\nTip: jalankan "
            "`python cek_nilai.py <nomor_level>` "
            "untuk melihat detail kegagalan.\n"
        )


if __name__ == "__main__":
    main()
