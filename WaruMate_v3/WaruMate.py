# ============================================================
# WaruMate.py (v3)
# Aplikasi CLI WaruMate v3
# Fitur: tambah menu, lihat menu, cari, filter kategori,
# transaksi sederhana (simpan ke DB), laporan penjualan per kategori.
# ============================================================

from DB_WaruMate import DatabaseHandler

# Buat objek DatabaseHandler (akan membuat warung.db & tabel jika belum ada)
db = DatabaseHandler()

def tambah_menu():
    """Input data menu dan simpan ke database."""
    print("\n=== Tambah Menu Baru ===")
    nama = input("Masukkan nama menu: ").strip()
    try:
        harga = float(input("Masukkan harga menu (contoh: 15000): "))
    except ValueError:
        print("⚠️ Harga tidak valid. Proses dibatalkan.")
        return
    try:
        stok = int(input("Masukkan stok awal (angka): "))
    except ValueError:
        stok = 0
    kategori = input("Masukkan kategori (contoh: Makanan / Minuman / Lauk): ").strip()
    db.tambah_menu(nama, harga, stok, kategori)
    print(f"✅ Menu '{nama}' berhasil ditambahkan.\n")

def lihat_menu():
    """Tampilkan semua menu tersimpan di database."""
    print("\n=== Daftar Menu ===")
    data = db.tampilkan_semua_menu()
    if not data:
        print("⚠️ Belum ada menu tersimpan.\n")
        return
    for row in data:
        id_menu, nama, harga, stok, kategori = row
        print(f"{id_menu}. {nama} - Rp{int(harga)} (Stok: {stok}) [{kategori}]")
    print()

def cari_menu():
    """Cari menu berdasarkan kata kunci nama."""
    keyword = input("Masukkan kata kunci nama menu yang dicari: ").strip()
    if not keyword:
        print("⚠️ Kata kunci kosong.\n"); return
    hasil = db.cari_menu_by_name(keyword)
    if not hasil:
        print("🔍 Tidak ditemukan menu yang cocok.\n"); return
    print("\nHasil pencarian:")
    for row in hasil:
        id_menu, nama, harga, stok, kategori = row
        print(f"{id_menu}. {nama} - Rp{int(harga)} (Stok: {stok}) [{kategori}]")
    print()

def filter_kategori():
    """Tampilkan menu berdasarkan kategori."""
    kategori = input("Masukkan kategori yang ingin difilter: ").strip()
    if not kategori:
        print("⚠️ Kategori kosong.\n"); return
    hasil = db.filter_menu_by_category(kategori)
    if not hasil:
        print(f"⚠️ Tidak ada menu pada kategori '{kategori}'.\n"); return
    print(f"\nMenu pada kategori '{kategori}':")
    for row in hasil:
        id_menu, nama, harga, stok, kategori = row
        print(f"{id_menu}. {nama} - Rp{int(harga)} (Stok: {stok})")
    print()

def transaksi_sederhana():
    """
    Proses transaksi sederhana:
    - Tampilkan menu
    - Pilih beberapa item dengan jumlah
    - Simpan transaksi (detail + update stok) ke database
    """
    print("\n=== Transaksi Pembelian ===")
    semua = db.tampilkan_semua_menu()
    if not semua:
        print("⚠️ Belum ada menu untuk transaksi.\n"); return

    # tampilkan menu singkat
    for row in semua:
        id_menu, nama, harga, stok, kategori = row
        print(f"{id_menu}. {nama} - Rp{int(harga)} (Stok: {stok})")

    items = []
    while True:
        choice = input("Masukkan ID menu ingin dibeli (atau ketik 'selesai'): ").strip()
        if choice.lower() == "selesai":
            break
        try:
            id_menu = int(choice)
        except ValueError:
            print("⚠️ ID tidak valid, coba lagi.")
            continue

        # ambil data menu untuk id tersebut
        # kita pakai method cari untuk memeriksa keberadaan
        hasil = db.cari_menu_by_name("")  # tidak ideal untuk lookup by id, jadi gunakan fetch langsung
        # lebih baik: query langsung id
        from sqlite3 import Connection
        # ambil baris menu
        cur = db.conn.cursor()
        cur.execute("SELECT id_menu, nama_menu, harga, stok FROM menu WHERE id_menu = ?", (id_menu,))
        row = cur.fetchone()
        if not row:
            print("⚠️ Menu dengan ID tersebut tidak ditemukan.")
            continue
        _, nama, harga, stok = row
        try:
            jumlah = int(input(f"Masukkan jumlah untuk '{nama}': "))
        except ValueError:
            print("⚠️ Jumlah tidak valid.")
            continue
        if jumlah <= 0:
            print("⚠️ Jumlah harus lebih dari 0.")
            continue
        # cek stok
        if stok is not None and stok < jumlah:
            print(f"⚠️ Stok untuk '{nama}' tidak cukup (Stok: {stok}).")
            continue
        # simpan item ke list items
        items.append({"id_menu": id_menu, "jumlah": jumlah, "harga": harga})
        print(f"Ditambahkan ke keranjang: {nama} x{jumlah} (Rp{int(jumlah*harga)})")

    if not items:
        print("⚠️ Tidak ada item dibeli. Transaksi dibatalkan.\n"); return

    # simpan transaksi ke DB (fungsi ini juga akan update stok)
    try:
        id_trans = db.simpan_transaksi(items)
        print(f"✅ Transaksi berhasil disimpan (ID transaksi: {id_trans}).\n")
    except Exception as e:
        print(f"❌ Gagal menyimpan transaksi: {e}\n")

def laporan_per_kategori():
    """Menampilkan laporan penjualan per kategori (seluruh periode)."""
    print("\n=== Laporan Penjualan per Kategori ===")
    hasil = db.laporan_penjualan_per_kategori()
    if not hasil:
        print("⚠️ Belum ada data penjualan.\n"); return
    for row in hasil:
        kategori, jumlah_terjual, total_omzet = row
        print(f"- {kategori}: Terjual {int(jumlah_terjual)} item, Omzet Rp{int(total_omzet)}")
    print()

def main():
    """Menu utama CLI untuk WaruMate v3"""
    while True:
        print("=== WARUMATE v3 - Filter, Pencarian & Laporan ===")
        print("1. Tambah Menu")
        print("2. Lihat Semua Menu")
        print("3. Cari Menu (by name)")
        print("4. Filter Menu (by kategori)")
        print("5. Transaksi Pembelian (sederhana)")
        print("6. Laporan: Penjualan per Kategori")
        print("7. Keluar")
        pilihan = input("Pilih menu (1-7): ").strip()

        if pilihan == "1":
            tambah_menu()
        elif pilihan == "2":
            lihat_menu()
        elif pilihan == "3":
            cari_menu()
        elif pilihan == "4":
            filter_kategori()
        elif pilihan == "5":
            transaksi_sederhana()
        elif pilihan == "6":
            laporan_per_kategori()
        elif pilihan == "7":
            print("👋 Terima kasih telah menggunakan WaruMate v3!\n")
            break
        else:
            print("❌ Pilihan tidak valid. Coba lagi.\n")

if __name__ == "__main__":
    main()
