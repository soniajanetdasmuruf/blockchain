
import hashlib
import json

from ecdsa import BadSignatureError, SECP256k1, SigningKey, VerifyingKey


def buat_pasangan_kunci():
    """Membuat kunci privat dan kunci publik SECP256k1."""

    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()

    kunci_privat_hex = sk.to_string().hex()
    kunci_publik_hex = vk.to_string().hex()

    return kunci_privat_hex, kunci_publik_hex


def alamat_dari_kunci_publik(kunci_publik_hex: str) -> str:
    """Membuat alamat dari kunci publik."""

    kunci_publik_bytes = bytes.fromhex(kunci_publik_hex)

    hasil_hash = hashlib.sha256(kunci_publik_bytes).hexdigest()

    return hasil_hash[:40]


def pesan_transaksi(tx: dict) -> bytes:
    """Mengubah data transaksi menjadi bytes kanonik."""

    data = {
        "sender": tx["sender"],
        "recipient": tx["recipient"],
        "amount": tx["amount"]
    }

    pesan = json.dumps(data, sort_keys=True)

    return pesan.encode("utf-8")


def tanda_tangani(tx: dict, kunci_privat_hex: str) -> str:
    """Menandatangani transaksi menggunakan kunci privat."""

    sk = SigningKey.from_string(
        bytes.fromhex(kunci_privat_hex),
        curve=SECP256k1
    )

    pesan = pesan_transaksi(tx)

    tanda_tangan = sk.sign(pesan)

    return tanda_tangan.hex()


def verifikasi(tx: dict, tanda_tangan_hex: str, kunci_publik_hex: str) -> bool:
    """Memverifikasi tanda tangan digital."""

    try:
        vk = VerifyingKey.from_string(
            bytes.fromhex(kunci_publik_hex),
            curve=SECP256k1
        )

        sig_bytes = bytes.fromhex(tanda_tangan_hex)

        pesan = pesan_transaksi(tx)

        return vk.verify(sig_bytes, pesan)

    except (BadSignatureError, ValueError, TypeError, KeyError):
        return False


def transaksi_sah(tx: dict, tanda_tangan_hex: str, kunci_publik_hex: str) -> bool:
    """Memastikan tanda tangan valid dan alamat pengirim cocok."""

    try:
        alamat = alamat_dari_kunci_publik(kunci_publik_hex)

        if tx["sender"] != alamat:
            return False

        return verifikasi(tx, tanda_tangan_hex, kunci_publik_hex)

    except (ValueError, TypeError, KeyError):
        return False


if __name__ == "__main__":
    priv, pub = buat_pasangan_kunci()

    alamat = alamat_dari_kunci_publik(pub)

    tx = {
        "sender": alamat,
        "recipient": "alamat_budi",
        "amount": 5
    }

    sig = tanda_tangani(tx, priv)

    print("Alamat Ani :", alamat)
    print("Tanda tangan:", sig[:32], "...")

    print("Sah?", transaksi_sah(tx, sig, pub))

    tx["amount"] = 500

    print(
        "Setelah amount diubah jadi 500, sah?",
        transaksi_sah(tx, sig, pub)
    )
