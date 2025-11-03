# ============================================================
# Program : WaruMate v2
# Deskripsi : Sistem Manajemen Warung Makan berbasis Database (SQLite)
# Konsep : OOP, Modularisasi, Database Handling
# ============================================================

from DB_WaruMate import DatabaseHandler

# Membuat objek dari class DatabaseHandler
db = DatabaseHandler()

# ------------------------------------------------------------
# Fungsi: Tambah Menu
# ------------------------------------------------------------
def tambah_menu():
    print("\n=== Tambah Menu Baru ===")
    nama = input("Masukkan nama menu: ")
    harga = float(input("Masukkan harga menu: "))
    kategori = input("Masukkan kategori menu (contoh: Makanan, Minuman, Lauk): ")

    db.tambah_menu(nama, harga, kategori)
    print(f"✅ Menu '{nama}' berhasil ditambahkan ke database!\n")

# ------------------------------------------------------------
# Fungsi: Lihat Semua Menu
# ------------------------------------------------------------
def lihat_menu():
    print("\n=== Daftar Menu di Database ===")
    data_menu = db.tampilkan_semua_menu()

    if not data_menu:
        print("⚠️ Belum ada data menu tersimpan.\n")
        return

    for row in data_menu:
        id_menu, nama, harga, kategori = row
        print(f"{id_menu}. {nama} - Rp{harga} [{kategori}]")
    print()

# ------------------------------------------------------------
# Fungsi: Hapus Menu
# ------------------------------------------------------------
def hapus_menu():
    lihat_menu()
    try:
        id_menu = int(input("Masukkan ID menu yang ingin dihapus: "))
        db.hapus_menu(id_menu)
        print("🗑️ Menu berhasil dihapus!\n")
    except ValueError:
        print("⚠️ Input tidak valid.\n")

# ------------------------------------------------------------
# Fungsi: Ubah Menu
# ------------------------------------------------------------
def ubah_menu():
    lihat_menu()
    try:
        id_menu = int(input("Masukkan ID menu yang ingin diubah: "))
        nama = input("Masukkan nama menu baru: ")
        harga = float(input("Masukkan harga baru: "))
        kategori = input("Masukkan kategori baru: ")

        db.ubah_menu(id_menu, nama, harga, kategori)
        print("✏️ Menu berhasil diperbarui!\n")
    except ValueError:
        print("⚠️ Input tidak valid.\n")

# ------------------------------------------------------------
# Fungsi: Menu Utama
# ------------------------------------------------------------
def main():
    while True:
        print("=== SISTEM MANAJEMEN WARUNG MAKAN (WaruMate v2) ===")
        print("1. Tambah Menu")
        print("2. Lihat Semua Menu")
        print("3. Ubah Menu")
        print("4. Hapus Menu")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tambah_menu()
        elif pilihan == "2":
            lihat_menu()
        elif pilihan == "3":
            ubah_menu()
        elif pilihan == "4":
            hapus_menu()
        elif pilihan == "5":
            print("👋 Terima kasih telah menggunakan WaruMate v2!\n")
            break
        else:
            print("❌ Pilihan tidak valid, coba lagi.\n")

# ------------------------------------------------------------
# Jalankan program utama
# ------------------------------------------------------------
if __name__ == "__main__":
    main()
