import streamlit as st
import re
import requests

WEBHOOK_URL = "https://connect.pabbly.com/workflow/sendwebhookdata/IjU3NjYwNTZkMDYzNTA0Mzc1MjZlNTUzMzUxMzYi_pc"

def is_valid_email(email):
    # Basic regex pattern for email validation
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(email_pattern, email) is not None

def render():
    st.title("Contact Us")
    
    st.write("""
    We would love to hear from you! If you have any questions, feedback, or need support, please fill out the contact form below.
    """)

    # Contact Form
    with st.form(key='contact_form'):
        st.subheader("Contact Form")
        
        name = st.text_input("Name")
        email = st.text_input("Email Address")
        subject = st.text_input("Subject")
        message = st.text_area("Message")

        submit_button = st.form_submit_button("Send")
        
        if submit_button:
         
            if not WEBHOOK_URL:
                st.error("Email service is not set up. Please try again later.", icon="📧")
                st.stop()

            if not name:
                st.error("Please provide your name.", icon="🧑")
                st.stop()

            if not email:
                st.error("Please provide your email address.", icon="📨")
                st.stop()

            if not is_valid_email(email):
                st.error("Please provide a valid email address.", icon="📧")
                st.stop()

            if not message:
                st.error("Please provide a message.", icon="💬")
                st.stop()

            # Prepare the data payload and send it to the specified webhook URL
            data = {"email": email, "name": name, "message": message}
            response = requests.post(WEBHOOK_URL, json=data)

            if response.status_code == 200:
                st.success("Thank you for your message! We will get back to you soon. 🎉", icon="🚀")
            else:
                st.error("There was an error sending your message.", icon="😨")
              
             