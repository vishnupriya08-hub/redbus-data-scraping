import streamlit as st
import mysql.connector
import pandas as pd

# Function to connect to the MySQL database
def get_database_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345678",
        database="Redbus"
    )

# Function to retrieve data from the database with dynamic filters
def get_filtered_data(bustype, route, price_range, star_rating, availability):
    con = get_database_connection()
    cursor = con.cursor(dictionary=True)
    
    query = "SELECT * FROM bus_routes WHERE 1=1"
    params = []

    # Apply filters dynamically
    if bustype:
        query += " AND bustype LIKE %s"
        params.append(f"{bustype}%")
    if route:
        query += " AND route_name LIKE %s"
        params.append(f"%{route}%")
    if price_range:
        query += " AND price BETWEEN %s AND %s"
        params.extend(price_range)
    if star_rating:
        query += " AND star_rating <= %s"
        params.append(star_rating)
    if availability:
        query += " AND seats_available > 0"
    
    cursor.execute(query, params)
    result = cursor.fetchall()
    con.close()
    return result

# Streamlit application layout
st.title("Redbus Data Filtering and Analysis")

# User inputs for filters
bustype = st.selectbox("Select Bus Type", options=["","A/C Seater","A/C Sleeper","Non A/C Seater","Non A/C Sleeper","Electric A/C Seater","Electric A/C Sleeper","Volvo A/C Semi Sleeper","Volvo Multi Axle A/C Sleeper","NON A/C Semi Sleeper","NON A/C Push Back","Scania Multi-Axle AC Semi Sleeper","VE A/C Sleeper","Bharat Benz A/C Sleeper","Volvo Multi-Axle A/C Sleeper","A/C Semi Sleeper"])
route = st.text_input("Enter Route")
price_range = st.slider("Select Price Range", 0, 5000, (0, 5000))
star_rating = st.slider("Select Minimum Star Rating", 0.0, 5.0, 0.0)
availability = st.checkbox("Show only buses with available seats")

# Fetch and display filtered data
if st.button("Apply Filters"):
    data = get_filtered_data(bustype, route, price_range, star_rating, availability)
    if data:
        df = pd.DataFrame(data)
        st.write(f"Showing {len(data)} results:")
        st.dataframe(df)
    else:
        st.write("No results found.")

# Display all data initially
else:
    data = get_filtered_data(None, None, (0, 5000), 0.0, False)
    df = pd.DataFrame(data)
    st.write(f"Showing all {len(data)} results:")
    st.dataframe(df)
