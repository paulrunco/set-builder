from tkinter import Label, Entry, Button, LabelFrame, Menu, OptionMenu, StringVar, filedialog, Tk, END
from tkinter import messagebox as mb
from tkinter import ttk
import webbrowser

import functions
import dbase

class App(Tk):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.title('Set Builder Utility')
        self.version = "0.1.0"
        self.author = "PRunco"

        self.db = dbase.Database()
        #self.db.add_product('test', 'product 2', 15)
        self.products = self.db.get_products()
        print(self.products)
        if self.products:
            self.finished = [(product[0], product[1]) for product in self.products]
        else:
            self.finished = ['-']

        ## Menu
        self.menubar = Menu(self)

        # File Menu
        self.filemenu = Menu(self.menubar, tearoff=False)
        self.filemenu.add_command(label="Open", command=self.browse_for, accelerator="Ctrl+O")
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.close_app, accelerator="Ctrl+W")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        self.bind_all("<Control-o>", self.browse_for)
        self.bind_all("<Control-w>", self.close_app)

        # Help Menu
        self.helpmenu = Menu(self.menubar, tearoff=False)
        self.helpmenu.add_command(label="Documentation", command=self.open_docs, accelerator="Ctrl+?")
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)

        self.bind_all("<Control-?>", self.open_docs)

        self.config(menu=self.menubar)

        ## App window layout managed in tabs as a notebook widget
        self.tabbed_layout = ttk.Notebook(self)
        self.tabbed_layout.grid()

        self.set_builder = ttk.Frame(self.tabbed_layout)
        self.set_builder.grid()
        self.products = ttk.Frame(self.tabbed_layout)
        self.products.grid()
        self.materials = ttk.Frame(self.tabbed_layout)
        self.materials.grid()
        self.boms = ttk.Frame(self.tabbed_layout)
        self.boms.grid()

        self.tabbed_layout.add(self.set_builder, text="Set Builder")
        self.tabbed_layout.add(self.products, text="Products")
        self.tabbed_layout.add(self.materials, text="Materials")
        self.tabbed_layout.add(self.boms, text="BOMs")

        ## Inventory Report Entry
        self.inventory_report_label = Label(
            self.set_builder,
            text="Inventory Report",
        ).grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky='w')
        self.inventory_report_entry = Entry(
            self.set_builder,
            width=80,
            textvariable=StringVar
        )
        self.inventory_report_entry.grid(row=1, column=0, padx=5, pady=(0,5), sticky='w', columnspan=3)
        self.inventory_report_button = Button(
            self.set_builder,
            text="Browse",
            command=lambda: self.browse_for("inventory_report")
        ).grid(row=1, column=3, padx=5, pady=(0,5), sticky='w')        

        ## Frame for set selection options
        self.selections = LabelFrame(self.set_builder, relief='groove', borderwidth=1, text="Product Selection")
        self.selections.grid(row=3, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        
        ## Finished Options
        self.finished_option = StringVar(self)
        self.finished_option.set(self.finished[0])

        ## Material Options
        self.materials = ['1570']
        self.material_option = StringVar(self)
        self.material_option.set(self.materials[0])

        self.options_label = Label(self.selections, text="Product").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.finished_options = OptionMenu(self.selections, self.finished_option, *self.finished).grid(row=0, column=1, sticky='ew', padx=(0,5), pady=5)
        self.options_label = Label(self.selections, text="Weight (lbs)").grid(row=1, column=0, sticky='e', padx=5, pady=(0,5))
        self.order_weight_entry = Entry(self.selections, width=8, textvariable=StringVar)
        self.order_weight_entry.grid(row=1, column=1, sticky='ew', padx=(0,5), pady=(0,5))
        self.options_label = Label(self.selections, text="Material").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.material_options = OptionMenu(self.selections, self.material_option, *self.materials).grid(row=2, column=1, sticky='ew', padx=(0,5), pady=5)

        ## Frame for set information
        self.information = LabelFrame(self.set_builder, relief='groove', borderwidth=1, text='Info')
        self.information.grid(row=3, column=2, columnspan=2, sticky='ewns', padx=5, pady=5)

        # self.num_cuts = Label(self.information, text="Cuts").grid(row=0, column=0, sticky='e', padx=5, pady=5)

        # Generate sets
        self.set_builder = Button(self.set_builder, text="Generate sets", command=lambda: self.build_sets()
        ).grid(row=4, column=0, columnspan=4, sticky='ew', padx=5, pady=5)

    def browse_for(self, target="inventory_report"):
        file_name = filedialog.askopenfilename(
            filetypes=(("Excel files", "*xlsx"), ("All files", "*"))
        )
        if target == "inventory_report":
            self.inventory_report_entry.config(background='white')
            self.inventory_report_entry.delete(0, END)
            self.inventory_report_entry.insert(0, file_name)
            print(file_name)

    def build_sets(self):
        print("Clicked build set button...")
        path_to_inventory_report = self.inventory_report_entry.get()
        # if path_to_inventory_report == "":
        #     mb.showwarning(title="Warning: ID-10T", message="Please select an inventory report")
        #     self.inventory_report_entry.config(background='red')
        #     return
        finished = self.finished_option.get()
        material = self.material_option.get()
        order_target_lbs = int(self.order_weight_entry.get())
        if order_target_lbs == '':
            mb.showwarning(title="Warning: ID-10T", message="Please enter a target order weight")
            self.order_weight_entry.config(background='red')
        else:
            print(f'Assigning sets of {finished} using {material} up to {order_target_lbs} lbs')
            try:
                functions.generate_sets(
                    path_to_inventory_report,
                    finished, material, 
                    order_target_lbs, 
                    604.8, 
                    573.6)
            except ValueError as error:
                mb.showwarning(title="Error", message=error.message)
                return

    def open_docs(self, event=None):
        webbrowser.open('https://github.com/paulrunco/set-builder')

    def close_app(self, event=None):
        self.db.close()
        self.quit()

if __name__=="__main__":
    app = App()
    app.mainloop()