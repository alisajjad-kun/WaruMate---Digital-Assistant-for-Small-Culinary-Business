# ============================================================
# DB_WaruMate_v4.py
# Database handler untuk WaruMate v4
# ============================================================

import sqlite3
from datetime import datetime

class DatabaseHandler:
    def __init__(self, db_name="warung.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS menu (
                id_menu INTEGER PRIMARY KEY AUTOINCREMENT,
                nama_menu TEXT NOT NULL,
                harga REAL NOT NULL,
                stok INTEGER NOT NULL,
                kategori TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS transaksi (
                id_transaksi INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT NOT NULL,
                total REAL NOT NULL,
                metode_bayar TEXT NOT NULL
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS detail_transaksi (
                id_detail INTEGER PRIMARY KEY AUTOINCREMENT,
                id_transaksi INTEGER,
                id_menu INTEGER,
                jumlah INTEGER,
                subtotal REAL
            )
        """)
        self.conn.commit()

    # ----------------------------
    # CRUD MENU
    # ----------------------------
    def tambah_menu(self, nama, harga, stok, kategori):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO menu (nama_menu, harga, stok, kategori) VALUES (?, ?, ?, ?)",
            (nama, harga, stok, kategori)
        )
        self.conn.commit()

    def ambil_menu(self):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM menu")
        return cur.fetchall()

    def hapus_menu(self, id_menu):
        cur = self.conn.cursor()
        cur.execute("DELETE FROM menu WHERE id_menu = ?", (id_menu,))
        self.conn.commit()

    def cari_menu(self, keyword):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM menu WHERE nama_menu LIKE ?", (f"%{keyword}%",))
        return cur.fetchall()

    def update_stok(self, id_menu, jumlah_terjual):
        cur = self.conn.cursor()
        cur.execute("UPDATE menu SET stok = stok - ? WHERE id_menu = ?", (jumlah_terjual, id_menu))
        self.conn.commit()

    # ----------------------------
    # TRANSAKSI
    # ----------------------------
    def tambah_transaksi(self, items, metode_bayar):
        cur = self.conn.cursor()
        total = sum([item['subtotal'] for item in items])
        tanggal = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("""
            INSERT INTO transaksi (tanggal, total, metode_bayar)
            VALUES (?, ?, ?)
        """, (tanggal, total, metode_bayar))
        id_trans = cur.lastrowid

        for item in items:
            cur.execute("""
                INSERT INTO detail_transaksi (id_transaksi, id_menu, jumlah, subtotal)
                VALUES (?, ?, ?, ?)
            """, (id_trans, item['id_menu'], item['jumlah'], item['subtotal']))
            self.update_stok(item['id_menu'], item['jumlah'])

        self.conn.commit()
        return id_trans

    # ----------------------------
    # LAPORAN
    # ----------------------------
    def laporan_per_kategori(self):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT kategori, COUNT(*) AS jumlah
            FROM menu
            GROUP BY kategori
        """)
        return cur.fetchall()

    def laporan_harian(self, tanggal):
        cur = self.conn.cursor()
        cur.execute("""
            SELECT t.id_transaksi, t.tanggal, t.total, t.metode_bayar
            FROM transaksi t
            WHERE DATE(t.tanggal) = ?
        """, (tanggal,))
        return cur.fetchall()

