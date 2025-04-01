import tkinter as tk
from tkinter import *
from tkinter import filedialog, Text
import keyword
import re

keywords = keyword.kwlist

def highlight_keywords(event=None):
    text.tag_remove("keyword", "1.0", tk.END)
    text.tag_remove("string", "1.0", tk.END)
    text.tag_remove("comment", "1.0", tk.END)
    # keywords
    content = text.get("1.0", tk.END)
    for word in keywords:
        matches = [m.start() for m in re.finditer(rf'\b{word}\b', content)]
        for start_index in matches:
            start = text.index(f"1.0+{start_index}c")
            end = text.index(f"{start}+{len(word)}c")
            text.tag_add("keyword", start, end)
    # strings
        for match in re.finditer(r'(\".*?(?<!\\)\"|\'.*?(?<!\\)\')'
, content):
            start_index = match.start()
            end_index = match.end()
            start = text.index(f"1.0+{start_index}c")
            end = text.index(f"1.0+{end_index}c")
            text.tag_add("string", start, end)
    # comments
        for match in re.finditer(r'#.*', content):
            start_index = match.start()
            end_index = match.end()
            start = text.index(f"1.0+{start_index}c")
            end = text.index(f"1.0+{end_index}c")
            text.tag_add("comment", start, end)
    # for variable names
    for match in re.finditer(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*=', content):
        var_name = match.group(1)
        start = f"1.0+{match.start(1)}c"
        end = f"1.0+{match.end(1)}c"
        text.tag_add("variable", start, end)

def auto_indent(event):
    line_index = text.index("insert linestart")
    line_text = text.get(line_index, f"{line_index} lineend")

    indent = re.match(r"\s*", line_text).group()

    if line_text.rstrip().endswith(":"):
        indent += "    "

    text.insert("insert", f"\n{indent}")
    return "break"

def open_file():
    file_path = filedialog.askopenfilename(
        title="Open File",
        filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("HTML Files", "*.html"), ("CSS Files", "*.css"), ("JavaScript Files", "*.js"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
        line_numbers()
        highlight_keywords()

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

    text_width = text.winfo_width()

    font = text.cget("font")
    char_width = text.bbox("1.0")[2]

    for line in range(1, total_lines + 1):

        line_content = text.get(f"{line}.0", f"{line}.end")
        
        wrapped_lines = len(line_content) // (text_width // char_width) + 1

        for _ in range(wrapped_lines):
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

# styling of keywords
text.tag_configure("keyword", foreground="blue", font=("TkDefaultFont", 10, "bold"))
text.tag_configure("string", foreground="green")
text.tag_configure("comment", foreground="gray", font=("TkDefaultFont", 10, "italic"))
text.tag_configure("variable", foreground="orange")

line_numbers_widget = Text(frame, width=4, wrap="none", padx=5, takefocus=0, state="disabled")
line_numbers_widget.pack(side="left", fill="y")

# for updating line numbers
def on_modified(event=None):
    if text.edit_modified():
        line_numbers()
        highlight_keywords()
        text.edit_modified(False)

text.bind("<<Modified>>", on_modified)
text.bind("<ButtonRelease-1>", line_numbers)
text.bind("<Return>", auto_indent)

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