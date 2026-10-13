import sqlite3

def process_transaction(item_id, channel, quantity):
    """Processes sales across eBay/Poshmark with atomic rollback on invalid stock levels."""
    conn = sqlite3.connect('inventory.db')
    cursor = conn.cursor()
    
    try:
        conn.execute("BEGIN TRANSACTION;")
        
        # Check current stock
        cursor.execute("SELECT current_stock FROM master_inventory WHERE item_id = ?", (item_id,))
        result = cursor.fetchone()
        
        if not result or result[0] < quantity:
            raise ValueError(f"Insufficient inventory for Item ID: {item_id} on {channel}")
            
        # Update master stock
        cursor.execute("""
            UPDATE master_inventory 
            SET current_stock = current_stock - ? 
            WHERE item_id = ?
        """, (quantity, item_id))
        
        # Log channel sale
        cursor.execute("""
            INSERT INTO channel_sales (item_id, channel, quantity_sold, timestamp)
            VALUES (?, ?, ?, DATETIME('now'))
        """, (item_id, channel, quantity))
        
        conn.commit()
        print(f"Transaction successful: {quantity} units sold on {channel}")
        
    except Exception as e:
        conn.rollback()
        print(f"Transaction failed and rolled back: {e}")
    finally:
        conn.close()
