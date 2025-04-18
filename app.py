import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import json
import threading


class MedicineTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Напоминалка о лекарствах v2.0")
        self.root.configure(bg="light sky blue")
        self.medicines = []
        self.load_data()

        # Элементы интерфейса
        self.create_widgets()
        self.schedule_checks()

    def create_widgets(self):
        # Название лекарства
        self.label_name = tk.Label(self.root, text="Название:", bg="light sky blue")
        self.label_name.pack(pady=5)
        self.entry_name = tk.Entry(self.root, width=30, bg="snow3")
        self.entry_name.pack(pady=5)

        # Время первого приёма
        self.label_time = tk.Label(self.root, text="Первый приём (ЧЧ:ММ):", bg="light sky blue")
        self.label_time.pack(pady=5)
        self.entry_time = tk.Entry(self.root, bg="snow3")
        self.entry_time.pack(pady=5)

        # Частота приёма
        self.label_frequency = tk.Label(self.root, text="Раз в сутки:", bg="light sky blue")
        self.label_frequency.pack(pady=5)
        self.entry_frequency = tk.Entry(self.root, bg="snow3")
        self.entry_frequency.pack(pady=5)

        # Дозировка
        self.label_quantity = tk.Label(self.root, text="Дозировка:", bg="light sky blue")
        self.label_quantity.pack(pady=5)
        self.entry_quantity = tk.Entry(self.root, bg="snow3")
        self.entry_quantity.pack(pady=5)

        # Кнопки
        self.btn_frame = tk.Frame(self.root, bg="light sky blue")
        self.btn_frame.pack(pady=10)

        self.add_btn = tk.Button(self.btn_frame, text="Добавить", command=self.add_medicine)
        self.add_btn.pack(side=tk.LEFT, padx=5)

        self.remove_btn = tk.Button(self.btn_frame, text="Удалить", command=self.remove_medicine)
        self.remove_btn.pack(side=tk.LEFT, padx=5)

        # Список лекарств
        self.listbox = tk.Listbox(self.root, width=60, bg="snow3")
        self.listbox.pack(pady=10, padx=20)
        self.update_listbox()

    def add_medicine(self):
        try:
            name = self.entry_name.get().strip()
            time_str = self.entry_time.get().strip()
            frequency = self.entry_frequency.get().strip()
            quantity = self.entry_quantity.get().strip()

            # Валидация
            if not all([name, time_str, frequency, quantity]):
                raise ValueError("Все поля обязательны")

            time = datetime.strptime(time_str, "%H:%M").time()
            frequency = int(frequency)
            if frequency <= 0:
                raise ValueError("Частота должна быть > 0")

            # Расчёт следующего приёма
            now = datetime.now()
            next_dose = datetime.combine(now.date(), time)
            if next_dose < now:
                next_dose += timedelta(days=1)

            new_med = {
                "name": name,
                "time": time_str,
                "frequency": frequency,
                "quantity": quantity,
                "next_dose": next_dose.strftime("%Y-%m-%d %H:%M:%S")
            }

            self.medicines.append(new_med)
            self.update_listbox()
            self.clear_entries()
            self.save_data()

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def remove_medicine(self):
        selected = self.listbox.curselection()
        if selected:
            del self.medicines[selected[0]]
            self.update_listbox()
            self.save_data()
        else:
            messagebox.showwarning("Внимание", "Выберите лекарство для удаления")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for med in self.medicines:
            next_dose = datetime.strptime(med["next_dose"], "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y %H:%M")
            self.listbox.insert(tk.END,
                                f"{med['name']} | {med['time']} | {med['frequency']}р/д | {med['quantity']} | След.: {next_dose}")

    def schedule_checks(self):
        """Проверяет напоминания каждые 60 секунд"""
        try:
            now = datetime.now()
            for med in self.medicines:
                next_dose = datetime.strptime(med["next_dose"], "%Y-%m-%d %H:%M:%S")
                if now >= next_dose:
                    self.show_reminder(med)
                    # Пересчитываем следующий приём
                    interval = timedelta(hours=24 / med["frequency"])
                    med["next_dose"] = (next_dose + interval).strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
        finally:
            self.root.after(60000, self.schedule_checks)

    def show_reminder(self, medicine):
        messagebox.showinfo("Напоминание",
                            f"Пора принять:\n{medicine['quantity']} {medicine['name']}\nСледующий приём: {medicine['next_dose']}",
                            parent=self.root)

    def clear_entries(self):
        self.entry_name.delete(0, tk.END)
        self.entry_time.delete(0, tk.END)
        self.entry_frequency.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)

    def save_data(self):
        with open("medicines.json", "w") as f:
            json.dump(self.medicines, f, indent=2, default=str)

    def load_data(self):
        try:
            with open("medicines.json", "r") as f:
                self.medicines = json.load(f)
                # Преобразуем строки обратно в datetime
                for med in self.medicines:
                    med["next_dose"] = datetime.fromisoformat(med["next_dose"]).strftime("%Y-%m-%d %H:%M:%S")
        except FileNotFoundError:
            self.medicines = []


if __name__ == "__main__":
    root = tk.Tk()
    app = MedicineTracker(root)
    root.mainloop()