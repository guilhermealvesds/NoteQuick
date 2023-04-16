import tkinter as tk
import tkinter.ttk as ttk
import sqlite3

root = tk.Tk()
root.title("NoteQuick v1.0.0")

frame_tree = ttk.Frame(root)
frame_tree.pack(padx=10, pady=10)

tree = ttk.Treeview(frame_tree, columns=("coluna1", "coluna2"))
tree.heading("#0", text="ID")
tree.heading("coluna1", text="Nome")
tree.heading("coluna2", text="Valor")
tree.pack()

frame_input = ttk.Frame(root)
frame_input.pack(padx=10, pady=10)

label_nome = ttk.Label(frame_input, text="Nome:")
label_nome.grid(row=0, column=0, padx=5, pady=5)
entry_nome = ttk.Entry(frame_input)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

label_valor = ttk.Label(frame_input, text="Valor:")
label_valor.grid(row=1, column=0, padx=5, pady=5)
entry_valor = ttk.Entry(frame_input)
entry_valor.grid(row=1, column=1, padx=5, pady=5)

def adicionar():
    nome = entry_nome.get()
    valor = entry_valor.get()
    if nome and valor:
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO valores (nome, valor) VALUES (?, ?)", (nome, valor))
        conn.commit()
        cursor.close()
        conn.close()
        tree.insert("", "end", text=cursor.lastrowid, values=(nome, valor))

def pesquisar():
    nome = entry_nome.get()
    conn = sqlite3.connect("banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, valor FROM valores WHERE nome LIKE ?", (f"%{nome}%",))
    for row in tree.get_children():
        tree.delete(row)
    for row in cursor.fetchall():
        tree.insert("", "end", text=row[0], values=row[1:])
    cursor.close()
    conn.close()

def on_select(event):
    selected_item = tree.selection()[0]
    item_values = tree.item(selected_item, "values")
    entry_valor.delete(0, tk.END)
    entry_valor.insert(0, item_values[1])

botao_adicionar = ttk.Button(frame_input, text="Adicionar", command=adicionar)
botao_adicionar.grid(row=2, column=0, padx=5, pady=5)
botao_pesquisar = ttk.Button(frame_input, text="Pesquisar", command=pesquisar)
botao_pesquisar.grid(row=2, column=1, padx=5, pady=5)

tree.bind("<<TreeviewSelect>>", on_select)

conn = sqlite3.connect("banco.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS valores (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT, valor TEXT)")
conn.commit()
cursor.close()
conn.close()

root.mainloop()
