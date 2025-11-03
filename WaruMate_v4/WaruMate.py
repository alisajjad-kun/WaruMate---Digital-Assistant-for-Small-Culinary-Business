# ============================================================
# WaruMate
# GUI Modern CustomTkinter untuk WaruMate v4
# Fitur:
# - Kelola Menu (CRUD)
# - Transaksi (Cash/Non-Cash)
# - Laporan per kategori & harian
# ============================================================

import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime
from DB_WaruMate import DatabaseHandler

db = DatabaseHandler()

# -----------------------------
# Aplikasi utama
# -----------------------------
class WaruMateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WaruMate v4 - Sistem Manajemen Warung Makan")
        self.geometry("1200x720")
        self.minsize(1000, 650)

        # Tema visual
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Layout grid utama
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar biru kiri
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#143d7a")
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(6, weight=1)

        ctk.CTkLabel(self.sidebar, text="🍜 WaruMate", text_color="white",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(24,4))
        ctk.CTkLabel(self.sidebar, text="Digital Assistant for\nSmall Culinary Businesses",
                     text_color="#cbd5e1", font=ctk.CTkFont(size=10)).pack()

        # Tombol navigasi
        self.btn_menu = ctk.CTkButton(self.sidebar, text="Kelola Menu", fg_color="#1f6feb", command=self.show_menu_page)
        self.btn_trans = ctk.CTkButton(self.sidebar, text="Transaksi", fg_color="#1f6feb", command=self.show_transaksi_page)
        self.btn_lap = ctk.CTkButton(self.sidebar, text="Laporan", fg_color="#1f6feb", command=self.show_laporan_page)

        self.btn_menu.pack(pady=(30,8), padx=20)
        self.btn_trans.pack(pady=8, padx=20)
        self.btn_lap.pack(pady=8, padx=20)

        # Kontainer utama (content area)
        self.container = ctk.CTkFrame(self, fg_color="white")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.show_menu_page()  # halaman default

    # -----------------------------
    # Utility: bersihkan kontainer
    # -----------------------------
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    # -----------------------------
    # Halaman: Kelola Menu
    # -----------------------------
    def show_menu_page(self):
        self.clear_container()
        header = ctk.CTkLabel(self.container, text="🍽 Kelola Menu", font=ctk.CTkFont(size=20, weight="bold"))
        header.grid(row=0, column=0, sticky="w", pady=(6,12))

        content = ctk.CTkFrame(self.container)
        content.grid(row=1, column=0, sticky="nsew")
        content.grid_columnconfigure(1, weight=1)

        # Kartu form tambah menu
        card = ctk.CTkFrame(content, width=320, corner_radius=8, fg_color="#f8fafc")
        card.grid(row=0, column=0, sticky="nw", padx=(0,12), pady=6)
        card.grid_propagate(False)

        ctk.CTkLabel(card, text="Tambah Menu Baru", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,6))
        self.nama_entry = ctk.CTkEntry(card, placeholder_text="Nama menu")
        self.nama_entry.pack(fill="x", padx=12, pady=4)
        self.harga_entry = ctk.CTkEntry(card, placeholder_text="Harga")
        self.harga_entry.pack(fill="x", padx=12, pady=4)
        self.stok_entry = ctk.CTkEntry(card, placeholder_text="Stok")
        self.stok_entry.pack(fill="x", padx=12, pady=4)
        self.kategori_entry = ctk.CTkEntry(card, placeholder_text="Kategori")
        self.kategori_entry.pack(fill="x", padx=12, pady=4)
        ctk.CTkButton(card, text="Tambah Menu", command=self.tambah_menu, fg_color="#10b981").pack(fill="x", padx=12, pady=(8,12))

        # Tabel daftar menu
        tree_container = ctk.CTkFrame(content, fg_color="white")
        tree_container.grid(row=0, column=1, sticky="nsew", pady=6)
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)

        cols = ("id", "nama", "harga", "stok", "kategori")
        self.tree = ttk.Treeview(tree_container, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=130 if c != "id" else 60, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        self.tampilkan_menu()

    def tampilkan_menu(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in db.ambil_menu():
            self.tree.insert("", "end", values=row)

    def tambah_menu(self):
        nama = self.nama_entry.get().strip()
        harga = self.harga_entry.get().strip()
        stok = self.stok_entry.get().strip()
        kategori = self.kategori_entry.get().strip()
        if not all([nama, harga, stok, kategori]):
            messagebox.showwarning("Input Kosong", "Semua kolom wajib diisi!")
            return
        try:
            db.tambah_menu(nama, float(harga), int(stok), kategori)
            messagebox.showinfo("Sukses", f"Menu '{nama}' ditambahkan.")
            self.tampilkan_menu()
            self.nama_entry.delete(0, "end")
            self.harga_entry.delete(0, "end")
            self.stok_entry.delete(0, "end")
            self.kategori_entry.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah menu: {e}")

    # -----------------------------
    # Halaman: Transaksi
    # -----------------------------
    def show_transaksi_page(self):
        self.clear_container()
        header = ctk.CTkLabel(self.container, text="💰 Transaksi Penjualan", font=ctk.CTkFont(size=20, weight="bold"))
        header.grid(row=0, column=0, sticky="w", pady=(6,12))

        frame = ctk.CTkFrame(self.container, fg_color="white")
        frame.grid(row=1, column=0, sticky="nsew")

        # Daftar menu
        self.trans_tree = ttk.Treeview(frame, columns=("id", "nama", "harga", "stok"), show="headings")
        for col in ("id", "nama", "harga", "stok"):
            self.trans_tree.heading(col, text=col.capitalize())
            self.trans_tree.column(col, width=150)
        self.trans_tree.pack(fill="both", expand=True, padx=20, pady=10)

        for row in db.ambil_menu():
            self.trans_tree.insert("", "end", values=row[:4])

        # Form input transaksi
        form = ctk.CTkFrame(frame, fg_color="#f8fafc", corner_radius=8)
        form.pack(pady=10)
        self.jumlah_entry = ctk.CTkEntry(form, placeholder_text="Jumlah")
        self.jumlah_entry.pack(side="left", padx=10, pady=10)
        self.metode_var = ctk.StringVar(value="Cash")
        ctk.CTkRadioButton(form, text="Cash", variable=self.metode_var, value="Cash").pack(side="left", padx=6)
        ctk.CTkRadioButton(form, text="Non-Cash", variable=self.metode_var, value="Non-Cash").pack(side="left", padx=6)
        ctk.CTkButton(form, text="Bayar", command=self.proses_transaksi, fg_color="#0284c7").pack(side="left", padx=10)

    def proses_transaksi(self):
        selected = self.trans_tree.selection()
        if not selected:
            messagebox.showwarning("Pilih Menu", "Pilih menu yang ingin dibeli.")
            return
        jumlah = self.jumlah_entry.get().strip()
        if not jumlah.isdigit():
            messagebox.showerror("Input Error", "Jumlah harus angka.")
            return
        jumlah = int(jumlah)
        id_menu, nama, harga, stok = self.trans_tree.item(selected[0])["values"]
        if stok < jumlah:
            messagebox.showwarning("Stok Kurang", "Stok tidak mencukupi.")
            return
        subtotal = harga * jumlah
        metode = self.metode_var.get()
        db.tambah_transaksi([{"id_menu": id_menu, "jumlah": jumlah, "subtotal": subtotal}], metode)
        messagebox.showinfo("Sukses", f"Transaksi berhasil!\nMenu: {nama}\nTotal: Rp{subtotal:,}\nMetode: {metode}")
        self.show_transaksi_page()

    # -----------------------------
    # Halaman: Laporan
    # -----------------------------
    def show_laporan_page(self):
        self.clear_container()
        header = ctk.CTkLabel(self.container, text="📊 Laporan Penjualan", font=ctk.CTkFont(size=20, weight="bold"))
        header.grid(row=0, column=0, sticky="w", pady=(6,12))

        frame = ctk.CTkFrame(self.container, fg_color="white")
        frame.grid(row=1, column=0, sticky="nsew")

        kategori = db.laporan_per_kategori()
        tanggal = datetime.now().strftime("%Y-%m-%d")
        harian = db.laporan_harian(tanggal)

        ctk.CTkLabel(frame, text="📁 Laporan Per Kategori", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,4))
        if kategori:
            for row in kategori:
                ctk.CTkLabel(frame, text=f"- {row[0]} : {row[1]} menu").pack(anchor="w", padx=20)
        else:
            ctk.CTkLabel(frame, text="Belum ada data kategori.").pack(anchor="w", padx=20)

        ctk.CTkLabel(frame, text="\n🗓 Laporan Transaksi Hari Ini", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10,4))
        if harian:
            total = sum([row[2] for row in harian])
            ctk.CTkLabel(frame, text=f"Total transaksi hari ini: Rp{total:,}").pack()
        else:
            ctk.CTkLabel(frame, text="Belum ada transaksi hari ini.").pack()


# -----------------------------
# Jalankan aplikasi
# -----------------------------
if __name__ == "__main__":
    app = WaruMateApp()
    app.mainloop()
