import sqlite3

def init_crosslisting_database():
    # 1. Connect to SQLite (This automatically creates a file named 'inventory_system.db')
    conn = sqlite3.connect('inventory_system.db')
    cursor = conn.cursor()
    print("💾 Database file initialized successfully...")

    # 2. CIS Architecture: Create the Master Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS master_inventory (
            sku TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            cost_of_goods REAL,
            quantity_in_stock INTEGER DEFAULT 1
        )
    ''')

    # 3. Relational Logic: Create the eBay Table (linked via SKU)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ebay_listings (
            ebay_item_id TEXT PRIMARY KEY,
            sku TEXT,
            current_price REAL,
            FOREIGN KEY (sku) REFERENCES master_inventory(sku)
        )
    ''')

    # 4. Relational Logic: Create the Poshmark Table (linked via SKU)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS poshmark_listings (
            poshmark_id TEXT PRIMARY KEY,
            sku TEXT,
            current_price REAL,
            FOREIGN KEY (sku) REFERENCES master_inventory(sku)
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("✅ All relational tables created cleanly!")

if __name__ == "__main__":
    init_crosslisting_database()
