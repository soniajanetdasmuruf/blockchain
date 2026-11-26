
import hashlib
import json

def sha256_hex(teks: str) -> str:
    """Menghasilkan hash SHA-256 dalam bentuk heksadesimal."""
    hasil = hashlib.sha256(teks.encode('utf-8')).hexdigest()
    return hasil

def hash_dict(data: dict) -> str:
    """Hash sebuah dict secara kanonik."""
    teks_json = json.dumps(data, sort_keys=True)
    return sha256_hex(teks_json)

def bit_berbeda(hash_a: str, hash_b: str) -> int:
    """Menghitung jumlah bit yang berbeda antara dua hash."""
    angka_a = int(hash_a, 16)
    angka_b = int(hash_b, 16)

    hasil_xor = angka_a ^ angka_b
    return bin(hasil_xor).count('1')

def persen_bit_berbeda(teks_a: str, teks_b: str) -> float:
    """Menghitung persentase bit yang berbeda."""
    hash_a = sha256_hex(teks_a)
    hash_b = sha256_hex(teks_b)

    jumlah = bit_berbeda(hash_a, hash_b)
    return (jumlah / 256) * 100

if __name__ == "__main__":
    a, b = "Teknologi Blockchain", "teknologi Blockchain"

    print(f"SHA256('{a}') = {sha256_hex(a)}")
    print(f"SHA256('{b}') = {sha256_hex(b)}")
    print(f"Bit berbeda: {persen_bit_berbeda(a, b):.1f}%  (efek avalanche)")