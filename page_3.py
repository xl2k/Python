import streamlit as st

st.set_page_config(layout="wide")


# Sample tile data
tiles = [
    {"title": "Tile 1", "description": "This is tile 1.", "image": "https://via.placeholder.com/150"},
    {"title": "Tile 2", "description": "This is tile 2.", "image": "https://via.placeholder.com/150"},
    {"title": "Tile 3", "description": "This is tile 3.", "image": "https://via.placeholder.com/150"},
    {"title": "Tile 4", "description": "This is tile 4.", "image": "https://via.placeholder.com/150"},
    {"title": "Tile 5", "description": "This is tile 5.", "image": "https://via.placeholder.com/150"},
    {"title": "Tile 6", "description": "This is tile 6.", "image": "https://via.placeholder.com/150"},
]

# Page Title
st.title("📌 Tile-Based UI in Streamlit")

# Create a grid layout (3 tiles per row)
cols = st.columns(3)

# Display tiles dynamically
for index, tile in enumerate(tiles):
    with cols[index % 3]:  # Place in one of the three columns
        st.image(tile["image"])
        st.subheader(tile["title"])
        st.write(tile["description"])
        st.button(f"More Info", key=f"btn_{index}")

