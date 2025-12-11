import tkinter as tk
from tkinter import messagebox
import os
import json


DATA_FILE = "films_list.json"

# Создаёт файл, если его нет
def ensure_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

# Загрузка данных из файла
def load_data():
    ensure_file()
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            return json.loads(content)
    except Exception as e:
        print(f"❌ Error loading: {e}")
        return []

# Сохранение данных в файл
def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Saved in {DATA_FILE}")
    except Exception as e:
        print(f"❌ Error saving: {e}")
        messagebox.showerror("Error", f"Failed to save:\n{e}")

def save_film():
    title = entry_title.get().strip()
    status = entry_status.get()
    rating = entry_rating.get()

    if not title:
        messagebox.showerror("Error", "Enter the name of the movie")
        return

    film = {
        "title": title,
        "status": status,
        "rating": rating
    }

    film_list = load_data()
    film_list.append(film)
    save_data(film_list)

    entry_title.delete(0, tk.END)
    set_status("in the plans")
    set_rating("")
    messagebox.showinfo("Success", f"Movie'{title}' successfully added to the list!")

def center_window(window, width=400, height=300):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

def show_film_list():
    film_list = load_data()
    selected_index = tk.IntVar(value=-1)

    list_window = tk.Toplevel(main_window)
    list_window.title("List of films")
    center_window(list_window, 620, 420)
    list_window.configure(bg="#f0f0f0")

    tk.Label(list_window, text="My movie list", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    canvas = tk.Canvas(list_window, bg="#f0f0f0", borderwidth=0, highlightthickness=0)
    frame = tk.Frame(canvas, bg="#ffffff")
    scrollbar = tk.Scrollbar(list_window, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)
    canvas.create_window((0, 0), window=frame, anchor="nw")

    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    blocks = []

    def on_select(index):
        selected_index.set(index)
        for i, b in enumerate(blocks):
            b.config(bg="#e3f2fd" if i == index else "#ffffff")

    for idx, anime in enumerate(film_list):
        block = tk.Frame(frame, bg="#ffffff", bd=1, relief="solid", padx=10, pady=5)
        block.pack(fill="x", padx=10, pady=5)
        block.bind("<Button-1>", lambda e, i=idx: on_select(i))

        def label(text, font_style):
            lbl = tk.Label(block, text=text, font=font_style, bg="#ffffff", anchor="w")
            lbl.pack(anchor="w")
            lbl.bind("<Button-1>", lambda e, i=idx: on_select(i))
            return lbl

        label(f"{idx + 1}. {anime['title']}", ("Arial", 12, "bold"))
        label(f"Статус: {anime['status']}", ("Arial", 11))
        if anime.get("rating"):
            label(f"Grade: {anime['rating']}", ("Arial", 11))

        blocks.append(block)

    def delete_selected():
        idx = selected_index.get()
        if idx == -1:
            messagebox.showwarning("Select", "Select a movie to delete.")
            return

        if messagebox.askyesno("Delete", "Delete the selected movie?"):
            del film_list[idx]
            save_data(film_list)
            list_window.destroy()
            show_film_list()

    tk.Button(
        list_window,
        text="Delete selected",
        command=delete_selected,
        bg="#f44336",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=10,
        pady=5
    ).pack(pady=10)

# Главное окно
main_window = tk.Tk()
main_window.title("A simple movie app")
center_window(main_window, 450, 380)
main_window.configure(bg="#f0f0f0")

tk.Label(main_window, text="Add a movie", font=("Arial", 16, "bold"), bg="#f0f0f0").pack(pady=15)

form_frame = tk.Frame(main_window, bg="#f0f0f0")
form_frame.pack(padx=20, pady=10)

tk.Label(form_frame, text="Movie title:", font=("Arial", 12), bg="#f0f0f0").grid(row=0, column=0, sticky="w")
entry_title = tk.Entry(form_frame, font=("Arial", 11), width=30)
entry_title.grid(row=1, column=0, columnspan=5, pady=5)

tk.Label(form_frame, text="Status:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="w", pady=(10, 0))

entry_status = tk.StringVar()
entry_status.set("In the plans")

status_buttons = []
statuses = ["I'm watching", "Viewed", "In the plans"]

def set_status(s):
    entry_status.set(s)
    for btn in status_buttons:
        if btn["text"] == s:
            btn.config(bg="#2196F3", fg="white")
        else:
            btn.config(bg="SystemButtonFace", fg="black")

status_frame = tk.Frame(form_frame, bg="#f0f0f0")
status_frame.grid(row=3, column=0, columnspan=5, sticky="w", pady=5)

for status in statuses:
    btn = tk.Button(
        status_frame,
        text=status,
        font=("Arial", 11),
        width=10,
        command=lambda s=status: set_status(s)
    )
    btn.pack(side="left", padx=5)
    status_buttons.append(btn)

set_status("In the plans")

tk.Label(form_frame, text="Grade (1–5):", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, sticky="w", pady=(10, 0))

entry_rating = tk.StringVar()
entry_rating.set("")

rating_buttons = []

def set_rating(r):
    entry_rating.set(r)
    for i, btn in enumerate(rating_buttons, 1):
        if str(i) == r:
            btn.config(bg="#4CAF50", fg="white")
        else:
            btn.config(bg="SystemButtonFace", fg="black")

rating_frame = tk.Frame(form_frame, bg="#f0f0f0")
rating_frame.grid(row=5, column=0, columnspan=5, sticky="w", pady=5)

for i in range(1, 6):
    btn = tk.Button(
        rating_frame,
        text=str(i),
        width=3,
        font=("Arial", 11, "bold"),
        command=lambda x=i: set_rating(str(x))
    )
    btn.pack(side="left", padx=3)
    rating_buttons.append(btn)

# Кнопки Сохранить и Список
button_frame = tk.Frame(main_window, bg="#f0f0f0")
button_frame.pack(pady=20)

tk.Button(
    button_frame,
    text="Save",
    command=save_film,
    bg="#4CAF50",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5
).pack(side="left", padx=10)

tk.Button(
    button_frame,
    text="List",
    command=show_film_list,
    bg="#2196F3",
    fg="white",
    font=("Arial", 11, "bold"),
    padx=10,
    pady=5
).pack(side="right", padx=10)

main_window.mainloop()
