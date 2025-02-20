import tkinter as tk
from tkinter import *
from tkinter import filedialog, Text


def open_file():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("HTML Files", "*.html"), ("CSS Files", "*.css"), ("JavaScript Files", "*.js"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        title="Save File"
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get(1.0, tk.END)) 


root = tk.Tk()
root.title('Syntax Shade')
icon = tk.PhotoImage(file='syntaxlogo.png')
root.iconphoto(False, icon)

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

text = Text(root, wrap="word")
text.pack(expand=True, fill='both')

scrollbar = Scrollbar(text)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)


root.mainloop()