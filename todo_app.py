import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Optional
from tkcalendar import Calendar

# =======================
# INTERFACE & ABSTRACT CLASS
# =======================

class ITask(ABC):
    """Interface untuk semua tipe task dengan kontrak method."""
    
    @abstractmethod
    def get_details(self) -> str:
        """Mendapatkan deskripsi task."""
        pass

    @abstractmethod
    def toggle_status(self):
        """Mengubah status task."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Mengkonversi task ke bentuk dictionary."""
        pass


# =======================
# MODEL - TASK & SUBTYPES
# =======================

class Task(ITask):
    """
    Kelas Task sebagai base class untuk semua jenis task.
    Mengimplementasikan interface ITask dengan properties yang dienkapsulasi.
    """
    
    def __init__(self, task_id: int, title: str, description: str, category: str = "Umum"):
        """
        Inisialisasi task baru.
        
        Args:
            task_id: Unique identifier untuk task
            title: Judul task
            description: Deskripsi detail task
            category: Kategori task (default: "Umum")
        """
        self._id = task_id
        self._title = title
        self._description = description
        self._category = category
        self._completed = False
        self._created_date = datetime.now().strftime("%Y-%m-%d")

    @property
    def task_id(self) -> int:
        return self._id

    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, value: str):
        self._title = value

    @property
    def description(self) -> str:
        return self._description
    
    @description.setter
    def description(self, value: str):
        self._description = value

    @property
    def category(self) -> str:
        return self._category
    
    @category.setter
    def category(self, value: str):
        self._category = value

    @property
    def created_date(self) -> str:
        return self._created_date

    def toggle_status(self):
        """Toggle status task antara completed dan pending."""
        self._completed = not self._completed

    def is_completed(self) -> bool:
        """Mengecek apakah task sudah selesai."""
        return self._completed

    def get_details(self) -> str:
        """Mendapatkan detail task."""
        return f"{self._title} ({self._category})"

    def to_dict(self) -> dict:
        """Mengkonversi task ke dictionary untuk disimpan ke file."""
        return {
            "id": self._id,
            "title": self._title,
            "description": self._description,
            "category": self._category,
            "completed": self._completed,
            "created_date": self._created_date,
            "type": "Task"
        }


class DeadlineTask(Task):
    """
    Subclass Task untuk task dengan deadline.
    Inheritance dari Task base class.
    """
    
    def __init__(self, task_id: int, title: str, description: str, deadline: str, category: str = "Umum"):
        """
        Inisialisasi DeadlineTask.
        
        Args:
            task_id: Unique identifier
            title: Judul task
            description: Deskripsi task
            deadline: Deadline task (format: YYYY-MM-DD)
            category: Kategori task
        """
        super().__init__(task_id, title, description, category)
        self._deadline = deadline

    @property
    def deadline(self) -> str:
        return self._deadline
    
    @deadline.setter
    def deadline(self, value: str):
        self._deadline = value

    def get_details(self) -> str:
        """Override: tampilkan dengan deadline."""
        status = "✓" if self._completed else "✗"
        return f"[{status}] {self._title} | Deadline: {self._deadline}"

    def to_dict(self) -> dict:
        """Override: tambahkan deadline ke dictionary."""
        data = super().to_dict()
        data["deadline"] = self._deadline
        data["type"] = "DeadlineTask"
        return data


# =======================
# MODEL - CATEGORY
# =======================

class Category:
    """
    Kelas untuk merepresentasikan kategori task.
    Menyediakan struktur untuk mengorganisir task berdasarkan kategori.
    """
    
    def __init__(self, name: str):
        """
        Inisialisasi kategori.
        
        Args:
            name: Nama kategori
        """
        self._name = name
        self._tasks: List[Task] = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def tasks(self) -> List[Task]:
        return self._tasks

    def add_task(self, task: Task):
        """Menambah task ke kategori."""
        if task not in self._tasks:
            self._tasks.append(task)

    def remove_task(self, task: Task):
        """Menghapus task dari kategori."""
        if task in self._tasks:
            self._tasks.remove(task)


# =======================
# CONTROLLER - TASK MANAGER
# =======================

class TaskManager:
    """
    Manager untuk mengelola semua task.
    Bertanggung jawab untuk:
    - Penyimpanan dan pemuatan data task
    - Operasi CRUD pada task
    - Persistensi data ke file JSON
    """
    
    def __init__(self, file_path: str = "tasks.json"):
        """
        Inisialisasi task manager.
        
        Args:
            file_path: Path untuk file penyimpanan tasks (default: tasks.json)
        """
        self._file_path = file_path
        self._tasks: List[Task] = []
        self.load_tasks()

    @property
    def tasks(self) -> List[Task]:
        """Mendapatkan list semua tasks."""
        return self._tasks

    def add_task(self, task: Task):
        """Menambah task baru ke manager."""
        self._tasks.append(task)
        self.save_tasks()

    def delete_task(self, index: int):
        """Menghapus task berdasarkan index."""
        if 0 <= index < len(self._tasks):
            self._tasks.pop(index)
            self.save_tasks()

    def toggle_task(self, index: int):
        """Mengubah status task berdasarkan index."""
        if 0 <= index < len(self._tasks):
            self._tasks[index].toggle_status()
            self.save_tasks()

    def save_tasks(self):
        """Simpan semua tasks ke file JSON."""
        try:
            with open(self._file_path, "w") as f:
                json.dump([t.to_dict() for t in self._tasks], f, indent=4)
        except IOError as e:
            print(f"Error saat menyimpan tasks: {e}")

    def load_tasks(self):
        """Load task dari file JSON."""
        try:
            with open(self._file_path, "r") as f:
                data = json.load(f)
                for item in data:
                    task = DeadlineTask(
                        item["id"], 
                        item["title"], 
                        item["description"],
                        item.get("deadline", ""), 
                        item.get("category", "Umum")
                    )
                    
                    task._completed = item.get("completed", False)
                    self._tasks.append(task)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError as e:
            print(f"Error membaca file task: {e}")


# =======================
# VIEW - TODO APP GUI
# =======================

class TodoApp:
    """
    Aplikasi To-Do List dengan GUI menggunakan Tkinter.
    Menerapkan MVC pattern dengan TaskManager sebagai model.
    """
    
    # Modern Color Palette
    COLOR_PRIMARY = "#6366F1"      # Indigo
    COLOR_SECONDARY = "#8B5CF6"    # Purple
    COLOR_SUCCESS = "#10B981"      # Green
    COLOR_WARNING = "#F59E0B"      # Amber
    COLOR_DANGER = "#EF4444"       # Red
    COLOR_BG = "#F9FAFB"           # Light Gray
    COLOR_PANEL = "#FFFFFF"        # White
    COLOR_TEXT = "#1F2937"         # Dark Gray
    COLOR_MUTED = "#6B7280"        # Gray
    COLOR_BORDER = "#E5E7EB"       # Light Border
    CATEGORIES = ["Umum", "Kuliah", "Kerja", "Pribadi"]

    def __init__(self, root: tk.Tk):
        """
        Inisialisasi aplikasi GUI.
        
        Args:
            root: Tkinter root window
        """
        self._root = root
        self._root.title("✨ My Todo List - PBO Edition")
        self._root.geometry("1000x650")
        self._root.configure(bg=self.COLOR_BG)
        self.manager = TaskManager()

        # Setup styles
        self._setup_styles()

        # Setup main layout
        main_frame = ttk.Frame(self._root, padding=12)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        self._setup_header(main_frame)

        # Content area
        content = ttk.Frame(main_frame, padding=8)
        content.pack(fill=tk.BOTH, expand=True)

        # Input section
        self._setup_input_section(content)

        # Search bar
        self._setup_search_section(content)

        # List section
        self._setup_list_section(content)

        # Buttons section
        self._setup_buttons_section(content)

        # Status bar
        self._setup_status_bar()

        # Keybindings
        self._setup_keybindings()

    def _setup_styles(self):
        """Setup ttk styles dengan modern design."""
        style = ttk.Style()
        style.theme_use('clam')  # Modern theme base
        
        # Button styles
        style.configure('Primary.TButton', 
                       padding=10,
                       relief='flat',
                       background=self.COLOR_PRIMARY,
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Segoe UI', 10, 'bold'))
        style.map('Primary.TButton',
                 background=[('active', self.COLOR_SECONDARY)])
        
        style.configure('Success.TButton', 
                       padding=8,
                       relief='flat',
                       background=self.COLOR_SUCCESS,
                       foreground='white',
                       font=('Segoe UI', 9, 'bold'))
        style.map('Success.TButton',
                 background=[('active', '#059669')])
        
        style.configure('Danger.TButton', 
                       padding=8,
                       relief='flat',
                       background=self.COLOR_DANGER,
                       foreground='white',
                       font=('Segoe UI', 9, 'bold'))
        style.map('Danger.TButton',
                 background=[('active', '#DC2626')])
        
        style.configure('Warning.TButton', 
                       padding=8,
                       relief='flat',
                       background=self.COLOR_WARNING,
                       foreground='white',
                       font=('Segoe UI', 9, 'bold'))
        style.map('Warning.TButton',
                 background=[('active', '#D97706')])
        
        # Frame styles
        style.configure('Card.TFrame', background=self.COLOR_PANEL, relief='flat')
        style.configure('TFrame', background=self.COLOR_BG)
        
        # LabelFrame styles
        style.configure('Card.TLabelframe', 
                       background=self.COLOR_PANEL,
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.COLOR_BORDER)
        style.configure('Card.TLabelframe.Label', 
                       background=self.COLOR_PANEL,
                       foreground=self.COLOR_PRIMARY,
                       font=('Segoe UI', 11, 'bold'))
        
        # Treeview styles
        style.configure('Treeview', 
                       rowheight=32, 
                       font=('Segoe UI', 10),
                       background=self.COLOR_PANEL,
                       fieldbackground=self.COLOR_PANEL,
                       foreground=self.COLOR_TEXT,
                       borderwidth=0)
        style.configure('Treeview.Heading',
                       font=('Segoe UI', 10, 'bold'),
                       background=self.COLOR_PRIMARY,
                       foreground='white',
                       relief='flat',
                       borderwidth=0)
        style.map('Treeview.Heading',
                 background=[('active', self.COLOR_SECONDARY)])
        style.map('Treeview',
                 background=[('selected', self.COLOR_PRIMARY)],
                 foreground=[('selected', 'white')])
        
        # Label styles
        style.configure('TLabel', background=self.COLOR_PANEL, foreground=self.COLOR_TEXT)
        
        # Combobox styles
        style.configure('TCombobox', 
                       fieldbackground='white',
                       background=self.COLOR_PRIMARY,
                       borderwidth=1,
                       relief='solid')

    def _setup_header(self, parent):
        """Setup header section dengan gradient effect."""
        header = tk.Canvas(parent, height=80, bd=0, highlightthickness=0)
        header.pack(fill=tk.X, pady=(0, 15))
        
        # Gradient background (simulated dengan multiple rectangles)
        gradient_colors = ['#6366F1', '#7C3AED', '#8B5CF6', '#9333EA']
        width = 1000
        for i, color in enumerate(gradient_colors):
            x1 = (i * width) // len(gradient_colors)
            x2 = ((i + 1) * width) // len(gradient_colors)
            header.create_rectangle(x1, 0, x2, 80, fill=color, outline='')
        
        # Title dengan shadow effect
        header.create_text(22, 27, text="✨ MY TODO LIST", anchor='w', 
                          fill='#1F2937', font=("Segoe UI", 20, "bold"))
        header.create_text(20, 25, text="✨ MY TODO LIST", anchor='w', 
                          fill='white', font=("Segoe UI", 20, "bold"))
        
        # Subtitle
        header.create_text(20, 55, text="📚 Kelola tugas dengan lebih terorganisir", anchor='w',
                          fill='#E0E7FF', font=("Segoe UI", 10))

    def _setup_input_section(self, parent):
        """Setup input section untuk menambah task."""
        input_frame = ttk.LabelFrame(parent, text="➕ Tambah Task Baru", padding=15, style='Card.TLabelframe')
        input_frame.pack(fill=tk.X, pady=10)

        # Title
        ttk.Label(input_frame, text="📌 Judul:", font=('Segoe UI', 9, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=6, pady=6)
        self._title_entry = tk.Entry(input_frame, font=("Segoe UI", 10), width=30,
                                     relief='solid', borderwidth=1,
                                     highlightthickness=2, highlightbackground=self.COLOR_BORDER,
                                     highlightcolor=self.COLOR_PRIMARY)
        self._title_entry.grid(row=0, column=1, columnspan=3, sticky=tk.EW, padx=6, pady=6)

        # Description
        ttk.Label(input_frame, text="📝 Deskripsi:", font=('Segoe UI', 9, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=6, pady=6)
        self._desc_entry = tk.Entry(input_frame, font=("Segoe UI", 10), width=30,
                                    relief='solid', borderwidth=1,
                                    highlightthickness=2, highlightbackground=self.COLOR_BORDER,
                                    highlightcolor=self.COLOR_PRIMARY)
        self._desc_entry.grid(row=1, column=1, columnspan=3, sticky=tk.EW, padx=6, pady=6)

        # Category
        ttk.Label(input_frame, text="🏷️ Kategori:", font=('Segoe UI', 9, 'bold')).grid(row=0, column=4, sticky=tk.W, padx=6, pady=6)
        self._category_cb = ttk.Combobox(input_frame, values=self.CATEGORIES, 
                                         state="readonly", width=14,
                                         font=('Segoe UI', 10))
        self._category_cb.current(0)
        self._category_cb.grid(row=0, column=5, sticky=tk.EW, padx=6, pady=6)

        # Deadline
        ttk.Label(input_frame, text="📅 Deadline:", font=('Segoe UI', 9, 'bold')).grid(row=2, column=0, sticky=tk.W, padx=6, pady=6)
        
        deadline_frame = tk.Frame(input_frame, bg=self.COLOR_PANEL)
        deadline_frame.grid(row=2, column=1, sticky=tk.EW, padx=6, pady=6)
        
        self._deadline_entry = tk.Entry(deadline_frame, font=("Segoe UI", 10), width=12,
                                        relief='solid', borderwidth=1,
                                        highlightthickness=2, highlightbackground=self.COLOR_BORDER,
                                        highlightcolor=self.COLOR_PRIMARY)
        self._deadline_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Tombol Calendar
        btn_calendar = tk.Button(deadline_frame, text="📆", 
                                command=self._show_calendar,
                                bg=self.COLOR_PRIMARY, fg='white',
                                font=('Segoe UI', 10, 'bold'),
                                relief='flat', borderwidth=0,
                                padx=10, pady=5,
                                cursor='hand2',
                                activebackground=self.COLOR_SECONDARY)
        btn_calendar.pack(side=tk.LEFT, padx=5)
        
        # Deadline hint
        ttk.Label(input_frame, text="(DD-MM-YYYY atau klik 📆)", 
                 font=('Segoe UI', 8), foreground=self.COLOR_MUTED).grid(row=2, column=2, sticky=tk.W, padx=2)

        # Add button
        self._add_btn = ttk.Button(input_frame, text="➕ Tambah Task", 
                                  command=self._add_task, style='Primary.TButton')
        self._add_btn.grid(row=3, column=1, columnspan=4, sticky=tk.E, pady=10, padx=6)

        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(5, weight=1)

    def _setup_search_section(self, parent):
        """Setup search section."""
        search_frame = ttk.Frame(parent, style='Card.TFrame')
        search_frame.pack(fill=tk.X, pady=8)
        
        ttk.Label(search_frame, text="🔍 Cari:", font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=8)
        self._search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=self._search_var,
                               font=('Segoe UI', 10), relief='solid', borderwidth=1,
                               highlightthickness=2, highlightbackground=self.COLOR_BORDER,
                               highlightcolor=self.COLOR_PRIMARY)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=8, pady=8)
        self._search_var.trace_add("write", lambda *_: self._refresh_list())
        
        # Tombol aksi di samping search
        # Button Tandai Selesai (Hijau)
        btn_complete = tk.Button(search_frame, text="✓ Selesai", 
                                command=self._toggle_task,
                                bg=self.COLOR_SUCCESS, fg='white',
                                font=('Segoe UI', 9, 'bold'),
                                relief='raised', borderwidth=1,
                                padx=12, pady=8,
                                cursor='hand2',
                                activebackground='#059669')
        btn_complete.pack(side=tk.LEFT, padx=4)
        
        # Button Edit (Kuning)
        btn_edit = tk.Button(search_frame, text="✎ Edit", 
                           command=self._edit_task,
                           bg=self.COLOR_WARNING, fg='white',
                           font=('Segoe UI', 9, 'bold'),
                           relief='raised', borderwidth=1,
                           padx=12, pady=8,
                           cursor='hand2',
                           activebackground='#D97706')
        btn_edit.pack(side=tk.LEFT, padx=4)
        
        # Button Hapus (Merah)
        btn_delete = tk.Button(search_frame, text="✕ Hapus", 
                             command=self._delete_task,
                             bg=self.COLOR_DANGER, fg='white',
                             font=('Segoe UI', 9, 'bold'),
                             relief='raised', borderwidth=1,
                             padx=12, pady=8,
                             cursor='hand2',
                             activebackground='#DC2626')
        btn_delete.pack(side=tk.LEFT, padx=4)

    def _setup_list_section(self, parent):
        """Setup task list section."""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview columns
        columns = ("#", "Judul", "Kategori", "Deadline", "Status")
        self._tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # Setup column headings
        self._tree.heading("#", text="#")
        self._tree.column("#", width=40, anchor='center')
        self._tree.heading("Judul", text="Judul")
        self._tree.column("Judul", anchor='w')
        self._tree.heading("Kategori", text="Kategori")
        self._tree.column("Kategori", width=100, anchor='center')
        self._tree.heading("Deadline", text="Deadline")
        self._tree.column("Deadline", width=120, anchor='center')
        self._tree.heading("Status", text="Status")
        self._tree.column("Status", width=100, anchor='center')

        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scrollbar.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Tags untuk styling
        self._tree.tag_configure('completed', foreground='#9CA3AF', background='#F3F4F6', font=('Segoe UI', 10, 'overstrike'))
        self._tree.tag_configure('pending', background='#FFFFFF')
        self._tree.tag_configure('urgent', foreground=self.COLOR_DANGER, font=('Segoe UI', 10, 'bold'))

    def _setup_buttons_section(self, parent):
        """Setup action buttons."""
        btn_frame = tk.Frame(parent, bg=self.COLOR_BG)
        btn_frame.pack(fill=tk.X, pady=15, padx=10, anchor='w')
        
        # Button Tandai Selesai (Hijau)
        btn_complete = tk.Button(btn_frame, text="✓ TANDAI SELESAI", 
                                command=self._toggle_task,
                                bg=self.COLOR_SUCCESS, fg='white',
                                font=('Segoe UI', 10, 'bold'),
                                relief='raised', borderwidth=2,
                                padx=20, pady=12,
                                width=18,
                                cursor='hand2',
                                activebackground='#059669',
                                activeforeground='white')
        btn_complete.pack(side=tk.LEFT, padx=8)
        
        # Button Edit (Kuning)
        btn_edit = tk.Button(btn_frame, text="✎ EDIT TASK", 
                           command=self._edit_task,
                           bg=self.COLOR_WARNING, fg='white',
                           font=('Segoe UI', 10, 'bold'),
                           relief='raised', borderwidth=2,
                           padx=20, pady=12,
                           width=18,
                           cursor='hand2',
                           activebackground='#D97706',
                           activeforeground='white')
        btn_edit.pack(side=tk.LEFT, padx=8)
        
        # Button Hapus (Merah) - PALING JELAS
        btn_delete = tk.Button(btn_frame, text="✕ HAPUS TASK", 
                             command=self._delete_task,
                             bg=self.COLOR_DANGER, fg='white',
                             font=('Segoe UI', 10, 'bold'),
                             relief='raised', borderwidth=2,
                             padx=20, pady=12,
                             width=18,
                             cursor='hand2',
                             activebackground='#DC2626',
                             activeforeground='white')
        btn_delete.pack(side=tk.LEFT, padx=8)

    def _setup_status_bar(self):
        """Setup status bar with progress."""
        status_frame = tk.Frame(self._root, bg=self.COLOR_PRIMARY, height=50)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self._status_var = tk.StringVar()
        status_bar = tk.Label(status_frame, textvariable=self._status_var, 
                             anchor=tk.W, bg=self.COLOR_PRIMARY, fg='white',
                             font=('Segoe UI', 10, 'bold'), padx=15, pady=10)
        status_bar.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Style untuk progressbar
        style = ttk.Style()
        style.configure('Custom.Horizontal.TProgressbar',
                       troughcolor=self.COLOR_SECONDARY,
                       background=self.COLOR_SUCCESS,
                       borderwidth=0,
                       thickness=20)
        
        self._progress = ttk.Progressbar(status_frame, mode='determinate', 
                                        length=200, style='Custom.Horizontal.TProgressbar')
        self._progress.pack(side=tk.RIGHT, padx=15, pady=10)

    def _setup_keybindings(self):
        """Setup keyboard shortcuts."""
        self._root.bind("<Control-n>", lambda e: self._title_entry.focus_set())
        self._root.bind("<Delete>", lambda e: self._delete_task())

    def _show_calendar(self):
        """Tampilkan calendar popup untuk memilih deadline."""
        # Create calendar window
        cal_window = tk.Toplevel(self._root)
        cal_window.title("Pilih Deadline")
        cal_window.resizable(False, False)
        cal_window.grab_set()
        
        # Create calendar widget dengan format DD-MM-YYYY
        cal = Calendar(cal_window, selectmode='day', year=datetime.now().year, 
                       month=datetime.now().month, date_pattern='dd-mm-yyyy')
        cal.pack(padx=10, pady=10)
        
        def on_select():
            """Ketika tanggal dipilih, isi ke entry field."""
            selected_date = cal.get_date()
            self._deadline_entry.delete(0, tk.END)
            self._deadline_entry.insert(0, selected_date)
            cal_window.destroy()
        
        # Button OK
        btn_ok = tk.Button(cal_window, text="✓ Pilih", 
                          command=on_select,
                          bg=self.COLOR_SUCCESS, fg='white',
                          font=('Segoe UI', 10, 'bold'),
                          relief='flat', borderwidth=0,
                          padx=20, pady=8,
                          cursor='hand2',
                          activebackground='#059669')
        btn_ok.pack(pady=10)

    def _add_task(self):
        """Handler untuk menambah task."""
        title = self._title_entry.get().strip()
        description = self._desc_entry.get().strip()
        category = self._category_cb.get()
        deadline = self._deadline_entry.get().strip()

        if not title:
            messagebox.showwarning("Input Error", "Judul task tidak boleh kosong!")
            return

        if not deadline:
            messagebox.showwarning("Input Error", "Deadline tidak boleh kosong!")
            return

        try:
            datetime.strptime(deadline, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Format Error", "Format deadline harus DD-MM-YYYY\nContoh: 25-12-2026")
            return

        try:
            task_id = max([t.task_id for t in self.manager._tasks], default=0) + 1
            task = DeadlineTask(task_id, title, description, deadline, category)
            
            self.manager.add_task(task)
            self._clear_inputs()
            self._refresh_list()
            messagebox.showinfo("Success", f"Task '{title}' berhasil ditambahkan!")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambah task: {str(e)}")

    def _edit_task(self):
        """Handler untuk mengedit task."""
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Pilih task untuk diedit")
            return
        
        index = int(sel[0])
        task = self.manager.tasks[index]
        
        # Create edit dialog
        dlg = tk.Toplevel(self._root)
        dlg.title(f"Edit Task - {task.title}")
        dlg.resizable(False, False)
        dlg.grab_set()

        ttk.Label(dlg, text="Judul:").grid(row=0, column=0, sticky=tk.W, padx=8, pady=8)
        title_entry = tk.Entry(dlg, font=("Segoe UI", 10), width=40)
        title_entry.insert(0, task.title)
        title_entry.grid(row=0, column=1, padx=8, pady=8)

        ttk.Label(dlg, text="Deskripsi:").grid(row=1, column=0, sticky=tk.W, padx=8, pady=8)
        desc_entry = tk.Entry(dlg, font=("Segoe UI", 10), width=40)
        desc_entry.insert(0, task.description)
        desc_entry.grid(row=1, column=1, padx=8, pady=8)

        ttk.Label(dlg, text="Deadline:").grid(row=2, column=0, sticky=tk.W, padx=8, pady=8)
        deadline_entry = tk.Entry(dlg, font=("Segoe UI", 10), width=40)
        deadline_entry.insert(0, task.deadline)
        deadline_entry.grid(row=2, column=1, padx=8, pady=8)

        def save_changes():
            task._title = title_entry.get().strip()
            task._description = desc_entry.get().strip()
            task._deadline = deadline_entry.get().strip()
            
            self.manager.save_tasks()
            self._refresh_list()
            dlg.destroy()
            messagebox.showinfo("Sukses", "Task berhasil diupdate!")

        ttk.Button(dlg, text="💾 Simpan", command=save_changes).grid(row=3, column=1, sticky=tk.E, padx=8, pady=12)

    def _toggle_task(self):
        """Handler untuk toggle status task."""
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Pilih task terlebih dahulu")
            return
        
        index = int(sel[0])
        self.manager.toggle_task(index)
        self._refresh_list()

    def _delete_task(self):
        """Handler untuk delete task."""
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Info", "Pilih task untuk dihapus")
            return
        
        index = int(sel[0])
        task = self.manager.tasks[index]
        
        if messagebox.askyesno("Konfirmasi", f"Hapus task: {task.title}?"):
            self.manager.delete_task(index)
            self._refresh_list()

    def _clear_inputs(self):
        """Clear input fields."""
        self._title_entry.delete(0, tk.END)
        self._desc_entry.delete(0, tk.END)
        self._deadline_entry.delete(0, tk.END)
        self._category_cb.current(0)

    def _refresh_list(self):
        """Refresh task list display."""
        # Clear tree
        for item in self._tree.get_children():
            self._tree.delete(item)

        query = self._search_var.get().strip().lower()

        # Populate tree
        for idx, task in enumerate(self.manager.tasks):
            # Apply search filter
            combined_text = f"{task.title} {task.description} {task.category}".lower()
            if query and query not in combined_text:
                continue

            # Status dengan emoji yang lebih menarik
            if task.is_completed():
                status_text = "✅ Selesai"
                tags = ('completed',)
            else:
                # Check if urgent (deadline soon)
                try:
                    deadline_date = datetime.strptime(task.deadline, "%d-%m-%Y")
                    days_left = (deadline_date - datetime.now()).days
                    if days_left < 3:
                        status_text = "🔥 Mendesak!"
                        tags = ('urgent',)
                    else:
                        status_text = "⏳ Tertunda"
                        tags = ('pending',)
                except:
                    status_text = "⏳ Tertunda"
                    tags = ('pending',)

            self._tree.insert('', tk.END, iid=str(idx), 
                            values=(idx + 1, task.title, task.category, task.deadline, status_text),
                            tags=tags)

        # Update progress dengan emoji
        total = len(self.manager.tasks)
        done = sum(1 for t in self.manager.tasks if t.is_completed())
        pending = total - done
        percentage = int((done / total * 100)) if total > 0 else 0

        self._status_var.set(f"📊 Total: {total}  •  ✅ Selesai: {done}  •  ⏳ Tertunda: {pending}  •  📈 Progress: {percentage}%")
        if total > 0:
            self._progress['maximum'] = total
            self._progress['value'] = done
        else:
            self._progress['value'] = 0


# =======================
# MAIN
# =======================

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
