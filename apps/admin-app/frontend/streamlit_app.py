import streamlit as st
import requests
import pandas as pd
from streamlit_autorefresh import st_autorefresh

API_URL = "http://localhost:5000/api"

st.set_page_config(page_title="Aagaaram Admin Dashboard")
st.title("🍽️ Aagaaram Admin Dashboard")

if st.button("Refresh Orders"):
    orders = requests.get(f"{API_URL}/orders").json()
else:
    orders = []  # or keep last-fetched data via session_state

# --- Menu Management ---
st.subheader("Menu Management")
with st.form("add_food", clear_on_submit=True):
    name = st.text_input("Dish Name")
    price = st.number_input("Price", min_value=1)
    if st.form_submit_button("Add Dish"):
        resp = requests.post(f"{API_URL}/foods", json={"name": name, "price": price})
        if resp.ok:
            st.success(f"Added: {resp.json()['name']} (₹{resp.json()['price']})")

if st.button("Refresh Menu"):
    foods = requests.get(f"{API_URL}/foods").json()
    df_food = pd.DataFrame(foods)
    st.table(df_food)

# --- Orders & EDA ---
st.subheader("Orders Overview")
orders = requests.get(f"{API_URL}/orders").json()

if orders:
    df_orders = pd.DataFrame(orders)
    st.dataframe(df_orders)
    st.bar_chart(df_orders['table_no'].value_counts())
else:
    st.info("No orders yet.")
