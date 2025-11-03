# ============================================================
# Program : WaruMate v1
# Deskripsi : Sistem Manajemen Warung Makan Sederhana (Versi 1)
# ============================================================

# ====================
# CLASS MENU
# ====================
class Menu:
    def __init__(self, nama, harga, stok):
        self.nama = nama      # atribut nama menu
        self.harga = harga    # atribut harga menu
        self.stok = stok      # atribut stok menu

    def tampilkan_info(self):
        """Menampilkan informasi menu"""
        print(f"{self.nama} - Rp{self.harga} ({self.stok} porsi)")

    def kurangi_stok(self, jumlah):
        """Mengurangi stok setelah pembelian"""
        if jumlah <= self.stok:
            self.stok -= jumlah
            return True
        else:
            print(f"❌ Stok {self.nama} tidak mencukupi!")
            return False


# ====================
# CLASS TRANSAKSI
# ====================
class Transaksi:
    def __init__(self):
        self.daftar_beli = []  # list berisi (menu, jumlah)
        self.total = 0

    def tambah_item(self, menu, jumlah):
        """Menambah item ke daftar transaksi"""
        if menu.kurangi_stok(jumlah):  # cek stok dulu
            self.daftar_beli.append((menu, jumlah))
            subtotal = menu.harga * jumlah
            self.total += subtotal
            print(f"✅ {jumlah}x {menu.nama} ditambahkan ke transaksi (Subtotal: Rp{subtotal})")

    def tampilkan_ringkasan(self):
        """Menampilkan daftar pesanan dan total"""
        print("\n🧾 Ringkasan Transaksi:")
        for menu, jumlah in self.daftar_beli:
            print(f"- {menu.nama} x{jumlah} = Rp{menu.harga * jumlah}")
        print(f"Total Pembayaran: Rp{self.total}")


# ====================
# PROGRAM UTAMA
# ====================
def main():
    # Membuat daftar menu
    menu1 = Menu("Nasi Goreng", 15000, 10)
    menu2 = Menu("Mie Ayam", 12000, 8)
    menu3 = Menu("Es Teh", 5000, 15)

    # Simpan semua menu dalam list
    daftar_menu = [menu1, menu2, menu3]

    # Membuat objek transaksi baru
    transaksi = Transaksi()

    print("=== SELAMAT DATANG DI WARUNG MAKAN PYTHON ===")

    while True:
        print("\n📋 Daftar Menu:")
        for i, m in enumerate(daftar_menu):
            print(f"{i+1}. {m.nama} - Rp{m.harga} ({m.stok} tersedia)")

        pilih = input("\nPilih nomor menu (atau '0' untuk selesai): ")

        if pilih == "0":
            break

        try:
            index = int(pilih) - 1
            if 0 <= index < len(daftar_menu):
                jumlah = int(input(f"Masukkan jumlah pesanan untuk {daftar_menu[index].nama}: "))
                transaksi.tambah_item(daftar_menu[index], jumlah)
            else:
                print("❌ Pilihan tidak valid.")
        except ValueError:
            print("❌ Input harus berupa angka!")

    transaksi.tampilkan_ringkasan()
    print("\nTerima kasih sudah berbelanja! 🍽️")


# Jalankan program
if __name__ == "__main__":
    main()
