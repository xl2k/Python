import streamlit as st

st.markdown("# Page 2 ❄️")
st.sidebar.markdown("# Page 2 ❄️")
print("getting page_2")

# Sample data: Categories and corresponding subcategories
CATEGORIES = {
    "Electronics": ["Phones", "Laptops", "Cameras"],
    "Clothing": ["Shirts", "Pants", "Shoes"],
    "Home Appliances": ["Refrigerators", "Microwaves", "Washing Machines"]
}

# Streamlit UI
st.title("📌 Dynamic Filtering with Dependent Dropdowns")

# Dropdown for selecting a category
selected_category = st.selectbox("Select a Category:", options=[""] + list(CATEGORIES.keys()))

# Dynamically update subcategories based on the selected category
if selected_category:
    subcategories = CATEGORIES[selected_category]
    selected_subcategory = st.selectbox("Select a Subcategory:", options=subcategories)
    
    # Display the selection
    st.write(f"**You selected:** {selected_category} → {selected_subcategory}")
else:
    st.warning("Please select a category to see subcategories.")
