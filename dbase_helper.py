import dbase

db = dbase.Database()

data = [
    ("1534", "P2362W-190-003", "1572", 634.5, 568.7, 2),
    ("1535", "P2362W-190-003", "1572", 380.7, 343.1, 2),
    ("1541", "P2362W-190-003", "1572", 47.0, 42.3, 2),
]

# db.add_products(data)

# db.add_product('1111', 'Test Product', '5555', 500, 450, 2)

# db.update_product_max_lots(1, 42)

# db.delete_product(2)

# db.delete_products()

# print(db.get_product(8))

print(db.get_products())
