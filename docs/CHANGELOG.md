WaruMate Project Changelog
Catatan pengembangan versi aplikasi WaruMate  
"Digital Assistant for Small Culinary Businesses"

---

## Versi 1.0 (Initial Console)
**Tanggal:** 24 Oktober 2025  
**Fitur:**
- Aplikasi berbasis terminal (CLI)
- CRUD menu sederhana (Tambah, Lihat, Hapus)
- Menggunakan `list` dan `dict` sebagai penyimpanan sementara (tanpa DB)
- Struktur OOP dasar: class `Menu`, `WarungMakan`

**Tujuan:** Membangun pondasi sistem WaruMate berbasis Python.

---

## 🏷️ Versi 2.0 (Database Integration)
**Tanggal:** 25 Oktober 2025  
**Fitur:**
- Integrasi database `SQLite` (file `DB_WaruMate.py`)
- Penyimpanan permanen menu (id, nama, harga, stok, kategori)
- Penerapan konsep OOP yang lebih kuat

**Peningkatan:**
- Fungsi CRUD terpisah dari tampilan CLI
- Database handler modular (`DatabaseHandler` class)

---

## 🏷️ Versi 3.0 (Optimized CLI)
**Tanggal:** 27 Oktober 2025  
**Fitur:**
- Tampilan CLI lebih interaktif
- Penambahan fitur laporan penjualan harian
- Validasi input data & penanganan error user-friendly

**Catatan Teknis:**
- Menambahkan `tuple` dan `list comprehension` untuk efisiensi
- Database handler dioptimalkan untuk query cepat

---

## 🏷️ Versi 4.0 (GUI Introduction)
**Tanggal:** 3 November 2025  
**Fitur:**
- Migrasi ke GUI menggunakan `CustomTkinter`
- Tampilan modern (blue-white theme)
- Fitur baru:
  - Transaksi penjualan dengan metode bayar Cash/Non-Cash
  - Stok otomatis berkurang setelah transaksi
  - Laporan penjualan per hari

**Catatan Teknis:**
- Kelas utama: `WaruMateApp`
- Struktur modular: `WaruMate.py` + `DB_WaruMate.py`

---

## 🏷️ Versi 5.0 (Dashboard & Analytics)
**Tanggal:** 3 November 2025  
**Fitur:**
- Dashboard analitik penjualan dengan `Matplotlib`
- Grafik pendapatan harian, metode pembayaran, dan menu terlaris
- Tampilan GUI lebih modern & responsif
- Pembaruan DB Handler (`DB_WaruMate_v5_Refined_Full.py`):
  - Kompatibilitas penuh dengan versi sebelumnya
  - Penambahan fungsi analitik (`ambil_data_dashboard()`)

**Status:** ✅ FINAL STABLE RELEASE
