# ============================================================
# WaruMate v5 - Database Generator
# ============================================================
# Fungsi:
#   - Membuat ulang file database (warung.db)
#   - Menghapus tabel lama jika sudah ada
#   - Membuat tabel baru dengan struktur WaruMate v5
#   - Mengisi contoh data menu untuk pengujian awal
# ============================================================

import sqlite3
from pathlib import Path

# Lokasi file database
DB_PATH = Path("warung.db")

# Koneksi ke database (akan dibuat otomatis jika belum ada)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

print("🧩 Membuat ulang struktur database WaruMate v5 Refined...")
print("📦 Database:", DB_PATH.resolve())

# 1️⃣ Hapus tabel lama jika sudah ada
tables = ["detail_transaksi", "transaksi", "menu"]
for t in tables:
    c.execute(f"DROP TABLE IF EXISTS {t}")
print("🧹 Tabel lama dihapus (jika ada)")

# 2️⃣ Buat tabel baru dengan struktur terbaru
c.execute("""
CREATE TABLE menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga REAL NOT NULL,
    stok INTEGER NOT NULL,
    kategori TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tanggal TEXT NOT NULL,
    total REAL NOT NULL,
    metode TEXT NOT NULL
)
""")

c.execute("""
CREATE TABLE detail_transaksi (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_transaksi INTEGER NOT NULL,
    id_menu INTEGER NOT NULL,
    jumlah INTEGER NOT NULL,
    subtotal REAL NOT NULL,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id),
    FOREIGN KEY (id_menu) REFERENCES menu(id)
)
""")

print("✅ Struktur tabel baru berhasil dibuat!")

# 3️⃣ Isi contoh data awal (dummy data)
menus = [
    ("Nasi Goreng", 15000, 20, "Makanan"),
    ("Mie Goreng", 12000, 25, "Makanan"),
    ("Tempe Goreng", 3000, 40, "Lauk"),
    ("Sayur Asem", 4000, 30, "Sayur"),
    ("Es Teh Manis", 5000, 50, "Minuman"),
    ("Kopi Hitam", 8000, 35, "Minuman")
]

c.executemany("INSERT INTO menu (nama, harga, stok, kategori) VALUES (?, ?, ?, ?)", menus)
print(f"🍱 Data menu awal berhasil dimasukkan ({len(menus)} item).")

# 4️⃣ Simpan dan tutup koneksi
conn.commit()
conn.close()

print("\n🎉 Database WaruMate v5 Refined siap digunakan!")
print("   Struktur lengkap:")
print("   - menu (id, nama, harga, stok, kategori)")
print("   - transaksi (id, tanggal, total, metode)")
print("   - detail_transaksi (id, id_transaksi, id_menu, jumlah, subtotal)")
print("===========================================================")
