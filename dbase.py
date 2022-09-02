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
        
        if Path(self.path + 'test.db3').is_file():
            print('Database found...')
            self.cur = connect(self.path, 'test.db3')

        else:
            print('Database doesn\'t exist, creating...')
            try:
                Path(self.path).mkdir(parents=True)
            except FileExistsError:
                pass
            self.cur = connect(self.path, 'test.db3')
            self.cur.execute("CREATE TABLE product(product_item, product_code, material_item, target_lbs, min_lbs, max_lots)")
        
    def add_product(self, name, description, max_input_lots):
        data = (name, description, max_input_lots)
        self.cur.execute("INSERT INTO product VALUES(?, ?, ?)", data)
        self.con.commit()

    def get_products(self):
        res = self.cur.execute("SELECT rowid, * FROM product")
        return res.fetchall()
        
    def close(self):
        self.con.close()





