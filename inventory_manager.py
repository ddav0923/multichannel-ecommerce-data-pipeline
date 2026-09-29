import sqlite3

DB_NAME = 'inventory_system.db'

def get_db_connection():
    """Connects to SQLite and enforces foreign key constraints."""
    conn = sqlite3.connect(DB_NAME)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def add_master_item(sku: str, item_name: str, cost_of_goods: float, quantity: int = 1):
    """Inserts a new product into the master inventory table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO master_inventory (sku, item_name, cost_of_goods, quantity_in_stock)
        VALUES (?, ?, ?, ?)
    """
    try:
        cursor.execute(query, (sku, item_name, cost_of_goods, quantity))
        conn.commit()
        print(f"📦 Added SKU '{sku}' ({item_name}) to Master Inventory.")
    except sqlite3.IntegrityError:
        print(f"⚠️ Error: SKU '{sku}' already exists.")
    finally:
        conn.close()

def link_ebay_listing(ebay_item_id: str, sku: str, price: float):
    """Links an active eBay listing to an existing SKU in master inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO ebay_listings (ebay_item_id, sku, current_price)
        VALUES (?, ?, ?)
    """
    try:
        cursor.execute(query, (ebay_item_id, sku, price))
        conn.commit()
        print(f"🔗 Linked eBay Item {ebay_item_id} -> SKU {sku}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Link Failed: Foreign Key Error. Ensure SKU '{sku}' exists in master_inventory first.")
    finally:
        conn.close()

if __name__ == "__main__":
    print("--- Running Inventory Insertion Tests ---")
    add_master_item("SKU-VINTAGE-001", "Vintage Denim Jacket - Size L", 18.50, 1)
    link_ebay_listing("EBAY-29481029", "SKU-VINTAGE-001", 49.99)
