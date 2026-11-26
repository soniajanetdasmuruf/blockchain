# Jawaban Refleksi --- Latihan Blockchain

**Nama:** Sonia Janetd Asmuruf\
**NIM:** 202155202026\
**Kelas:** \_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_

---

## Level 1 --- Fungsi Hash

1.  Hash disebut **sidik jari digital** karena setiap data akan
    menghasilkan nilai hash yang menjadi identitas digital data
    tersebut. Jika isi data berubah sedikit saja, nilai hash yang
    dihasilkan biasanya berubah besar. Tiga sifat fungsi hash
    kriptografis adalah:
    - **Deterministik:** masukan yang sama selalu menghasilkan hash
      yang sama.
    - **Satu arah (one-way):** sangat sulit mendapatkan kembali data
      asli hanya dari nilai hash.
    - **Tahan terhadap collision:** sangat sulit menemukan dua data
      berbeda yang menghasilkan hash yang sama.

2.  Pada percobaan yang saya jalankan, teks `Teknologi Blockchain` dibandingkan dengan `teknologi Blockchain`. Perubahan satu huruf dari huruf besar menjadi huruf kecil menghasilkan **48,8% bit berbeda**. Ini menunjukkan efek avalanche, yaitu perubahan kecil pada masukan dapat mengubah banyak bit pada hash. Saya baru memiliki satu pasangan hasil percobaan; dua pasangan tambahan belum diuji.

    **Output Level 1:**

    ```text
    SHA256('Teknologi Blockchain') = 126cca3fa9f7c370dae78c3ee50a40c1b8604c9ae35a70075d74c18175de04b7
    SHA256('teknologi Blockchain') = bc6f093ad620096c8743bda24afb52ffaa23ee3fce01eec545b9f7852b2b5c03
    Bit berbeda: 48.8%  (efek avalanche)
    ```

3.  Jika `hash_dict` tidak menggunakan `sort_keys=True`, urutan pasangan
    key dan value dalam dictionary dapat memengaruhi teks JSON yang
    di-hash. Dua dictionary dengan isi yang sama tetapi urutan key
    berbeda bisa menghasilkan hash berbeda. Hal ini berbahaya untuk
    blockchain karena data yang sebenarnya sama dapat dianggap berbeda
    dan perhitungan hash antarblok menjadi tidak konsisten.

## Level 2 --- Blockchain Dasar

1.  `previous_hash` pada blok genesis berisi `"0"` karena blok genesis
    merupakan blok pertama dan belum memiliki blok sebelumnya. Nilai
    tersebut menjadi penanda awal rantai agar format blok tetap memiliki
    acuan `previous_hash`.

2.  Saat difficulty dinaikkan, proses proof of work menjadi lebih sulit
    karena hash harus memiliki lebih banyak angka nol di bagian awal.
    Akibatnya, program perlu mencoba lebih banyak nilai proof dan waktu
    mining cenderung lebih lama.

Pada output yang saya kirim, program menampilkan proof berikut. Percobaan ini tidak mencatat pengujian terpisah pada difficulty 3, 4, dan 5, sehingga nilai-nilai tersebut tidak saya isi dengan perkiraan.

| Blok | Proof |
| ---- | ----: |
| #2   |   533 |
| #3   | 45293 |
| #4   | 21391 |
| #5   |  8018 |

**Output Level 2:**

```text
Blok #2 ditambang, proof=533
Blok #3 ditambang, proof=45293
Blok #4 ditambang, proof=21391
Blok #5 ditambang, proof=8018
```

Untuk menjawab perbandingan difficulty 3, 4, dan 5 secara tepat, demo masih perlu dijalankan masing-masing pada ketiga nilai difficulty tersebut dan waktu mining-nya dicatat.

## Level 3 --- Tampering

1.  Jika data pada blok posisi _k_ diubah, hash blok tersebut ikut
    berubah. Blok setelahnya, yaitu posisi _k+1_, masih menyimpan
    `previous_hash` yang mengacu pada hash lama blok _k_. Karena itu,
    tautan yang pertama kali tidak cocok ditemukan pada blok _k+1_.

2.  Perubahan pada blok terakhir tidak terdeteksi oleh
    `cari_tautan_putus` karena tidak ada blok berikutnya yang menyimpan
    `previous_hash` untuk dibandingkan dengan hash blok terakhir. Untuk
    mengetahui perubahan pada blok terakhir, hash blok itu sendiri perlu
    dibandingkan dengan hash yang tersimpan atau divalidasi melalui
    mekanisme lain.

3.  Kelemahan desain PoW pada contoh Level 3 adalah proof hanya
    bergantung pada nilai proof sebelumnya dan proof saat ini, bukan
    pada seluruh isi data blok. Akibatnya, data blok dapat diubah lalu
    tautan `previous_hash` disambungkan ulang tanpa harus melakukan
    proses mining yang benar-benar mengamankan isi blok. Ini membuat
    rantai palsu dapat terlihat valid.

    **Output Level 3:**

```text
Asli valid?            True
Setelah diubah valid?  False
Tautan putus di indeks 2
Setelah disambung ulang valid? True <-- masalah!
```

## Level 4 --- Transaksi

1.  Transaksi tidak langsung masuk ke blok karena transaksi biasanya
    dikumpulkan terlebih dahulu di `pending_transactions`. Dengan cara
    ini, beberapa transaksi dapat dimasukkan bersama-sama ketika
    penambang membuat blok baru. Pending juga menjadi tempat menampung
    transaksi yang belum dikonfirmasi.

2.  `create_block` menggunakan `list(self.pending_transactions)` agar
    blok menyimpan salinan daftar transaksi, bukan merujuk ke daftar
    pending yang sama. Jika tidak disalin, ketika daftar pending
    dikosongkan atau diubah setelah blok dibuat, daftar transaksi di
    blok juga dapat ikut berubah. Akibatnya, riwayat transaksi dalam
    blok menjadi tidak aman atau tidak sesuai dengan keadaan saat blok
    dibuat.

    **Output Level 4:**

```text
Riwayat Budi: [(2, {'sender': 'Ani', 'recipient': 'Budi', 'amount': 5}), (2, {'sender': 'Budi', 'recipient': 'Citra', 'amount': 2})]
```

## Level 5 --- PoW dengan Nonce

1.  Pada Level 3, perubahan data dapat disambungkan ulang karena proof
    of work belum mengikat seluruh isi blok. Pada Level 5, hash dihitung
    dari isi blok, termasuk data transaksi dan nonce. Jika isi blok
    diubah, hash berubah dan penyerang harus mencari nonce baru yang
    memenuhi difficulty. Blok berikutnya juga harus diperbarui karena
    `previous_hash`-nya berubah. Oleh sebab itu, serangan sambung ulang
    menjadi jauh lebih sulit.

2.  Jumlah percobaan untuk memalsukan blok #1 pada demo harus diambil
    dari output percobaan karena bergantung pada nonce yang ditemukan
    saat mining ulang.

    **Hasil percobaan:** program melaporkan penyerang menambang ulang dengan **151.522 percobaan hash**. Setelah mining ulang, rantai kembali dinyatakan valid. Angka ini adalah hasil percobaan pada program yang dijalankan, bukan jaminan jumlah yang selalu sama.

    Jika difficulty 6, rata-rata peluang menemukan hash yang memenuhi
    syarat adalah sekitar 1 banding `16^6`, atau 16.777.216 percobaan
    untuk satu blok. Jika penyerang harus menambang ulang sekitar 1.000
    blok, perkiraan kasarnya adalah:

    `1.000 × 16.777.216 = 16.777.216.000 percobaan hash`

    Angka tersebut adalah nilai harapan/perkiraan, bukan jumlah pasti.
    Waktu sebenarnya juga bergantung pada kecepatan perangkat keras.

    **Output Level 5:**

```text
Blok #1 nonce=69781 hash=0000d2e44aef58fe...
Blok #2 nonce=105686 hash=00003eb3a7e8da63...
Blok #3 nonce=358879 hash=0000110be3bccfe2...
Valid? True
Setelah diubah valid? False
Penyerang menambang ulang dengan 151522 percobaan hash. Valid? True
```

## Level 6 --- Difficulty

1.  Berikut tabel hasil eksperimen yang benar-benar muncul pada terminal saya. Hasil aktual dibandingkan dengan perkiraan teoritis `16^d`.

| Difficulty | Rata-rata percobaan aktual | Teori `16^d` | Rata-rata detik |
| ---------: | -------------------------: | -----------: | --------------: |
|          1 |                         25 |           16 |          0.0001 |
|          2 |                        231 |          256 |          0.0010 |
|          3 |                      6.983 |        4.096 |          0.0208 |
|          4 |                     64.827 |       65.536 |          0.4707 |
|          5 |                  1.396.848 |    1.048.576 |          4.0006 |

Hasil eksperimen tidak harus sama persis dengan `16^d` karena jumlah percobaan bersifat acak. Namun, nilainya secara umum berada di sekitar nilai harapan. Angka 16 digunakan karena hash ditulis dalam heksadesimal yang memiliki 16 kemungkinan karakter, yaitu 0 sampai 9 dan a sampai f. Peluang satu karakter awal menjadi `0` adalah 1/16. Untuk `d` karakter nol berturut-turut, peluangnya menjadi `1/16^d`.

**Output Level 6:**

```text
Diff |  Rata percobaan |  Teori 16^d | Rata detik
----------------------------------------------------
   1 |              25 |          16 |     0.0001
   2 |             231 |         256 |     0.0010
   3 |            6983 |        4096 |     0.0208
   4 |           64827 |       65536 |     0.4707
   5 |         1396848 |     1048576 |     4.0006
Grafik disimpan: grafik_difficulty.png
```

2.  Waktu blok perlu dijaga stabil agar transaksi dapat dikonfirmasi
    dengan jeda yang relatif dapat diperkirakan. Jika blok terlalu
    cepat, jaringan dan ukuran blockchain dapat berkembang terlalu
    cepat. Jika terlalu lambat, transaksi menunggu lebih lama.
    Penyesuaian difficulty membantu menjaga keseimbangan waktu
    konfirmasi dan keamanan jaringan.

## Level 7 --- Tanda Tangan Digital

1.  **Kunci privat** digunakan pemilik untuk menandatangani transaksi
    dan harus dirahasiakan. **Kunci publik** digunakan orang lain untuk
    memeriksa apakah tanda tangan tersebut benar. **Alamat** merupakan
    identitas yang diturunkan dari kunci publik dan digunakan sebagai
    tujuan atau asal transaksi dalam sistem.

2.  Tanda tangan penipu dapat valid karena tanda tangan itu memang
    dibuat menggunakan kunci privat milik penipu sendiri. Namun,
    transaksi atas nama korban tidak sah karena alamat pengirim tidak
    cocok dengan alamat yang diturunkan dari kunci publik yang
    disertakan. Jadi, tanda tangan yang valid tidak otomatis membuktikan
    bahwa penanda tangan adalah pemilik alamat korban.

3.  Jika kunci privat hilang, pemilik biasanya tidak dapat lagi
    menandatangani transaksi untuk menggunakan aset yang dikendalikan
    oleh kunci tersebut. Jika kunci privat dicuri, pencuri dapat membuat
    tanda tangan yang valid dan memindahkan aset atas nama pemilik.
    Karena itu, kunci privat harus disimpan dengan aman dan tidak
    dibagikan.

    **Output Level 7:**

```text
Alamat Ani : fde25646c3db0efb8a0a512e6d7ea022e4931e81
Tanda tangan: 5b817432520218ad0f5c1e69e544cebe ...
Sah? True
Setelah amount diubah jadi 500, sah? False
```

## Level 8 --- Jaringan & Konsensus

1.  Kondisi fork berarti beberapa node memiliki rantai dengan panjang
    atau isi berbeda. Contoh sederhana:

    ```text
    Kondisi fork:
    Node A: Genesis ── Blok A1
    Node B: Genesis ── Blok A1 ── Blok B2
    Node C: Genesis ── Blok A1 ── Blok B2 ── Blok B3

    Setelah resolve_conflicts:
    Node A: Genesis ── Blok A1 ── Blok B2 ── Blok B3
    Node B: Genesis ── Blok A1 ── Blok B2 ── Blok B3
    Node C: Genesis ── Blok A1 ── Blok B2 ── Blok B3
    ```

    Node memilih rantai valid yang lebih panjang. Karena itu, setelah
    `resolve_conflicts`, node-node pada contoh akhirnya menggunakan
    rantai yang sama.

2.  Transaksi `fork-B` yang hanya berada pada cabang yang kalah tidak
    otomatis menjadi bagian dari rantai utama. Transaksi tersebut dapat
    perlu dimasukkan kembali ke mempool dan ditambang pada blok
    berikutnya jika masih valid. Anjuran menunggu 6 konfirmasi di
    Bitcoin bertujuan mengurangi risiko transaksi dibatalkan akibat
    reorganisasi rantai. Semakin banyak blok yang dibangun setelah blok
    transaksi, semakin sulit membatalkan transaksi tersebut, walaupun
    risikonya tidak benar-benar nol.

3.  **Catatan praktik:** bagian ini harus dilengkapi dengan output asli
    setelah menjalankan tiga server. Contoh alur pengujian:

    ```powershell
    # Terminal 1
    python latihan/level08_server.py 5001

    # Terminal 2
    python latihan/level08_server.py 5002

    # Terminal 3
    python latihan/level08_server.py 5003

    # Terminal 4: daftarkan node 5002 dan 5003 sebagai peer node 5001
    Invoke-RestMethod -Method Post `
      -Uri http://localhost:5001/nodes `
      -ContentType "application/json" `
      -Body '{"nodes":["http://localhost:5002","http://localhost:5003"]}'

    # Tambang dua blok pada node 5002
    Invoke-RestMethod http://localhost:5002/mine_block
    Invoke-RestMethod http://localhost:5002/mine_block

    # Periksa rantai node 5001 sebelum sinkronisasi
    Invoke-RestMethod http://localhost:5001/get_chain

    # Sinkronisasi node 5001 dengan rantai valid terpanjang
    Invoke-RestMethod http://localhost:5001/resolve

    # Periksa rantai dan validitas setelah sinkronisasi
    Invoke-RestMethod http://localhost:5001/get_chain
    Invoke-RestMethod http://localhost:5001/valid
    ```

    Pada skenario ini, sebelum sinkronisasi node 5001 diharapkan masih
    memiliki 1 blok (genesis), sedangkan node 5002 memiliki 3 blok
    setelah menambang dua blok. Setelah `/resolve`, node 5001 diharapkan
    memiliki 3 blok dan `/valid` menyatakan blockchain valid.
    **Tempelkan output asli dari terminal Anda di sini:** \[isi hasil
    praktik\].

    **Output praktik jaringan Level 8 (`level08_jaringan.py`):**

```text
Panjang setelah A menambang & menyiarkan: [2, 2, 2]
Saat fork: [2, 3, 4]
Setelah resolve_conflicts: [4, 4, 4] | semua sama? True
```

**Praktik server HTTP (`level08_server.py`):** belum saya jalankan karena belum memahami langkah menjalankan tiga server. Jadi, saya tidak mencantumkan output seolah-olah sudah diuji. Pengujian ini masih perlu dilakukan dengan menjalankan server pada port 5001, 5002, dan 5003, kemudian mencoba endpoint `/mine_block`, `/get_chain`, `/resolve`, dan `/valid`.

## Level 9 --- Reward & Saldo

1.  Koin pertama berasal dari transaksi coinbase yang dibuat oleh sistem
    ketika sebuah blok berhasil ditambang. Pada latihan ini, setiap
    penambangan memberikan `MINING_REWARD` sebesar 10 coin kepada alamat
    penambang. Jadi, meskipun semua pengguna memulai dengan saldo 0,
    koin baru dapat masuk melalui hadiah mining.

2.  `chain_valid` memeriksa integritas struktur rantai melalui hash dan
    hubungan antarblok. Namun, hash yang valid tidak menjamin aturan
    ekonomi dipatuhi. Seseorang masih bisa membuat transaksi dengan
    jumlah melebihi saldo atau membuat coinbase yang tidak sesuai
    aturan, lalu menghitung hash yang benar. `validasi_ekonomi`
    diperlukan untuk memeriksa aturan hadiah mining, mencegah coinbase
    tambahan, dan memastikan saldo tidak pernah negatif ketika transaksi
    diputar ulang.

3.  Bitcoin menggunakan model **UTXO (Unspent Transaction Output)**.
    Pada model saldo akun dalam latihan ini, saldo dihitung dengan
    menjumlahkan semua penerimaan lalu mengurangi semua pengiriman. Pada
    model UTXO, koin disimpan sebagai keluaran transaksi yang belum
    digunakan. Saat membayar, transaksi menggunakan satu atau beberapa
    UTXO sebagai input dan menghasilkan UTXO baru untuk penerima serta,
    jika ada, uang kembalian. Jadi, Bitcoin tidak menyimpan saldo akun
    secara langsung seperti contoh latihan ini.

**Output Level 9:**

```text
Saldo ani: 6
Saldo budi: 4
Saldo citra: 10
Total suplai: 20
Ditolak: Saldo tidak mencukupi
Validasi ekonomi: True
```
