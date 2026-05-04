import random
import string
import json
import os
from tkinter import *
from tkinter import ttk, messagebox

# Файл для хранения истории
HISTORY_FILE = "password_history.json"

class PasswordGenerator:
def __init__(self, root):
self.root = root
self.root.title("Random Password Generator")
self.root.geometry("700x500")
self.root.resizable(False, False)

# Переменные
self.password_length = IntVar(value=12)
self.use_digits = BooleanVar(value=True)
self.use_letters = BooleanVar(value=True)
self.use_symbols = BooleanVar(value=True)
self.history = self.load_history()

# Интерфейс
self.create_widgets()
self.update_history_table()

def create_widgets(self):
# Рамка настроек
settings_frame = LabelFrame(self.root, text="Настройки пароля", padx=10, pady=10)
settings_frame.pack(fill="x", padx=10, pady=10)

# Ползунок длины
Label(settings_frame, text="Длина пароля:").grid(row=0, column=0, sticky="w")
self.length_slider = Scale(settings_frame, from_=4, to=32, orient=HORIZONTAL,
variable=self.password_length, length=300)
self.length_slider.grid(row=0, column=1, padx=10)
self.length_label = Label(settings_frame, text="12")
self.length_label.grid(row=0, column=2)
self.length_slider.config(command=lambda x: self.length_label.config(text=str(int(float(x)))))

# Чекбоксы
Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).grid(row=1, column=0, sticky="w")
Checkbutton(settings_frame, text="Буквы (A-Z a-z)", variable=self.use_letters).grid(row=2, column=0, sticky="w")
Checkbutton(settings_frame, text="Спецсимволы (!@#$%^&*)", variable=self.use_symbols).grid(row=3, column=0, sticky="w")

# Кнопка генерации
self.generate_btn = Button(settings_frame, text="Сгенерировать пароль", command=self.generate_password,
bg="green", fg="white", font=("Arial", 10, "bold"))
self.generate_btn.grid(row=4, column=0, columnspan=3, pady=10)

# Поле для отображения пароля
self.password_var = StringVar()
self.password_entry = Entry(self.root, textvariable=self.password_var, font=("Courier", 14), state="readonly",
justify="center")
self.password_entry.pack(fill="x", padx=10, pady=5)

# Копирование в буфер
self.copy_btn = Button(self.root, text="Копировать в буфер", command=self.copy_to_clipboard)
self.copy_btn.pack(pady=5)

# Таблица истории
history_frame = LabelFrame(self.root, text="История паролей", padx=10, pady=10)
history_frame.pack(fill="both", expand=True, padx=10, pady=10)

self.tree = ttk.Treeview(history_frame, columns=("Password", "Length", "Charset"), show="headings")
self.tree.heading("Password", text="Пароль")
self.tree.heading("Length", text="Длина")
self.tree.heading("Charset", text="Использованные символы")
self.tree.column("Password", width=250)
self.tree.column("Length", width=80)
self.tree.column("Charset", width=250)
self.tree.pack(fill="both", expand=True)

# Кнопки управления историей
btn_frame = Frame(history_frame)
btn_frame.pack(fill="x", pady=5)

Button(btn_frame, text="Очистить историю", command=self.clear_history).pack(side="left", padx=5)
Button(btn_frame, text="Удалить выбранный", command=self.delete_selected).pack(side="left", padx=5)

def generate_password(self):
length = self.password_length.get()
if length < 4:
messagebox.showerror("Ошибка", "Минимальная длина пароля — 4 символа")
return
if length > 32:
messagebox.showerror("Ошибка", "Максимальная длина пароля — 32 символа")
return

if not (self.use_digits.get() or self.use_letters.get() or self.use_symbols.get()):
messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
return

chars = ""
charset_desc = ""
if self.use_digits.get():
chars += string.digits
charset_desc += "цифры "
if self.use_letters.get():
chars += string.ascii_letters
charset_desc += "буквы "
if self.use_symbols.get():
chars += "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"
charset_desc += "спецсимволы"

password = ''.join(random.choice(chars) for _ in range(length))
self.password_var.set(password)

# Сохраняем в историю
self.history.append({
"password": password,
"length": length,
"charset": charset_desc.strip()
})
self.save_history()
self.update_history_table()

def copy_to_clipboard(self):
pwd = self.password_var.get()
if pwd:
self.root.clipboard_clear()
self.root.clipboard_append(pwd)
messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена")
else:
messagebox.showwarning("Внимание", "Нет сгенерированного пароля")

def load_history(self):
if os.path.exists(HISTORY_FILE):
with open(HISTORY_FILE, "r", encoding="utf-8") as f:
try:
return json.load(f)
except:
return []
return []

def save_history(self):
with open(HISTORY_FILE, "w", encoding="utf-8") as f:
json.dump(self.history, f, ensure_ascii=False, indent=2)

def update_history_table(self):
for row in self.tree.get_children():
self.tree.delete(row)
for entry in self.history:
self.tree.insert("", END, values=(entry["password"], entry["length"], entry["charset"]))

def clear_history(self):
if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
self.history = []
self.save_history()
self.update_history_table()

def delete_selected(self):
selected = self.tree.selection()
if not selected:
messagebox.showwarning("Внимание", "Выберите запись для удаления")
return
index = self.tree.index(selected[0])
del self.history[index]
self.save_history()
self.update_history_table()

if __name__ == "__main__":
root = Tk()
app = PasswordGenerator(root)
root.mainloop()
