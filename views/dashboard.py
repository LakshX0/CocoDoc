import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# MySQL Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="root",       # Replace with your MySQL username
        password="Lakshan@2024",  # Replace with your MySQL password
        database="cocodoc_db"  # Replace with your MySQL database name
    )

# Fetch admin data from MySQL
def verify_login(username, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin_cred WHERE username=%s AND password=%s", (username, password))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

# Fetch prediction statistics for dashboard
def fetch_dashboard_data():
    conn = create_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch total predictions
    cursor.execute("SELECT COUNT(*) AS total_predictions FROM predictions")
    total_predictions = cursor.fetchone()["total_predictions"]

    # Fetch count of each disease
    cursor.execute("SELECT predicted_class, COUNT(*) AS count FROM predictions GROUP BY predicted_class")
    disease_counts = cursor.fetchall()

    # Fetch last 5 predictions
    cursor.execute("SELECT timestamp, predicted_class, confidence, is_healthy FROM predictions ORDER BY timestamp DESC LIMIT 5")
    recent_predictions = cursor.fetchall()

    cursor.close()
    conn.close()

    return total_predictions, disease_counts, recent_predictions

# Render login page
def render_login():
    st.title("Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if verify_login(username, password):
            st.success("Logged in successfully")
            st.session_state["is_logged_in"] = True
            render_dashboard()
        else:
            st.error("Invalid credentials")

# Render admin dashboard
def render_dashboard():
    st.title("Admin Dashboard") 
    st.write("Welcome to the Admin Dashboard!")
    
    # Fetch data for dashboard
    total_predictions, disease_counts, recent_predictions = fetch_dashboard_data()

    # Display total predictions
    st.subheader(f"Total Predictions Made: {total_predictions}")

    # Display disease counts
    st.subheader("Diseases Detected:")
    for disease in disease_counts:
        st.write(f"{disease['predicted_class']}: {disease['count']}")

    # Pie chart for disease distribution
    if disease_counts:
        disease_df = pd.DataFrame(disease_counts)
        fig = px.pie(disease_df, values='count', names='predicted_class', title="Disease Distribution")
        st.plotly_chart(fig)

    # Display recent activity
    st.subheader("Recent Predictions:")
    recent_predictions_df = pd.DataFrame(recent_predictions)
    st.table(recent_predictions_df)

    # Option to download the recent predictions as a CSV
    st.subheader("Download Recent Predictions Report")
    csv = recent_predictions_df.to_csv(index=False)
    st.download_button(
        label="Download Predictions as CSV",
        data=csv,
        file_name="recent_predictions.csv",
        mime="text/csv"
    )

    # Admin actions
    st.subheader("Admin Actions")
    st.write("Here you can manage users and upload new models.")

    if st.button("Logout"):
        st.session_state["is_logged_in"] = False
        st.experimental_rerun()

# Check login status
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False

if st.session_state["is_logged_in"]:
    render_dashboard()
else:
    render_login()