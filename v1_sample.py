import streamlit as st
import streamlit.components.v1 as components

# HTML code for the tile layout
html_code = """
<div style="display: flex; flex-wrap: wrap; gap: 10px;">
    <div style="flex: 1 1 calc(33.333% - 10px); background-color: #f8b400; padding: 20px; text-align: center;">
        <h2>Tile 1</h2>
        <p>Content for tile 1</p>
    </div>
    <div style="flex: 1 1 calc(33.333% - 10px); background-color: #f85f73; padding: 20px; text-align: center;">
        <h2>Tile 2</h2>
        <p>Content for tile 2</p>
    </div>
    <div style="flex: 1 1 calc(33.333% - 10px); background-color: #17b978; padding: 20px; text-align: center;">
        <h2>Tile 3</h2>
        <p>Content for tile 3</p>
    </div>
</div>
"""

# Display the HTML code in Streamlit
components.html(html_code, height=300)
