import pandas as pd
import random

def generate_medicines(n=100):
    medicines = [
        "Paracetamol", "Amoxicillin", "Ibuprofen", "Metformin", "Atorvastatin",
        "Lisinopril", "Omeprazole", "Aspirin", "Cetirizine", "Azithromycin",
        "Losartan", "Albuterol", "Gabapentin", "Sertraline", "Amlodipine",
        "Furosemide", "Hydrochlorothiazide", "Levothyroxine", "Metoprolol", "Prednisone",
        "Rosuvastatin", "Simvastatin", "Tamsulosin", "Tramadol", "Warfarin",
        "Citalopram", "Escitalopram", "Fluoxetine", "Lorazepam", "Meloxicam",
        "Montelukast", "Oxycodone", "Pantoprazole", "Sildenafil", "Venlafaxine",
        "Zolpidem", "Allopurinol", "Bupropion", "Carvedilol", "Clopidogrel",
        "Dextroamphetamine", "Duloxetine", "Fenofibrate", "Glipizide", "Latanoprost",
        "Levofloxacin", "Potassium Chloride", "Propranolol", "Quetiapine", "Ranitidine",
        "Spironolactone", "Topiramate", "Valacyclovir", "Alprazolam", "Amitriptyline",
        "Baclofen", "Buspirone", "Celecoxib", "Clonazepam", "Cyclobenzaprine",
        "Doxycycline", "Ezetimibe", "Famotidine", "Hydralazine", "Hydrocodone",
        "Lansoprazole", "Methylprednisolone", "Naproxen", "Nifedipine", "Nitrofurantoin",
        "Olanzapine", "Oxybutynin", "Pioglitazone", "Pregabalin", "Sumatriptan",
        "Tizanidine", "Trazodone", "Valsartan", "Verapamil", "Warfarin",
        "Acyclovir", "Budesonide", "Cephalexin", "Digoxin", "Enalapril",
        "Fluticasone", "Glyburide", "Isosorbide Mononitrate", "Mupirocin", "Nystatin",
        "Phenytoin", "Promethazine", "Rizatriptan", "Tamoxifen", "Terazosin",
        "Theophylline", "Tolterodine", "Triamcinolone", "Triamterene", "Valproic Acid"
    ]
    
    # Fill remaining if list is shorter than n
    while len(medicines) < n:
        medicines.append(f"Medicine_{len(medicines)+1}")
        
    data = []
    for i, name in enumerate(medicines[:n]):
        data.append({
            "medicine_id": f"M{i+1:03d}",
            "name": name,
            "stock_level": random.randint(10, 500),
            "unit": random.choice(["tablet", "capsule", "ml", "ointment"]),
            "prescription_required": random.choice([True, False]),
            "price": round(random.uniform(2.0, 100.0), 2)
        })
    
    return pd.DataFrame(data)

def generate_orders(medicines_df, n=100):
    customers = [
        ("C001", "John Doe", "+1234567890"),
        ("C002", "Jane Smith", "+1987654321"),
        ("C003", "Bob Wilson", "+1122334455"),
        ("C004", "Alice Brown", "+1555666777"),
        ("C005", "Charlie Davis", "+1444333222"),
        ("C006", "David Miller", "+1666777888"),
        ("C007", "Eva Green", "+1777888999"),
        ("C008", "Frank White", "+1888999000"),
        ("C009", "Grace Lee", "+1999000111"),
        ("C010", "Henry Ford", "+1000111222")
    ]
    
    data = []
    for i in range(n):
        cust_id, cust_name, cust_phone = random.choice(customers)
        med = medicines_df.sample(1).iloc[0]
        
        # Random date in last 2 months
        days_ago = random.randint(0, 60)
        from datetime import datetime, timedelta
        order_date = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")
        
        data.append({
            "order_id": f"ORD{i+1:03d}",
            "customer_id": cust_id,
            "customer_name": cust_name,
            "customer_phone": cust_phone,
            "medicine_name": med['name'],
            "quantity": random.randint(10, 60),
            "dosage_frequency": random.choice(["1 per day", "2 per day", "1 every 8 hours", "As needed"]),
            "last_purchase_date": order_date
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    import os
    base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(base_dir, exist_ok=True)
    
    meds_df = generate_medicines(100)
    meds_df.to_csv(os.path.join(base_dir, "medicine_master.csv"), index=False)
    
    orders_df = generate_orders(meds_df, 100)
    orders_df.to_csv(os.path.join(base_dir, "order_history.csv"), index=False)
    
    print(f"Generated 100 rows for medicine_master.csv and order_history.csv in {base_dir}")
