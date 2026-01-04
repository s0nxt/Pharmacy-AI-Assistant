import pandas as pd
import os
from datetime import datetime

MEDICINE_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "medicine_master.csv")
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "order_history.csv")

def get_medicine_data():
    return pd.read_csv(MEDICINE_FILE)

def update_medicine_stock(medicine_name, quantity_reduced):
    df = pd.read_csv(MEDICINE_FILE)
    if medicine_name in df['name'].values:
        idx = df[df['name'] == medicine_name].index[0]
        if df.at[idx, 'stock_level'] >= quantity_reduced:
            df.at[idx, 'stock_level'] -= quantity_reduced
            df.to_csv(MEDICINE_FILE, index=False)
            return True, "Stock updated"
        return False, "Insufficient stock"
    return False, "Medicine not found"

def get_order_history():
    return pd.read_csv(HISTORY_FILE)

def add_order_to_history(customer_id, customer_name, customer_phone, medicine_name, quantity, dosage_frequency):
    df = pd.read_csv(HISTORY_FILE)
    new_order = {
        "order_id": f"ORD{len(df) + 1:03d}",
        "customer_id": customer_id,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "medicine_name": medicine_name,
        "quantity": quantity,
        "dosage_frequency": dosage_frequency,
        "last_purchase_date": datetime.now().strftime("%Y-%m-%d")
    }
    df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
    df.to_csv(HISTORY_FILE, index=False)
    return new_order

def get_proactive_refills():
    df_history = pd.read_csv(HISTORY_FILE)
    df_meds = pd.read_csv(MEDICINE_FILE)
    
    today = datetime.now()
    alerts = []
    
    for _, row in df_history.iterrows():
        # Simple logic: if last_purchase_date + duration (qty / freq) is near today
        try:
            last_date = datetime.strptime(row['last_purchase_date'], "%Y-%m-%d")
            # Parse dosage_frequency (e.g. "1 per day")
            freq_str = str(row['dosage_frequency']).lower()
            if "per day" in freq_str:
                per_day = float(freq_str.split()[0])
                days_supply = row['quantity'] / per_day
                days_passed = (today - last_date).days
                
                if days_passed >= (days_supply - 3): # Alert 3 days before running out
                    alerts.append({
                        "customer_name": row['customer_name'],
                        "medicine_name": row['medicine_name'],
                        "days_remaining": max(0, int(days_supply - days_passed))
                    })
        except Exception as e:
            print(f"Error processing refill for {row['customer_name']}: {e}")
            
    return alerts
