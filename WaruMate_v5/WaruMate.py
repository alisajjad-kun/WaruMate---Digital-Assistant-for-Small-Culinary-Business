# ============================================================
# WaruMate v5 - Digital Assistant for Small Culinary Businesses
# GUI Modern CustomTkinter + Matplotlib Analytic Dashboard
# ============================================================
# Fitur:
# - Kelola menu (CRUD)
# - Transaksi (Cash / Non-Cash, stok otomatis berkurang)
# - Dashboard & Analitik Penjualan (Pendapatan Harian, Metode Bayar, Menu Terlaris)
# ============================================================

import customtkinter as ctk
from tkinter import ttk, messagebox
from DB_WaruMate import DatabaseHandler
from datetime import datetime
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Inisialisasi database handler
db = DatabaseHandler()


# ============================================================
# Kelas Utama Aplikasi WaruMate
# ============================================================
class WaruMateApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("WaruMate v5 — Digital Assistant for Small Culinary Businesses")
        self.geometry("1200x720")
        self.minsize(1000, 650)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # ====== Layout Dasar ======
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar kiri
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#143d7a")
        self.sidebar.grid(row=0, column=0, sticky="nswe")

        # Logo dan tagline
        ctk.CTkLabel(self.sidebar, text="🍜 WaruMate", text_color="white",
                     font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(40, 10))
        ctk.CTkLabel(self.sidebar, text="Digital Assistant for\nSmall Culinary Businesses",
                     text_color="#dbeafe", font=ctk.CTkFont(size=11)).pack()

        # Tombol Navigasi
        nav_pad = {"pady": 10, "padx": 20}
        ctk.CTkButton(self.sidebar, text="Kelola Menu", fg_color="#1f6feb",
                      command=self.show_menu_page, height=40).pack(**nav_pad)
        ctk.CTkButton(self.sidebar, text="Transaksi", fg_color="#1f6feb",
                      command=self.show_transaksi_page, height=40).pack(**nav_pad)
        ctk.CTkButton(self.sidebar, text="Dashboard", fg_color="#1f6feb",
                      command=self.show_dashboard_page, height=40).pack(**nav_pad)

        # Area konten utama
        self.container = ctk.CTkFrame(self, fg_color="#f8fafc")
        self.container.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

        # Halaman awal
        self.show_menu_page()

    # ============================================================
    # Utility
    # ============================================================
    def clear_container(self):
        """Hapus semua widget di konten utama sebelum pindah halaman"""
        for widget in self.container.winfo_children():
            widget.destroy()

    # ============================================================
    # KELOLA MENU
    # ============================================================
    def show_menu_page(self):
        self.clear_container()

        ctk.CTkLabel(self.container, text="🍽 Kelola Menu",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(10, 10))

        main_frame = ctk.CTkFrame(self.container, fg_color="white", corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Form input menu
        form_frame = ctk.CTkFrame(main_frame, fg_color="#ffffff", corner_radius=10)
        form_frame.pack(side="top", pady=30)

        entries = {}
        for field in ["Nama", "Harga", "Stok", "Kategori"]:
            entry = ctk.CTkEntry(form_frame, placeholder_text=field, width=240, height=32)
            entry.pack(pady=5)
            entries[field.lower()] = entry

        def tambah_menu():
            """Tambah menu baru ke database"""
            nama = entries["nama"].get()
            harga = entries["harga"].get()
            stok = entries["stok"].get()
            kategori = entries["kategori"].get()

            if not all([nama, harga, stok, kategori]):
                messagebox.showwarning("Input Kosong", "Semua kolom harus diisi!")
                return

            db.tambah_menu(nama, float(harga), int(stok), kategori)
            messagebox.showinfo("Sukses", f"Menu '{nama}' berhasil ditambahkan.")
            tampilkan_menu()

        ctk.CTkButton(form_frame, text="Tambah Menu", fg_color="#10b981",
                      command=tambah_menu, width=180, height=35).pack(pady=10)

        # Tabel data menu
        table_frame = ctk.CTkFrame(main_frame, fg_color="#f3f4f6", corner_radius=10)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(10, 20))

        tree = ttk.Treeview(table_frame, columns=("id", "nama", "harga", "stok", "kategori"),
                            show="headings", height=12)
        for col in ("id", "nama", "harga", "stok", "kategori"):
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=200, anchor="center")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        def tampilkan_menu():
            """Tampilkan semua menu ke tabel"""
            for i in tree.get_children():
                tree.delete(i)
            for row in db.ambil_semua_menu():
                tree.insert("", "end", values=row)

        tampilkan_menu()

    # ============================================================
    # TRANSAKSI PENJUALAN
    # ============================================================
    def show_transaksi_page(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="💰 Transaksi Penjualan",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(15, 10))

        frame = ctk.CTkFrame(self.container, fg_color="white", corner_radius=15)
        frame.pack(fill="both", expand=True, padx=40, pady=20)

        # Daftar menu
        tree = ttk.Treeview(frame, columns=("id", "nama", "harga", "stok"), show="headings", height=10)
        for col in ("id", "nama", "harga", "stok"):
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=180, anchor="center")
        tree.pack(fill="x", padx=30, pady=10)

        for row in db.ambil_semua_menu():
            tree.insert("", "end", values=row[:4])

        # Input transaksi
        input_frame = ctk.CTkFrame(frame, fg_color="#f9fafb", corner_radius=10)
        input_frame.pack(pady=20)

        jumlah_entry = ctk.CTkEntry(input_frame, placeholder_text="Jumlah Pembelian", width=200)
        jumlah_entry.pack(side="left", padx=15, pady=15)

        metode_var = ctk.StringVar(value="Cash")
        ctk.CTkRadioButton(input_frame, text="Cash", variable=metode_var, value="Cash").pack(side="left", padx=5)
        ctk.CTkRadioButton(input_frame, text="Non-Cash", variable=metode_var, value="Non-Cash").pack(side="left", padx=5)

        def proses_transaksi():
            """Proses transaksi pembelian"""
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Pilih Menu", "Pilih menu yang akan dibeli!")
                return

            jumlah = jumlah_entry.get()
            if not jumlah.isdigit():
                messagebox.showerror("Input Salah", "Jumlah harus angka!")
                return

            jumlah = int(jumlah)
            id_menu, nama, harga, stok = tree.item(selected[0])["values"][:4]

            if stok < jumlah:
                messagebox.showwarning("Stok Kurang", "Stok tidak mencukupi!")
                return

            subtotal = harga * jumlah
            metode = metode_var.get()
            tanggal = datetime.now().strftime("%Y-%m-%d")

            # Simpan transaksi
            id_transaksi = db.simpan_transaksi(tanggal, subtotal, metode)
            db.simpan_detail_transaksi(id_transaksi, id_menu, jumlah, subtotal)
            db.kurangi_stok(id_menu, jumlah)

            messagebox.showinfo("Transaksi Sukses",
                                f"Menu: {nama}\nJumlah: {jumlah}\nTotal: Rp{subtotal:,}\nMetode: {metode}")
            self.show_transaksi_page()

        ctk.CTkButton(input_frame, text="Bayar Sekarang", fg_color="#0284c7",
                      command=proses_transaksi, width=160, height=35).pack(side="left", padx=15)

    # ============================================================
    # DASHBOARD ANALITIK
    # ============================================================
    def show_dashboard_page(self):
        self.clear_container()
        ctk.CTkLabel(self.container, text="📊 Dashboard Analitik Penjualan",
                     font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))

        data = db.ambil_data_dashboard()
        fig = Figure(figsize=(10, 4), dpi=100)

        # Pendapatan Harian
        if data["pendapatan_harian"]:
            tanggal, total = zip(*data["pendapatan_harian"])
            ax1 = fig.add_subplot(131)
            ax1.bar(tanggal, total, color="#2563eb")
            ax1.set_title("Pendapatan Harian", fontsize=10)
            ax1.tick_params(axis='x', rotation=45)

        # Metode Pembayaran
        if data["metode_pembayaran"]:
            metode, jumlah = zip(*data["metode_pembayaran"])
            ax2 = fig.add_subplot(132)
            ax2.pie(jumlah, labels=metode, autopct='%1.1f%%', colors=["#60a5fa", "#34d399"])
            ax2.set_title("Metode Pembayaran", fontsize=10)

        # Menu Terlaris
        if data["menu_terlaris"]:
            nama_menu, terjual = zip(*data["menu_terlaris"])
            ax3 = fig.add_subplot(133)
            ax3.bar(nama_menu, terjual, color="#f59e0b")
            ax3.set_title("Menu Terlaris", fontsize=10)
            ax3.tick_params(axis='x', rotation=45)

        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=30, pady=20)


# ============================================================
# Jalankan Aplikasi
# ============================================================
if __name__ == "__main__":
    app = WaruMateApp()
    app.mainloop()
