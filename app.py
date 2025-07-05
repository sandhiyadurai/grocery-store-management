import streamlit as st
import pandas as pd

# Load item data
items_df = pd.read_csv("items.csv")

st.set_page_config(page_title="🛒 Grocery Store App", layout="centered")
st.title("🛍️ Grocery Store Billing System")

st.subheader("📋 Available Items")
st.dataframe(items_df)

# User cart
st.subheader("🛒 Add Items to Cart")
cart = {}

for index, row in items_df.iterrows():
    qty = st.number_input(f"{row['Item']} (₹{row['Price']})", 0, row['Stock'], step=1)
    if qty > 0:
        cart[row['Item']] = {"qty": qty, "price": row['Price']}

# Show Bill
if st.button("Generate Bill"):
    if not cart:
        st.warning("Please add at least one item to the cart.")
    else:
        st.subheader("🧾 Your Bill Receipt")

        bill = []
        total = 0

        for item, details in cart.items():
            qty = details["qty"]
            price = details["price"]
            amount = qty * price
            total += amount
            bill.append([item, qty, price, amount])

        bill_df = pd.DataFrame(bill, columns=["Item", "Qty", "Price", "Amount"])
        bill_df.loc[len(bill_df.index)] = ["Total", "", "", total]

        st.dataframe(bill_df)

        # Save to CSV (works without openpyxl)
        csv = bill_df.to_csv(index=False).encode('utf-8')
        st.download_button("💾 Download Bill as CSV", data=csv, file_name="grocery_bill.csv", mime='text/csv')

