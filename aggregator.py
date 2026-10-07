import sqlite3

DB_NAME = 'inventory_system.db'

def get_inventory_metrics():
    """Calculates core business metrics for inventory and multi-channel listings."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = """
        SELECT 
            COUNT(m.sku) AS total_skus,
            SUM(m.quantity_in_stock) AS total_units_in_stock,
            SUM(m.cost_of_goods * m.quantity_in_stock) AS total_cogs_value,
            SUM(e.current_price * m.quantity_in_stock) AS total_ebay_potential_value,
            SUM(p.current_price * m.quantity_in_stock) AS total_poshmark_potential_value
        FROM master_inventory m
        LEFT JOIN ebay_listings e ON m.sku = e.sku
        LEFT JOIN poshmark_listings p ON m.sku = p.sku;
    """
    
    cursor.execute(query)
    row = cursor.fetchone()
    conn.close()

    total_skus, total_units, total_cogs, ebay_val, posh_val = row

    print("\n--- 📊 Executive Inventory Metrics ---")
    print(f"Total Unique SKUs: {total_skus or 0}")
    print(f"Total Units in Stock: {total_units or 0}")
    print(f"Total Invested Capital (COGS): ${total_cogs or 0.00:.2f}")
    print(f"Potential eBay Revenue: ${ebay_val or 0.00:.2f}")
    print(f"Potential Poshmark Revenue: ${posh_val or 0.00:.2f}")

if __name__ == "__main__":
    get_inventory_metrics()
