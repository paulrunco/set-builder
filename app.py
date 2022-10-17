import tkinter as tk
from tkinter import ttk
import webbrowser
from os import path

from ui.builder import Builder
from ui.setup import Setup

import database.dbase as dbase

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Set Builder Utility')
        self.version = "0.1.0"
        self.author = "PRunco"
        path_to_icon = path.abspath(path.join(path.dirname(__file__), 'icon.ico'))
        self.iconbitmap(path_to_icon)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(True, True)

        self.db = dbase.Database()
        self.products = self.db.get_products()

        ## Menu
        self.menubar = tk.Menu(self)

        # File Menu
        self.filemenu = tk.Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label="Open", command=lambda: self.set_builder.browse_for, accelerator="Ctrl+O")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.close_app, accelerator="Ctrl+W")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.bind_all("<Control-o>", lambda: self.set_builder.browse_for)
        self.bind_all("<Control-w>", self.close_app)

        # Help Menu
        self.helpmenu = tk.Menu(self.menubar, tearoff=False)
        self.helpmenu.add_command(label="Documentation", command=self.open_docs, accelerator="Ctrl+?")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.bind_all("<Control-?>", self.open_docs)

        self.config(menu=self.menubar)

        ## App window layout managed in tabs as a notebook widget
        self.tabbed_layout = ttk.Notebook(self)
        self.tabbed_layout.grid(sticky='nsew')
        self.tabbed_layout.columnconfigure(0, weight=1)

        self.set_builder = Builder(self, self.db)
        self.set_builder.grid(sticky='nsew')
        self.set_builder.columnconfigure(0, weight=1)
        self.set_builder.rowconfigure(3, weight=1)
        self.setup = Setup(self, self.db)
        self.setup.grid(sticky='nsew')
        self.setup.columnconfigure(0, weight=1)
        self.setup.rowconfigure(1, weight=1)

        self.tabbed_layout.add(self.set_builder, text="Builder")
        self.tabbed_layout.add(self.setup, text="Setup")

    def open_docs(self, event=None):
        webbrowser.open('https://github.com/paulrunco/set-builder')

    def close_app(self, event=None):
        self.db.close()
        self.quit()

if __name__=="__main__":
    app = App()
    app.mainloop()