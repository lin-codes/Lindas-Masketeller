import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import os
import sys

# --- Filplassering ---
if getattr(sys, 'frozen', False):
    # Når programmet kjører som .exe: bruk mappa der .exe ligger
    BASE_DIR = os.path.dirname(sys.executable)
else:
    # Når det kjører som vanlig .py: bruk mappa der scriptet ligger
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "teller.json")


# Funksjoner for Teller 1
def øke1():
    label1.config(text=str(int(label1["text"]) + 1))

def senke1():
    label1.config(text=str(int(label1["text"]) - 1))

# Funksjoner for Teller 2
def øke2():
    label2.config(text=str(int(label2["text"]) + 1))

def senke2():
    label2.config(text=str(int(label2["text"]) - 1))

# Nullstill (behold valgt telling)
def reset_current():
    label1.config(text="0")
    label2.config(text="0")

# Lagre telling
def save():
    valgt = combo.get()

    # Hvis man har valgt en telling: oppdater den
    if valgt:
        navn = valgt
    else:
        # Ellers spør om nytt navn
        navn = simpledialog.askstring("Lagre", "Gi et navn til tellingen:")
        if not navn:
            return

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    data[navn] = [int(label1["text"]), int(label2["text"])]

    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

    update_choices(list(data.keys()))
    combo.set(navn)

# Ny telling (alltid nytt navn og nullstilt)
def new_telling():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
    else:
        data = {}

    while True:
        navn = simpledialog.askstring("Ny telling", "Gi et navn til den nye tellingen:")
        if not navn:
            return  # Avbryt helt hvis brukeren ikke skriver noe

        if navn in data:
            messagebox.showwarning("Finnes allerede",
                                   f"Tellingen '{navn}' finnes allerede.\nPrøv et annet navn.")
            continue  # gå tilbake og spør igjen
        else:
            # Hvis navnet er ledig → lagre ny telling
            data[navn] = [0, 0]
            with open(DATA_FILE, "w") as f:
                json.dump(data, f, indent=2)
            update_choices(list(data.keys()))
            combo.set(navn)
            label1.config(text="0")
            label2.config(text="0")
            break  # ferdig, ut av while-løkken

# Last inn telling
def load(valgt):
    if not valgt or not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if valgt in data:
        label1.config(text=str(data[valgt][0]))
        label2.config(text=str(data[valgt][1]))

# Slett telling
def delete():
    valgt = combo.get()
    if not valgt or not os.path.exists(DATA_FILE):
        return
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
    if valgt in data and messagebox.askyesno("Slett", f"Vil du slette '{valgt}'?"):
        del data[valgt]
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        update_choices(list(data.keys()))
        combo.set("")
        reset_current()

def update_choices(names):
    combo["values"] = names
    if not names:
        combo.set("")

def init_load():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        update_choices(list(data.keys()))

def on_select(event):
    valgt = combo.get()
    load(valgt)

# GUI setup
root = tk.Tk()
root.title("Masketeller")
root.geometry("580x540")
root.configure(bg="#fffdf4")

frame = tk.Frame(root, bg="#fffdf4")
frame.pack(pady=20)

# Teller 1
t1 = tk.LabelFrame(frame, text="Teller 1", padx=10, pady=10,
                   bg="#fff6f2", fg="#361a10", font=("Arial", 10, "bold"))
t1.grid(row=0, column=0, padx=10)

label1 = tk.Label(t1, text="0", font=("Arial", 24), bg="#fff9f7", fg="#361a10")
label1.grid(row=0, column=0, columnspan=2)

tk.Button(t1, text="+", command=øke1, bg="#f0dbd5", fg="#49280f",
          font=("Arial", 12, "bold"), width=4).grid(row=1, column=0, padx=5, pady=5)
tk.Button(t1, text="–", command=senke1, bg="#f0dbd5", fg="#49280f",
          font=("Arial", 12, "bold"), width=4).grid(row=1, column=1, padx=5, pady=5)

# Teller 2 
t2 = tk.LabelFrame(frame, text="Teller 2", padx=10, pady=10,
                   bg="#fff6f2", fg="#361a10", font=("Arial", 10, "bold"))
t2.grid(row=0, column=1, padx=10)

label2 = tk.Label(t2, text="0", font=("Arial", 24), bg="#fff9f7", fg="#361a10")
label2.grid(row=0, column=0, columnspan=2)

tk.Button(t2, text="+", command=øke2, bg="#f0dbd5", fg="#49280f",
          font=("Arial", 12, "bold"), width=4).grid(row=1, column=0, padx=5, pady=5)
tk.Button(t2, text="–", command=senke2, bg="#f0dbd5", fg="#49280f",
          font=("Arial", 12, "bold"), width=4).grid(row=1, column=1, padx=5, pady=5)

# Nederste del
bottom = tk.Frame(root, bg="#fffdf4")
bottom.pack(pady=10)

combo = ttk.Combobox(bottom, state="readonly", width=30)
combo.grid(row=0, column=0, columnspan=4, pady=5)

tk.Button(bottom, text="Lagre", command=save, bg="#d6b96f", fg="white",
          font=("Arial", 10, "bold"), width=12).grid(row=1, column=0, padx=5, pady=5)
tk.Button(bottom, text="Ny telling", command=new_telling, bg="#ba8d8d", fg="white",
          font=("Arial", 10, "bold"), width=12).grid(row=1, column=1, padx=5, pady=5)
tk.Button(bottom, text="Slett", command=delete, bg="#d6b96f", fg="white",
          font=("Arial", 10, "bold"), width=12).grid(row=1, column=2, padx=5, pady=5)
tk.Button(bottom, text="Nullstill", command=reset_current, bg="#ba8d8d", fg="white",
          font=("Arial", 10, "bold"), width=12).grid(row=1, column=3, padx=5, pady=5)

combo.bind("<<ComboboxSelected>>", on_select)
init_load()

# Bilde
frames = []
i = 0
while True:
    try:
        frame = tk.PhotoImage(file="bee.gif", format=f"gif - {i}")
    except Exception:
        break
    frames.append(frame)
    i += 1

def update(ind):
    frame = frames[ind]
    ind = (ind + 1) % len(frames)
    label_img.configure(image=frame)
    root.after(90, update, ind)  # ms per frame

label_img = tk.Label(root, bg="#fffdf4")
label_img.pack(pady=10)
label_img.place(x=20, y=250)

# start animasjonen på GIF-bildet
root.after(0, update, 0)



# Brukerveiledning nederst
info = tk.Label(root, text=
                "Brukerveiledning:\n"
                "- 'Lagre' oppdaterer valgt telling eller ber om nytt navn hvis ingen er valgt.\n"
                "- 'Ny telling' oppretter en ny lagring og starter på 0.\n"
                "- 'Slett' fjerner valgt telling permanent.\n"
                "- 'Nullstill' setter tellerne til 0 på tellingen.",
                bg="#f0dbd5", fg="black", font=("Arial", 12), justify="left")
info.place(x=50, y=250)

root.mainloop()
