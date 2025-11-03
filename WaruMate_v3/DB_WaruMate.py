# ============================================================
# DB_WaruMate.py
# Database handler untuk WaruMate v3
# Menangani: koneksi SQLite, pembuatan tabel, CRUD menu,
# transaksi sederhana, dan laporan penjualan per kategori.
# ============================================================

import sqlite3
from datetime import datetime

class DatabaseHandler:
    """
    Class untuk mengatur koneksi dan operasi database SQLite.
    Semua query menggunakan parameterized query untuk keamanan.
    """

    def __init__(self, db_name="warung.db"):
        # buka koneksi ke file SQLite (akan dibuat otomatis jika belum ada)
        self.conn = sqlite3.connect(db_name)
        # enable foreign keys (penting untuk relasi)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        # membuat tabel jika belum ada
        self.create_tables()

    def create_tables(self):
        """Membuat tabel menu, transaksi, dan detail_transaksi jika belum ada."""
        cur = self.conn.cursor()

        # Tabel menu: id, nama, harga, stok (opsional), kategori
        cur.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id_menu INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_menu TEXT NOT NULL,
            harga REAL NOT NULL,
            stok INTEGER DEFAULT 0,
            kategori TEXT
        );
        """)

        # Tabel transaksi: satu baris per transaksi (tanggal + total)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS transaksi (
            id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
            tanggal TEXT NOT NULL,
            total REAL DEFAULT 0
        );
        """)

        # Tabel detail_transaksi: item per transaksi
        cur.execute("""
        CREATE TABLE IF NOT EXISTS detail_transaksi (
            id_detail INTEGER PRIMARY KEY AUTOINCREMENT,
            id_transaksi INTEGER NOT NULL,
            id_menu INTEGER NOT NULL,
            jumlah INTEGER NOT NULL,
            subtotal REAL NOT NULL,
            FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi) ON DELETE CASCADE,
            FOREIGN KEY (id_menu) REFERENCES menu(id_menu) ON DELETE RESTRICT
        );
        """)

        self.conn.commit()

    # ---------------------------
    # Operasi CRUD untuk tabel menu
    # ---------------------------

    def tambah_menu(self, nama, harga, stok=0, kategori="Umum"):
        """Masukkan menu baru ke tabel menu."""
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO menu (nama_menu, harga, stok, kategori) VALUES (?, ?, ?, ?)",
            (nama, harga, stok, kategori)
        )
        self.conn.commit()
        return cur.lastrowid  # mengembalikan id_menu yang baru

    def tampilkan_semua_menu(self):
        """Ambil semua baris dari tabel menu (tuple list)."""
        cur = self.conn.cursor()
        cur.execute("SELECT id_menu, nama_menu, harga, stok, kategori FROM menu ORDER BY id_menu")
        return cur.fetchall()

    def cari_menu_by_name(self, keyword):
        """Cari menu berdasarkan keyword (LIKE)."""
        cur = self.conn.cursor()
        like = f"%{keyword}%"
        cur.execute("SELECT id_menu, nama_menu, harga, stok, kategori FROM menu WHERE nama_menu LIKE ? ORDER BY id_menu", (like,))
        return cur.fetchall()

    def filter_menu_by_category(self, kategori):
        """Ambil daftar menu berdasarkan kategori."""
        cur = self.conn.cursor()
        cur.execute("SELECT id_menu, nama_menu, harga, stok, kategori FROM menu WHERE kategori = ? ORDER BY id_menu", (kategori,))
        return cur.fetchall()

    def update_stok(self, id_menu, delta):
        """
        Kurangi atau tambah stok. delta bisa negatif (kurangi) atau positif (tambah).
        Mengembalikan True jika berhasil (stok tidak menjadi negatif), False jika gagal.
        """
        cur = self.conn.cursor()
        # Ambil stok saat ini
        cur.execute("SELECT stok FROM menu WHERE id_menu = ?", (id_menu,))
        row = cur.fetchone()
        if not row:
            return False  # menu tidak ditemukan
        stok_sekarang = row[0] if row[0] is not None else 0
        stok_baru = stok_sekarang + delta
        if stok_baru < 0:
            return False  # stok tidak mencukupi
        cur.execute("UPDATE menu SET stok = ? WHERE id_menu = ?", (stok_baru, id_menu))
        self.conn.commit()
        return True

    # ---------------------------
    # Operasi transaksi & detail
    # ---------------------------

    def simpan_transaksi(self, items):
        """
        Menyimpan transaksi dan detailnya.
        `items` = list of dict: {"id_menu": int, "jumlah": int, "harga": float}
        Fungsi akan:
         - masukkan baris ke tabel transaksi
         - masukkan setiap item ke detail_transaksi
         - update stok (jika stok dipakai)
        Mengembalikan id_transaksi yang baru.
        """
        if not items:
            raise ValueError("Tidak ada item untuk disimpan.")

        cur = self.conn.cursor()
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # simpan transaksi dulu dengan total sementara 0
        cur.execute("INSERT INTO transaksi (tanggal, total) VALUES (?, ?)", (tanggal, 0.0))
        id_trans = cur.lastrowid

        total = 0.0
        for it in items:
            id_menu = it["id_menu"]
            jumlah = int(it["jumlah"])
            harga = float(it["harga"])
            subtotal = jumlah * harga
            total += subtotal

            # masukkan ke detail_transaksi
            cur.execute(
                "INSERT INTO detail_transaksi (id_transaksi, id_menu, jumlah, subtotal) VALUES (?, ?, ?, ?)",
                (id_trans, id_menu, jumlah, subtotal)
            )

            # update stok (jika tersedia), kurangi stok sebanyak jumlah
            # Jika update_stok gagal (stok tidak cukup) -> rollback dan raise
            # Perhatikan: update_stok meng-commit sendiri; untuk atomicity sederhana kita tidak gunakan transaksi SQL kompleks di sini
            ok = self.update_stok(id_menu, -jumlah)
            if not ok:
                # jika stok tidak cukup, batalkan dengan menghapus detail_transaksi yang sudah masuk dan transaksi
                self.conn.rollback()
                raise RuntimeError(f"Stok tidak cukup untuk id_menu={id_menu}")

        # update total di tabel transaksi
        cur.execute("UPDATE transaksi SET total = ? WHERE id_transaksi = ?", (total, id_trans))
        self.conn.commit()
        return id_trans

    # ---------------------------
    # Laporan penjualan per kategori
    # ---------------------------

    def laporan_penjualan_per_kategori(self, tanggal_mulai=None, tanggal_selesai=None):
        """
        Mengembalikan rekap jumlah terjual dan total omzet per kategori.
        Jika tanggal_mulai / tanggal_selesai None -> ambil seluruh data.
        Format return: list of tuples (kategori, jumlah_terjual, total_omzet)
        """
        cur = self.conn.cursor()

        # Jika filter tanggal diberikan, gunakan WHERE dengan range DATE(tanggal)
        if tanggal_mulai and tanggal_selesai:
            query = """
            SELECT m.kategori, SUM(d.jumlah) AS jumlah_terjual, SUM(d.subtotal) AS total_omzet
            FROM detail_transaksi d
            JOIN transaksi t ON d.id_transaksi = t.id_transaksi
            JOIN menu m ON d.id_menu = m.id_menu
            WHERE DATE(t.tanggal) BETWEEN DATE(?) AND DATE(?)
            GROUP BY m.kategori
            ORDER BY total_omzet DESC;
            """
            params = (tanggal_mulai, tanggal_selesai)
            cur.execute(query, params)
        else:
            query = """
            SELECT m.kategori, SUM(d.jumlah) AS jumlah_terjual, SUM(d.subtotal) AS total_omzet
            FROM detail_transaksi d
            JOIN transaksi t ON d.id_transaksi = t.id_transaksi
            JOIN menu m ON d.id_menu = m.id_menu
            GROUP BY m.kategori
            ORDER BY total_omzet DESC;
            """
            cur.execute(query)

        return cur.fetchall()

    # ---------------------------
    # Utility
    # ---------------------------

    def close(self):
        """Menutup koneksi database (jika ingin ditutup eksplisit)."""
        try:
            self.conn.close()
        except:
            pass

    def __del__(self):
        # pastikan koneksi ditutup saat object dihapus
        self.close()
