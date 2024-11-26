import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta


class MedicineTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Напоминалка о лекарствах")
        root.configure(bg="light sky blue")

        self.medicines = []

        # Название лекарства
        self.label_name = tk.Label(root, text="Введите название лекарства:",bg="light sky blue")
        self.label_name.pack()
        self.entry_name = tk.Entry(root, width=30, bg="snow3", fg="black")
        self.entry_name.pack()

        # Время приема
        self.label_time = tk.Label(root, text="Время приема (HH:MM):",bg="light sky blue")
        self.label_time.pack()
        self.entry_time = tk.Entry(root, bg="snow3", fg="black")
        self.entry_time.pack()

        # Частота
        self.label_frequency = tk.Label(root, text="Сколько раз в сутки:",bg="light sky blue")
        self.label_frequency.pack()
        self.entry_frequency = tk.Entry(root, bg="snow3", fg="black")
        self.entry_frequency.pack()

        # Количество за раз
        self.label_quantity= tk.Label(root, text="Сколько штучек/капелек:", bg="light sky blue")
        self.label_quantity.pack()
        self.entry_quantity = tk.Entry(root, width=30, bg="snow3", fg="black")
        self.entry_quantity.pack()

        # Кнопка для добавления лекарства
        self.button_add = tk.Button(root, text="Добавить лекарство", command=self.add_medicine)
        self.button_add.pack(pady=10)

        # Список добавленных лекарств
        self.listbox = tk.Listbox(root, height=10, width=50, bg="snow3", fg="black")
        self.listbox.pack(pady=10)

        # Кнопка для удаления лекарства
        self.button_remove = tk.Button(root, text="Удалить лекарство", command=self.remove_medicine)
        self.button_remove.pack(pady=10)

    def add_medicine(self):
        name = self.entry_name.get()
        time = self.entry_time.get()
        frequency = self.entry_frequency.get()
        quantity = self.entry_quantity.get()

        # Проверка на правильность ввода
        if not name or not time or not frequency or not quantity:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля правильно.")
            return

        # Добавление лекарства в список
        self.medicines.append((name, time, int(frequency)))
        self.listbox.insert(tk.END, f"{name} - {time}, {frequency} раза в сутки по {quantity}")
        self.entry_name.delete(0, tk.END)
        self.entry_time.delete(0, tk.END)
        self.entry_frequency.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    def remove_medicine(self):
        selected_index = self.listbox.curselection()
        if selected_index:
            self.listbox.delete(selected_index)
            del self.medicines[selected_index[0]]
        else:
            messagebox.showwarning("Предупреждение", "Пожалуйста, выберите лекарство для удаления.")


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineTracker(root)
    root.mainloop()
