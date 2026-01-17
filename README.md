# ✨ My Todo List - PBO Edition

Aplikasi To-Do List dengan implementasi OOP yang sempurna untuk pembelajaran Pemrograman Berorientasi Objek (PBO) Semester 3.

## 📋 Daftar File Penting

| File | Fungsi | Wajib? |
|------|--------|--------|
| `todo_app.py` | Aplikasi utama dengan GUI | ✅ **YA** |
| `tasks.json` | Database (akan auto-create) | ⚠️ Opsional |
| `requirements.txt` | Daftar dependencies | ✅ **YA** |
| `README.md` | Panduan setup & run | ✅ **YA** |
| `.gitignore` | File yang di-ignore Git | ✅ **YA** |
| `PRESENTASI_OUTLINE.md` | Slide presentasi | 📚 Dokumentasi |
| `OOP_IMPLEMENTASI.md` | Penjelasan OOP detail | 📚 Dokumentasi |
| `PENJELASAN_PER_BARIS.md` | Tips presentasi 7 menit | 📚 Dokumentasi |
| `UML_PENJELASAN_SINGKAT.md` | Diagram UML | 📚 Dokumentasi |

## ⚙️ Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/[username]/Project-PBO-KERKOM.git
cd Project-PBO-KERKOM
```

### 2. Install Python 3.8+
Pastikan Python 3.8 atau lebih baru sudah terinstall di komputer.

**Windows:**
- Download dari [python.org](https://www.python.org)
- Install dan centang "Add Python to PATH"

**Linux/Mac:**
```bash
# macOS dengan Homebrew
brew install python3

# Ubuntu/Debian
sudo apt-get install python3 python3-pip python3-tk
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Apa yang akan diinstall:**
- `tkcalendar==1.6.1` - Calendar picker widget
- `tkinter` - Built-in dengan Python (tidak perlu install)

### 4. Jalankan Aplikasi
```bash
python todo_app.py
```

## 🎯 Fitur Aplikasi

✅ **Tambah Task** - Buat task baru dengan judul, deskripsi, kategori, deadline
✅ **Calendar Picker** - Pilih deadline dengan visual calendar
✅ **Edit Task** - Ubah informasi task yang sudah ada
✅ **Hapus Task** - Menghapus task dari list
✅ **Search/Filter** - Cari task berdasarkan kata kunci
✅ **Smart Status** - Auto-deteksi deadline < 3 hari sebagai "Mendesak"
✅ **Progress Bar** - Visualisasi persentase task selesai
✅ **Data Persistence** - Simpan otomatis ke JSON

## 📁 Struktur File di GitHub

```
Project-PBO-KERKOM/
├── todo_app.py                    # Aplikasi utama ⭐
├── requirements.txt               # Dependencies ⭐
├── README.md                      # Panduan ini ⭐
├── .gitignore                     # File ignored ⭐
├── PRESENTASI_OUTLINE.md          # Slide presentation
├── OOP_IMPLEMENTASI.md            # Penjelasan OOP
├── PENJELASAN_PER_BARIS.md        # Tips presentasi
├── UML_PENJELASAN_SINGKAT.md      # Diagram UML
└── tasks.json                     # Data (auto-created) 📊
```

⭐ = File WAJIB agar aplikasi jalan
📊 = File auto-created saat pertama kali run

## 🚀 Upload ke GitHub (Step-by-Step)

### 1. Buat Repository Baru di GitHub
- Go to [github.com/new](https://github.com/new)
- Repository name: `Project-PBO-KERKOM`
- Description: "Aplikasi To-Do List dengan OOP - PBO Semester 3"
- Public (agar dosen bisa akses)
- **Jangan** centang "Initialize with README" (sudah punya)
- Click "Create repository"

### 2. Upload File ke GitHub via Git
```bash
# Navigate ke folder project
cd "c:\Users\lenovo\Documents\Project PBO KERKOM"

# Initialize git (jika belum ada)
git init

# Add semua file
git add .

# Commit
git commit -m "Initial commit: Todo app dengan OOP implementation"

# Set remote URL (ganti USERNAME dengan username GitHub)
git remote add origin https://github.com/USERNAME/Project-PBO-KERKOM.git

# Push ke GitHub
git branch -M main
git push -u origin main
```

### 3. Alternatif: Upload via GitHub Web
Jika tidak familiar dengan Git command:
1. Go to repository yang sudah dibuat
2. Click "Add file" → "Upload files"
3. Drag-drop atau select file ini:
   - `todo_app.py` ⭐
   - `requirements.txt` ⭐
   - `README.md` ⭐
   - `.gitignore` ⭐
   - `PRESENTASI_OUTLINE.md`
   - `OOP_IMPLEMENTASI.md`
   - `PENJELASAN_PER_BARIS.md`
   - `UML_PENJELASAN_SINGKAT.md`
4. Write commit message: "Initial commit: Todo app dengan OOP"
5. Click "Commit changes"

## ✅ Checklist Sebelum Push ke GitHub

- [ ] Semua file ⭐ sudah ada
- [ ] `requirements.txt` mencantumkan `tkcalendar`
- [ ] `README.md` dengan instruksi setup lengkap
- [ ] `.gitignore` untuk exclude `__pycache__`
- [ ] `tasks.json` sudah di-create (atau akan auto-create saat pertama run)
- [ ] `todo_app.py` bisa dijalankan: `python todo_app.py`
- [ ] Tidak ada file `.pyc` atau `__pycache__` yang terupload

## 📝 Testing Sebelum Dosen Jalankan

### Di Komputer Anda (Sebelum Push):
```bash
# 1. Bersihkan environment
rm -r __pycache__
rm -r .pytest_cache

# 2. Hapus dan test fresh install
pip uninstall tkcalendar -y
pip install -r requirements.txt

# 3. Jalankan aplikasi
python todo_app.py
```

Pastikan aplikasi jalan tanpa error.

### Di Komputer Dosen (Setelah Clone):
```bash
# 1. Clone repository
git clone https://github.com/[username]/Project-PBO-KERKOM.git
cd Project-PBO-KERKOM

# 2. Install dependencies
pip install -r requirements.txt

# 3. Jalankan aplikasi
python todo_app.py
```

Seharusnya aplikasi langsung jalan dengan sempurna! 🎉

## 🔧 Troubleshooting

### Error: "No module named 'tkcalendar'"
```bash
pip install tkcalendar==1.6.1
```

### Error: "No module named 'tkinter'"
**Windows:** Re-install Python dan centang "tcl/tk and IDLE" option
**Linux:** `sudo apt-get install python3-tk`
**Mac:** `brew install python-tk`

### Aplikasi jalan tapi tidak ada data sebelumnya
Normal! `tasks.json` akan auto-create saat pertama kali run.

### File `tasks.json` tidak appear
File akan dibuat otomatis saat Anda menambah task pertama kali.

## 📊 Informasi Presentasi

File ini adalah project untuk presentasi PBO Semester 3:
- **Durasi:** 7-10 menit
- **Penjelasan OOP:** See [OOP_IMPLEMENTASI.md](OOP_IMPLEMENTASI.md)
- **Slide Outline:** See [PRESENTASI_OUTLINE.md](PRESENTASI_OUTLINE.md)
- **Tips Presentasi:** See [PENJELASAN_PER_BARIS.md](PENJELASAN_PER_BARIS.md)

## 📚 Konsep OOP yang Diimplementasikan

✅ **Abstraksi** - Interface `ITask` mendefinisikan kontrak
✅ **Enkapsulasi** - Private attributes + properties dengan getter/setter
✅ **Pewarisan** - `DeadlineTask` mewarisi dari `Task`
✅ **Polimorfisme** - Override method di subclass
✅ **Komposisi** - `TaskManager` dan `Category` mengelola kumpulan `Task`
✅ **MVC Pattern** - Pemisahan Model, View, Controller yang jelas
✅ **SOLID Principles** - Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion

## 🎓 Pembelajaran dari Project Ini

Melalui project ini, Anda belajar:
- 🏗️ Design pattern & software architecture
- 🔐 Data encapsulation & abstraction
- 📦 Inheritance hierarchy & polymorphism
- 💾 Data persistence dengan JSON
- 🎨 GUI development dengan Tkinter
- 🧪 Code organization & documentation
- 📋 Professional software development practices

## 📞 Pertanyaan?

Jika ada error atau pertanyaan saat setup:
1. Cek file `README.md` ini (Troubleshooting section)
2. Cek file dokumentasi OOP: [OOP_IMPLEMENTASI.md](OOP_IMPLEMENTASI.md)
3. Review presentation outline: [PRESENTASI_OUTLINE.md](PRESENTASI_OUTLINE.md)

---

**Happy Learning! 🚀**

*Project ini dibuat sebagai assignment Pemrograman Berorientasi Objek (PBO) Semester 3.*
