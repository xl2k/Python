import streamlit as st
import streamlit.components.v1 as components

# HTML and JavaScript code for the pushable tile
html_code = """
<div id="tile" style="width: 100px; height: 100px; background-color: #f85f73; text-align: center; line-height: 100px; cursor: pointer;">
    Push Me
</div>
<script>
    document.getElementById("tile").onclick = function() {
        this.style.transform = "translateX(100px)";
    }
</script>
"""

# Display the HTML code in Streamlit
components.html(html_code, height=150)
