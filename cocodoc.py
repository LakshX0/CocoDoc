import streamlit as st
from PIL import Image
import os
from views import about, prediction, dashboard, contact

# st.set_page_config(page_title="CocoDoc", page_icon="🌴")

# Initialize session state for page and login
if "page" not in st.session_state:
    st.session_state["page"] = "about"  # Default page

if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False  # Login state

# Load logo
logo_path = os.path.join("assets", "cocodoc-logo.png")
logo = Image.open(logo_path)

# Layout
st.sidebar.image(logo, caption="Coconut Disease Predictor", width=100)  # Resize as needed

# Navigation
st.sidebar.title("Navigation")
navigation = st.sidebar.selectbox("Select a page:", ["About Us", "Prediction", "Contact Us", "Admin"])

if navigation == "About Us":
    st.session_state["page"] = "about"
elif navigation == "Prediction":
    st.session_state["page"] = "prediction"
elif navigation == "Contact Us":
    st.session_state["page"] = "contact"
elif navigation == "Admin":
    st.session_state["page"] = "dashboard"

# Inject custom HTML and CSS for top-right Admin button (if still needed)
# st.markdown("""
#     <style>
#     .admin-button {
#         position: fixed;
#         top: 10px;
#         right: 10px;
#         background-color: #FF4B4B;
#         color: white;
#         padding: 10px 20px;
#         border: none;
#         border-radius: 5px;
#         cursor: pointer;
#         font-size: 16px;
#         z-index: 1000;  /* Ensure button is above other elements */
#         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
#     }
#     .admin-button:hover {
#         background-color: #FF6B6B;
#     }
#     </style>
#     <button class="admin-button" onclick="window.location.href='/?page=dashboard'">Admin</button>
# """, unsafe_allow_html=True)

st.sidebar.text("Copyright @ 2024")

# Handle page rendering based on session state
if st.session_state["page"] == "about":
    about.render()
elif st.session_state["page"] == "prediction":
    prediction.render()  # This now points to the updated prediction logic
elif st.session_state["page"] == "contact":
    contact.render()
elif st.session_state.get("page") == "dashboard":
    if st.session_state["is_logged_in"]:
        dashboard.render_dashboard()
    else:
        dashboard.render_login()
