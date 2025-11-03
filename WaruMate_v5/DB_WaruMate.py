# DB_WaruMate_v5.py
# Database handler lengkap untuk WaruMate v5
# - SQLite (warung.db)
# - CRUD menu
# - Simpan transaksi & detail_transaksi (dengan stok check)
# - Laporan harian, per kategori, metode pembayaran, menu terlaris
# =================================================================

import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="warung.db"):
        """Inisialisasi koneksi database"""
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    # ============================================================
    # 1️⃣  Buat Struktur Tabel (Otomatis)
    # ============================================================
    def create_tables(self):
        c = self.conn.cursor()

        # Tabel menu
        c.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            harga REAL NOT NULL,
            stok INTEGER NOT NULL,
            kategori TEXT NOT NULL
        )
        """)

        # Tabel transaksi
        c.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            total REAL NOT NULL,
            metode TEXT NOT NULL
        )
        """)

        # Tabel detail transaksi
        c.execute("""
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_transaksi INTEGER NOT NULL,
            id_menu INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (id_transaksi) REFERENCES transaksi(id),
            FOREIGN KEY (id_menu) REFERENCES menu(id)
        )
        """)
        self.conn.commit()

    # ============================================================
    # 2️⃣  CRUD MENU
    # ============================================================
    def tambah_menu(self, nama, harga, stok, kategori):
        """Tambah data menu baru"""
        c = self.conn.cursor()
        c.execute("INSERT INTO menu (nama, harga, stok, kategori) VALUES (?, ?, ?, ?)",
                  (nama, harga, stok, kategori))
        self.conn.commit()

    def ambil_semua_menu(self):
        """Ambil seluruh daftar menu"""
        cur = self.conn.cursor()
        cur.execute("SELECT id, nama, harga, stok, kategori FROM menu ORDER BY id")
        return cur.fetchall()

    def hapus_menu(self, id_menu):
        """Hapus menu berdasarkan ID"""
        c = self.conn.cursor()
        c.execute("DELETE FROM menu WHERE id = ?", (id_menu,))
        self.conn.commit()

    def kurangi_stok(self, id_menu, jumlah):
        """Kurangi stok setelah transaksi"""
        c = self.conn.cursor()
        c.execute("UPDATE menu SET stok = stok - ? WHERE id = ?", (jumlah, id_menu))
        self.conn.commit()

    # ============================================================
    # 3️⃣  TRANSAKSI PENJUALAN
    # ============================================================
    def simpan_transaksi(self, tanggal, total, metode):
        """Simpan data transaksi"""
        c = self.conn.cursor()
        c.execute("INSERT INTO transaksi (tanggal, total, metode) VALUES (?, ?, ?)",
                  (tanggal, total, metode))
        self.conn.commit()
        return c.lastrowid  # Kembalikan ID transaksi terakhir

    def simpan_detail_transaksi(self, id_transaksi, id_menu, jumlah, subtotal):
        """Simpan detail transaksi"""
        c = self.conn.cursor()
        c.execute("""
        INSERT INTO detail_transaksi (id_transaksi, id_menu, jumlah, subtotal)
        VALUES (?, ?, ?, ?)
        """, (id_transaksi, id_menu, jumlah, subtotal))
        self.conn.commit()

    # ============================================================
    # 4️⃣  LAPORAN PENJUALAN (TEXT)
    # ============================================================
    def ambil_laporan_harian(self):
        """Ambil total pendapatan per hari"""
        c = self.conn.cursor()
        c.execute("""
        SELECT tanggal, SUM(total) AS total_harian
        FROM transaksi
        GROUP BY tanggal
        ORDER BY tanggal DESC
        """)
        return c.fetchall()

    # ============================================================
    # 5️⃣  DASHBOARD ANALITIK (MATPLOTLIB)
    # ============================================================
    def ambil_data_dashboard(self):
        """Ambil data analitik untuk dashboard"""
        c = self.conn.cursor()
        data = {}

        # a) Pendapatan harian
        c.execute("SELECT tanggal, SUM(total) FROM transaksi GROUP BY tanggal")
        data["pendapatan_harian"] = c.fetchall()

        # b) Metode pembayaran
        c.execute("SELECT metode, COUNT(*) FROM transaksi GROUP BY metode")
        data["metode_pembayaran"] = c.fetchall()

        # c) Menu terlaris
        c.execute("""
        SELECT m.nama, SUM(d.jumlah) AS total_terjual
        FROM detail_transaksi d
        JOIN menu m ON d.id_menu = m.id
        GROUP BY d.id_menu
        ORDER BY total_terjual DESC
        LIMIT 5
        """)
        data["menu_terlaris"] = c.fetchall()

        return data

    # ============================================================
    # 6️⃣  ALIAS UNTUK KOMPATIBILITAS VERSI LAMA
    # ============================================================
    def ambil_menu(self):
        """Alias lama: ambil_menu() → ambil_semua_menu()"""
        return self.ambil_semua_menu()

    def get_analytics_data(self):
        """Alias lama: get_analytics_data() → ambil_data_dashboard()"""
        return self.ambil_data_dashboard()

    # ============================================================
    # 7️⃣  PENUTUP
    # ============================================================
    def tutup_koneksi(self):
        """Tutup koneksi database"""
        self.conn.close()
