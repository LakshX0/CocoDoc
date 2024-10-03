import streamlit as st
from PIL import Image
import base64

# Function to convert an image to a base64 string
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def render():
    # Load cover image
    cover_image = Image.open("assets/coco_bg.jpg")  # Update the path to your cover image
    st.image(cover_image, use_column_width=True)

    st.title("About CocoDoc")

    # Convert image to base64 for HTML use
    image_base64 = image_to_base64("assets/4.png")

    # Use a container to manage layout and spacing
    with st.container():
        # Create two columns with custom widths and spacing
        col1, col2 = st.columns([1, 1], gap="large")

        with col1:
            # CSS for custom div and columns inside col1
            st.markdown(f"""
            <style>
            .outer-div {{
                border: 2px solid #00b8a5;
                border-radius: 15px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
                background-color: #0E1117;
            }}
            .row {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .column-left {{
                width: 45%;
            }}
            .column-right {{
                width: 50%;
                background-color: #0E1117;
                padding: 10px;
                border-radius: 10px;
            }}
            img {{
                border-radius: 10px;
                width: 100%;
            }}
            </style>
            
            <div class="outer-div">
                <div class="row">
                    <div class="column-left">
                        <img src="data:image/png;base64,{image_base64}" alt="Coconut image">
                    </div>
                    <div class="column-right">
                        <p>Sri lanka is the 4th largest coconut exporter in the world.</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Another image below the div
            st.image("./assets/coco-stat.jpg", use_column_width=True)  # Adjust image width to fill column
            st.write("Annual coconut production 2011 - 2021")

        with col2:
            st.write(
                """
                Welcome to CocoDoc, your go-to platform for coconut leaf disease prediction and management. 
                Our web app leverages advanced image processing and machine learning algorithms to provide farmers, 
                agricultural professionals, and enthusiasts with accurate and timely diagnoses of various 
                coconut leaf diseases. By analyzing leaf images, we aim to help you take proactive measures 
                to protect your coconut crops, improve yields, and reduce losses.
                """
            )
            st.write(
                """
                At CocoDoc, we are passionate about combining cutting-edge technology with agricultural expertise 
                to offer practical solutions for sustainable coconut farming. Our mission is to empower the coconut 
                farming community with the tools they need to combat crop diseases efficiently and effectively.
                """
            )
            st.write(
                """
                Whether you're a small-scale farmer or part of a large agricultural enterprise, our easy-to-use 
                platform is designed to help you monitor your crops' health and ensure a brighter, healthier future 
                for your coconut plantation.
                """
            )

# Call the render function
if __name__ == "__main__":
    render()
