# ============================================================
# File : DB_WaruMate.py
# Deskripsi : Modul koneksi dan manajemen database untuk WaruMate v2
# Konsep : Menggunakan OOP (Class dan Method)
# ============================================================

import sqlite3

class DatabaseHandler:
    """Class untuk mengatur koneksi dan interaksi dengan database SQLite."""

    def __init__(self, db_name="warung.db"):
        # Saat objek dibuat, otomatis terhubung ke database
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        """Membuat tabel menu jika belum ada."""
        query = """
        CREATE TABLE IF NOT EXISTS menu (
            id_menu INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_menu TEXT NOT NULL,
            harga REAL NOT NULL,
            kategori TEXT
        );
        """
        self.conn.execute(query)
        self.conn.commit()

    def tambah_menu(self, nama, harga, kategori):
        """Menambahkan menu baru ke dalam database."""
        query = "INSERT INTO menu (nama_menu, harga, kategori) VALUES (?, ?, ?)"
        self.conn.execute(query, (nama, harga, kategori))
        self.conn.commit()

    def tampilkan_semua_menu(self):
        """Mengambil semua data menu dari database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM menu")
        return cursor.fetchall()

    def hapus_menu(self, id_menu):
        """Menghapus menu berdasarkan ID."""
        query = "DELETE FROM menu WHERE id_menu = ?"
        self.conn.execute(query, (id_menu,))
        self.conn.commit()

    def ubah_menu(self, id_menu, nama, harga, kategori):
        """Mengubah data menu berdasarkan ID."""
        query = "UPDATE menu SET nama_menu=?, harga=?, kategori=? WHERE id_menu=?"
        self.conn.execute(query, (nama, harga, kategori, id_menu))
        self.conn.commit()

    def __del__(self):
        """Menutup koneksi saat objek dihapus."""
        self.conn.close()
