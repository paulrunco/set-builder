import tkinter as tk
from tkinter import messagebox as mb
from tkinter import filedialog

import functions.functions as functions

class Builder(tk.Frame):
    def __init__(self, parent, database):
        super().__init__(parent)

        self.db = database
        self.products = self.db.get_products()

        if self.products:
            self.finished = [product[1] for product in self.products]
        else:
            self.finished = ['-']

        # Inventory Report Entry
        self.inventory_report_label = tk.Label(
            self,
            text="Inventory Report",
        ).grid(row=0, column=0, padx=(5,0), pady=(5,0), sticky='w')
        self.inventory_report_entry = tk.Entry(
            self,
            width=80,
            textvariable=tk.StringVar
        )

        # Browse Button
        self.inventory_report_entry.grid(row=1, column=0, padx=5, pady=(0,5), sticky='we', columnspan=3)
        self.inventory_report_button = tk.Button(
            self,
            text="Browse",
            command= self.browse_for).grid(row=1, column=3, padx=5, pady=(0,5), sticky='w'),         

        # Frame for set selection options
        self.selections = tk.LabelFrame(self, relief='groove', borderwidth=1, text="Product Selection")
        self.selections.grid(row=3, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Finished Options
        self.finished_option = tk.StringVar(self)
        self.finished_option.set(self.finished[0])
        self.finished_option.trace('w', self.on_finished_select)

        # Material Options
        self.materials = ['-']
        self.material_option = tk.StringVar(self)
        self.material_option.set(self.materials[0])

        self.options_label = tk.Label(self.selections, text="Product").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.finished_options = tk.OptionMenu(self.selections, self.finished_option, *self.finished, command=self.on_finished_select)
        self.finished_options.grid(row=0, column=1, sticky='ew', padx=(0,5), pady=5)
        self.options_label = tk.Label(self.selections, text="Weight (lbs)").grid(row=1, column=0, sticky='e', padx=5, pady=(0,5))
        self.order_weight_entry = tk.Entry(self.selections, width=8, textvariable=tk.StringVar)
        self.order_weight_entry.grid(row=1, column=1, sticky='ew', padx=(0,5), pady=(0,5))
        self.options_label = tk.Label(self.selections, text="Material").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.material_options = tk.OptionMenu(self.selections, self.material_option, *self.materials)
        self.material_options.grid(row=2, column=1, sticky='ew', padx=(0,5), pady=5)

        self.on_finished_select

        # Generate sets
        self = tk.Button(self, text="Generate sets", command=self.build_sets).grid(row=4, column=0, columnspan=4, sticky='ews', padx=5, pady=5)


    def browse_for(self, target="inventory_report"):
        file_name = filedialog.askopenfilename(
            filetypes=(("Excel files", "*xlsx"), ("All files", "*"))
        )
        if target == "inventory_report":
            self.inventory_report_entry.config(background='white')
            self.inventory_report_entry.delete(0, tk.END)
            self.inventory_report_entry.insert(0, file_name)
            print(file_name)

    def build_sets(self):
        path_to_inventory_report = self.inventory_report_entry.get()
        if path_to_inventory_report == "":
            mb.showwarning(title="Warning: ID-10T", message="Please select an inventory report")
            self.inventory_report_entry.config(background='red')
            return

        finished = self.finished_option.get()
        material = self.material_option.get()
        order_target_lbs = int(self.order_weight_entry.get())

        if order_target_lbs == '':
            mb.showwarning(title="Warning: ID-10T", message="Please enter a target order weight")
            self.order_weight_entry.config(background='red')
        else:
            print(f'Assigning sets of {finished} using {material} up to {order_target_lbs} lbs')

            product = self.db.get_product_with_name_material(finished, material)

            if len(product) > 1:
                mb.showerror(title="Error - Too Many Materials",
                message="More than one material exists for this configuration, please check your settings.")
            elif len(product) == 0:
                mb.showerror(title="Error - No Materials",
                message="No material exist for this configuration, please check your settings.")
            elif len(product) == 1:

                (id, _, _, description, target_lbs, min_lbs, max_lots ) = product[0]

                try:
                    functions.generate_sets(
                        path_to_inventory_report,
                        finished, material, 
                        order_target_lbs, 
                        target_lbs, 
                        min_lbs)

                except ValueError as error:
                    mb.showwarning(title="Error", message=error.message)
                    return

    def refresh_products(self):
        self.products = self.db.get_products()

        if self.products:
            self.finished = [product[1] for product in self.products]
        else:
            self.finished = ['-']

        self.finished_options['menu'].delete(0, 'end')
        for fin in self.finished:
            self.finished_options['menu'].add_command(label=fin, command=tk._setit(self.finished_option, fin))

        self.finished_option.set(self.finished[0])

    def on_finished_select(self, *args):
        product = self.finished_option.get()
        products = self.db.get_products_with_name(product )

        materials = [product[3] for product in products] # extract material part number

        # Update the materials dropdown
        self.material_options['menu'].delete(0, 'end')

        if materials:
            for material in materials:
                self.material_options['menu'].add_command(label=material, command=tk._setit(self.material_option, material))

            self.material_option.set(self.materials[0])
        

        
