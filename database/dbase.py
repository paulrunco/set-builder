from pathlib import Path
import sqlite3

class Database:

    def __init__(self) -> sqlite3.Cursor:

        self.home = str(Path.home())
        self.path = self.home + '\.web\set-builder\\'

        def connect(path, dbase):
            self.con = sqlite3.connect(path + dbase)
            print('Connected!')
            return self.con.cursor()
        
        if Path(self.path + 'database.db3').is_file():
            print('Database found...')
            self.cur = connect(self.path, 'database.db3')

        else:
            print('Database doesn\'t exist, creating...')
            try:
                Path(self.path).mkdir(parents=True)
            except FileExistsError:
                pass
            self.cur = connect(self.path, 'database.db3')
            self.cur.execute("CREATE TABLE product(product, code, material, target_lbs, min_lbs, max_lots)")
        
    def add_product(self, product:str, code:str, material:str, target_lbs:float, min_lbs:float, max_lots:int):
        data = (product, code, material, target_lbs, min_lbs, max_lots)
        self.cur.execute("INSERT INTO product VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()

    def add_products(self, data):
        self.cur.executemany("INSERT INTO product VALUES(?, ?, ?, ?, ?, ?)", data)
        self.con.commit()

    def get_product(self, id):
        res = self.cur.execute("SELECT rowid, * from product WHERE rowid=?", str(id))
        return res.fetchall()

    def get_products_with_name(self, product):
        res = self.cur.execute("SELECT rowid, * from product WHERE product=?", (product,))
        return res.fetchall()

    def get_product_with_name_material(self, product, material):
        res = self.cur.execute("SELECT rowid, * from product WHERE product=? AND material=?", (product, material))
        return res.fetchall()
        
    def get_products(self):
        res = self.cur.execute("SELECT rowid, * FROM product")
        return res.fetchall()

    # Because SQLite does not allow column names to be parameterized, and string
    # interpolation would be vulnerable to injection, each field has its own update
    # function which is wrapped into a single update function.
    def update_product(self, id, values):
        self.update_product_name(id, values[0])
        self.update_product_code(id, values[1])
        self.update_product_material(id, values[2])
        self.update_product_target_lbs(id, values[3])
        self.update_product_min_lbs(id, values[4])
        self.update_product_max_lots(id, values[5])

    def update_product_name(self, id, value):
        data = (value, id)
        self.cur.execute("UPDATE product SET product = ? WHERE rowid = ?", data)
        self.con.commit()

    def update_product_code(self, id, value):
        data = (value, id)
        self.cur.execute("UPDATE product SET code = ? WHERE rowid = ?", data)
        self.con.commit()

    def update_product_material(self, id, value):
        data = (value, id)
        self.cur.execute("UPDATE product SET material = ? WHERE rowid = ?", data)
        self.con.commit()

    def update_product_target_lbs(self, id, value):
        data = (value, id)
        self.cur.execute("UPDATE product SET target_lbs = ? WHERE rowid = ?", data)
        self.con.commit()

    def update_product_min_lbs(self, id, value):
        data = (value, id)
        self.cur.execute("UPDATE product SET min_lbs = ? WHERE rowid = ?", data)
        self.con.commit()

    def update_product_max_lots(self, id, value):
        data = (value, id)
        self.cur.execute("UPDATE product SET max_lots = ? WHERE rowid = ?", data)
        self.con.commit()

    def delete_product(self, id):
        self.cur.execute("DELETE FROM product WHERE rowid=?", (id,))
        self.con.commit()

    def delete_products(self):
        self.cur.execute("DELETE FROM product")
        self.con.commit()
        
    def close(self):
        self.con.close()





