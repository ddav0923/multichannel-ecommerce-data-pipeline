import sqlite3

DB_NAME = 'inventory_system.db'

def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Enforce foreign key constraints
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 1. Master Inventory Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS master_inventory (
            sku TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            cost_of_goods REAL NOT NULL,
            quantity_in_stock INTEGER NOT NULL DEFAULT 1
        );
    """)
    
    # 2. eBay Listings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ebay_listings (
            ebay_item_id TEXT PRIMARY KEY,
            sku TEXT NOT NULL,
            current_price REAL NOT NULL,
            FOREIGN KEY (sku) REFERENCES master_inventory(sku) ON DELETE CASCADE
        );
    """)
    
    # 3. Poshmark Listings Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS poshmark_listings (
            poshmark_listing_id TEXT PRIMARY KEY,
            sku TEXT NOT NULL,
            current_price REAL NOT NULL,
            FOREIGN KEY (sku) REFERENCES master_inventory(sku) ON DELETE CASCADE
        );
    """)
    
    conn.commit()
    conn.close()
    print("💾 Database file initialized successfully...")
    print("✅ All relational tables created cleanly!")

if __name__ == "__main__":
    create_tables()