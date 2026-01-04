from langchain.tools import tool
from utils.database import get_medicine_data, update_medicine_stock, add_order_to_history, get_order_history
import pandas as pd

@tool
def check_inventory(medicine_name: str):
    """Checks the stock level and prescription requirement for a specific medicine."""
    df = get_medicine_data()
    med = df[df['name'].str.lower() == medicine_name.lower()]
    if not med.empty:
        return med.to_dict(orient='records')[0]
    return f"Medicine '{medicine_name}' not found."

@tool
def check_customer_history(customer_name: str):
    """Retrieves the order history for a customer to understand their recurring needs."""
    df = get_order_history()
    history = df[df['customer_name'].str.lower() == customer_name.lower()]
    if not history.empty:
        return history.to_dict(orient='records')
    return f"No history found for customer '{customer_name}'."

@tool
def place_order(customer_name: str, medicine_name: str, quantity: int, dosage_frequency: str = "1 per day"):
    """
    Executes an order: updates stock and records the transaction.
    Should only be called after verifying inventory and prescription if needed.
    """
    # In a real scenario, we'd have a customer_id. For mock, we'll derive/create one.
    df_history = get_order_history()
    customer_match = df_history[df_history['customer_name'].str.lower() == customer_name.lower()]
    
    if not customer_match.empty:
        customer_id = customer_match.iloc[0]['customer_id']
        customer_phone = customer_match.iloc[0]['customer_phone']
    else:
        customer_id = f"C{len(df_history['customer_id'].unique()) + 1:03d}"
        customer_phone = "+0000000000" # Placeholder

    success, message = update_medicine_stock(medicine_name, quantity)
    if success:
        order = add_order_to_history(customer_id, customer_name, customer_phone, medicine_name, quantity, dosage_frequency)
        # Mock Webhook trigger
        trigger_fulfillment_webhook(order)
        return f"Order placed successfully! Order ID: {order['order_id']}. A confirmation has been sent."
    else:
        return f"Failed to place order: {message}"

def trigger_fulfillment_webhook(order_details):
    """Mock webhook trigger for warehouse fulfillment."""
    print(f"TRIGER WEBHOOK: Sending order {order_details['order_id']} to warehouse...")
    # In a real app, use requests.post(webhook_url, json=order_details)
    pass
