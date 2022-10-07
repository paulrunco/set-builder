import tkinter as tk
from tkinter import ttk

class Setup(tk.Frame):
    def __init__(self, parent, database):
        super().__init__(parent)

        self.db = database
    
        self.action_row = tk.Frame(self)
        self.action_row.columnconfigure((0,1), weight=1)
        self.action_row.grid(row=0, column=0, sticky='e')

        self.edit_button = tk.Button(self.action_row, text='Edit', width=8, command=self.start_edit).grid(row=0, column=0, sticky='e')
        self.edit_button = tk.Button(self.action_row, text='Delete', width=8, command=self.delete).grid(row=0, column=1, sticky='e')

        columns = ('id', 'product', 'code', 'material', 'target_lbs', 'min_lbs', 'max_lots')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', selectmode='browse')
        self.tree.heading('id', text='ID')
        self.tree.heading('product', text='Product')
        self.tree.heading('code', text='Code')
        self.tree.heading('material', text='Material')
        self.tree.heading('target_lbs', text='Target Lbs')
        self.tree.heading('min_lbs', text='Min Lbs',)
        self.tree.heading('max_lots', text='Max Lots')
        
        self.tree.column('id', width=0, stretch=False)
        self.tree.column('product', width=60, anchor='w')
        self.tree.column('code', anchor='w')
        self.tree.column('material', width=60, anchor='w')
        self.tree.column('target_lbs', width=74, anchor='e')
        self.tree.column('min_lbs', width=74, anchor='e')
        self.tree.column('max_lots', width=64, anchor='center')

        self.tree.grid(row=1, column=0, sticky='nsew')

        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=1,column=1,sticky='ns')

        self.refresh()

        self.edit_frame = tk.Frame(self)
        self.edit_frame.columnconfigure((0,1,2,3,4,5), weight=1)
        self.edit_frame.grid(row=2,column=0, sticky='nsew', padx=(5,5), pady=(5,5))

        self.edit_product_label = tk.Label(self.edit_frame, text='Product').grid(row=0, column=0, sticky='w')
        self.edit_code_label = tk.Label(self.edit_frame, text='Code').grid(row=0, column=1, sticky='w')
        self.edit_material_label = tk.Label(self.edit_frame, text='Material').grid(row=0, column=2, sticky='w')
        self.edit_target_lbs_label = tk.Label(self.edit_frame, text='Target Lbs').grid(row=0, column=3, sticky='w')
        self.edit_min_lbs_label = tk.Label(self.edit_frame, text='Min Lbs').grid(row=0, column=4, sticky='w')
        self.edit_max_lots_label = tk.Label(self.edit_frame, text='Max Lots').grid(row=0, column=5, sticky='w')

        self.edit_product_entry = tk.Entry(self.edit_frame, width=10)
        self.edit_product_entry.grid(row=1, column=0, sticky='ew')
        self.edit_code_entry = tk.Entry(self.edit_frame, width=34)
        self.edit_code_entry.grid(row=1, column=1, sticky='ew')
        self.edit_material_entry = tk.Entry(self.edit_frame, width=9)
        self.edit_material_entry.grid(row=1, column=2, sticky='ew')
        self.edit_target_lbs_entry = tk.Entry(self.edit_frame, width=12)
        self.edit_target_lbs_entry.grid(row=1, column=3, sticky='ew')
        self.edit_min_lbs_entry = tk.Entry(self.edit_frame, width=12)
        self.edit_min_lbs_entry.grid(row=1, column=4, sticky='ew')
        self.edit_max_lots_entry = tk.Entry(self.edit_frame, width=12)
        self.edit_max_lots_entry.grid(row=1, column=5, sticky='ew')

        self.edit_entries = [
            self.edit_product_entry,
            self.edit_code_entry, 
            self.edit_material_entry,
            self.edit_target_lbs_entry,
            self.edit_min_lbs_entry,
            self.edit_max_lots_entry] # list of entries for batch handling

        self.edit_save_button = tk.Button(self.edit_frame, text='Save', width=20, command=self.save).grid(row=2, column=5, pady=(5,0), sticky='es')

    def save(self):
        product = self.edit_product_entry.get()
        code = self.edit_code_entry.get()
        material = self.edit_material_entry.get()
        target_lbs = float(self.edit_target_lbs_entry.get())
        min_lbs = float(self.edit_min_lbs_entry.get())
        max_lots = int(self.edit_max_lots_entry.get())

        product = [product, code, material, target_lbs, min_lbs, max_lots]

        if self.id:
            self.db.update_product(self.id, product)
        else:
            self.db.add_product(*product)

        self.refresh()
        self.clear_edits()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.products = self.db.get_products()
        for product in self.products:
            self.tree.insert('', tk.END, values=product)

    def clear_edits(self):
        for entry in self.edit_entries:
            entry.delete(0, tk.END)
            self.id = None

    def get_selected_item(self):
        for selected_item in self.tree.selection():
            item = self.tree.item(selected_item)['values']
            id = item[0]
            return id, item[1::]
        
    def start_edit(self):
        self.clear_edits()
        id, product = self.get_selected_item()
        self.id = id # store id of item being edited
        for entry, data in zip(self.edit_entries, product):
            entry.insert(0, data)
        
    def delete(self):
        if self.tree.selection():
            for selected_item in self.tree.selection():
                item = self.tree.item(selected_item)
                id = item['values'][0]
                self.db.delete_product(id)
        self.refresh()