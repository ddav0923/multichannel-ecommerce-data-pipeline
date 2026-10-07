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

def link_poshmark_listing(poshmark_listing_id: str, sku: str, price: float):
    """Links an active Poshmark listing to an existing SKU in master inventory."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        INSERT INTO poshmark_listings (poshmark_listing_id, sku, current_price)
        VALUES (?, ?, ?)
    """
    try:
        cursor.execute(query, (poshmark_listing_id, sku, price))
        conn.commit()
        print(f"🔗 Linked Poshmark Item {poshmark_listing_id} -> SKU {sku}")
    except sqlite3.IntegrityError:
        print(f"⚠️ Link Failed: Foreign Key Error. Ensure SKU '{sku}' exists in master_inventory first.")
    finally:
        conn.close()

def get_inventory_summary():
    """Performs a LEFT JOIN to report live channel listings across eBay and Poshmark."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            m.sku,
            m.item_name,
            m.quantity_in_stock,
            e.ebay_item_id,
            p.poshmark_listing_id
        FROM master_inventory m
        LEFT JOIN ebay_listings e ON m.sku = e.sku
        LEFT JOIN poshmark_listings p ON m.sku = p.sku
    """
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()

    print("\n--- Current Multi-Channel Inventory Summary ---")
    for row in records:
        print(f"SKU: {row[0]} | Name: {row[1]} | Qty: {row[2]} | eBay ID: {row[3]} | Poshmark ID: {row[4]}")

if __name__ == "__main__":
    print("--- Running Inventory Insertion Tests ---")
    add_master_item("SKU-VINTAGE-001", "Vintage Denim Jacket - Size L", 18.50, 1)
    link_ebay_listing("EBAY-29481029", "SKU-VINTAGE-001", 49.99)
    link_poshmark_listing("POSH-987654", "SKU-VINTAGE-001", 55.00)
    
    # Show initial state
    get_inventory_summary()

    # Record sale for existing item
    record_sale("SKU-VINTAGE-001", "Poshmark")

    # Show updated state
    get_inventory_summary()

def record_sale(sku: str, channel: str):
    """Decrements quantity_in_stock in master inventory when an item sells."""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Fetch using quantity_in_stock
        cursor.execute("SELECT quantity_in_stock FROM master_inventory WHERE sku = ?;", (sku,))
        result = cursor.fetchone()

        if not result:
            print(f"❌ Error: SKU '{sku}' not found in master inventory.")
            return

        current_qty = result[0]

        if current_qty <= 0:
            print(f"⚠️ Warning: SKU '{sku}' is already out of stock!")
            return

        # 2. Update using quantity_in_stock
        new_qty = current_qty - 1
        cursor.execute(
            "UPDATE master_inventory SET quantity_in_stock = ? WHERE sku = ?;",
            (new_qty, sku)
        )

        print(f"\n✅ Sale recorded on {channel} for SKU '{sku}'. New master quantity: {new_qty}")

        if new_qty == 0:
            print(f"🛑 SKU '{sku}' reached 0 stock.")

        conn.commit()

    except sqlite3.Error as e:
        conn.rollback()
        print(f"❌ Database error during sale recording: {e}")
    finally:
        conn.close()
        
# ==========================================
# 2. TESTING BLOCK (EXECUTES WHEN YOU RUN FILE)
# ==========================================
if __name__ == "__main__":
    # Test recording a sale on an existing SKU
    record_sale("TSHIRT-BLK-M", "Poshmark")
