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

def line_numbers(*i):
    line_numbers_widget.config(state="normal")
    line_numbers_widget.delete(1.0, tk.END)

    total_lines = int(text.index("end-1c").split('.')[0])
    display_line_number = 1

    for line in range(1, total_lines + 1):
        wrapped_lines = text.count(f"{line}.0", f"{line}.end", "displaylines")[0]

        for _ in range(wrapped_lines or 1):
            line_numbers_widget.insert(tk.END, f"{display_line_number}\n")
            display_line_number += 1

    line_numbers_widget.config(state="disabled")
    text.edit_modified(False)



root = tk.Tk()
root.title('Syntax Shade')
root.geometry('100x800')
icon = tk.PhotoImage(file='syntaxlogo.png')
root.iconphoto(False, icon)

# the box for the line numbers
frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

text = Text(frame, wrap="word", undo=True)
text.pack(side="right", expand=True, fill="both")

line_numbers_widget = Text(frame, width=4, wrap="none", padx=5, takefocus=0, state="disabled")
line_numbers_widget.pack(side="left", fill="y")

# the line numbers update when keys are pressed
text.bind("<KeyRelease>", line_numbers)
text.bind("<ButtonRelease-1>", line_numbers)

menu = tk.Menu(root)
root.config(menu=menu)

# for the file button
file_menu = tk.Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)

# for the scrollbar
scrollbar = Scrollbar(text)
scrollbar.pack(side=RIGHT, fill=Y)
scrollbar.config(command=text.yview)
text.config(yscrollcommand=scrollbar.set)


root.mainloop()