import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:5000/api"

st.set_page_config(page_title="Aagaaram Admin Dashboard")
st.title("🍽️ Aagaaram Admin Dashboard")

# --- navigation ---
page = st.sidebar.radio("Navigate to", ["Menu", "Servers", "Orders"])

if page == "Menu":
    st.header("📋 Menu Management")
    with st.form("add_food", clear_on_submit=True):
        name        = st.text_input("Dish Name")
        price       = st.number_input("Price", min_value=1)
        description = st.text_area("Description")
        image       = st.file_uploader("Upload Food Image", type=["png","jpg","jpeg"])
        if st.form_submit_button("Add Dish"):
            if not image:
                st.error("Image is required.")
            else:
                form_data = {"name": name, "price": price, "description": description}
                resp = requests.post(f"{API_URL}/foods", data=form_data, files={"image": image})
                if resp.ok:
                    st.success(f"Added: {resp.json()['name']} (₹{resp.json()['price']})")
                else:
                    st.error(f"Failed: {resp.text}")
    st.header(" Menu Overview")
    if st.button("Refresh Menu"):
        foods = requests.get(f"{API_URL}/foods").json()
    else:
        foods = requests.get(f"{API_URL}/foods").json()
    if foods:
        df_foods = pd.DataFrame(foods)
        st.dataframe(df_foods)
        # st.bar_chart(df_foods["table_no"].value_counts())
    else:
        st.info("No orders yet.")

elif page == "Servers":
    st.header("👨‍🍳 Server Management")
    with st.form("add_server", clear_on_submit=True):
        server_name = st.text_input("Server Name")
        age = st.number_input("Age", min_value=18, max_value=100)
        if st.form_submit_button("Add Server"):
            resp = requests.post(f"{API_URL}/servers", json={"name": server_name, "age": age})
            if resp.ok:
                st.success(f"Added Server: {resp.json()['name']}")

elif page == "Orders":
    st.header("🛎 Orders Overview")
    if st.button("Refresh Orders"):
        orders = requests.get(f"{API_URL}/orders").json()
    else:
        orders = requests.get(f"{API_URL}/orders").json()
    if orders:
        df_orders = pd.DataFrame(orders)
        st.dataframe(df_orders)
        st.bar_chart(df_orders["table_no"].value_counts())
    else:
        st.info("No orders yet.")
