import streamlit as st
from datetime import datetime, timedelta

# Data for dropdowns
car_options = ["AC Sedan car", "AC Ertiga Car", "AC Innova Crysta", "AC Tempo Travel"]
hotel_options = [
    "Non AC Hotel room",
    "Standard AC Hotel room",
    "3star AC Hotel room",
    "3star AC Hotel room with Breakfast",
    "4star AC Hotel room with Breakfast",
    "5star AC Hotel room with Breakfast"
]
city_options = ["Indore", "Ujjain", "Omkareshwar", "Bhopal"]
bhasma_types = ["Ticket", "Pandit ji", "Nandi hall"]

# Streamlit UI
st.title("Travel Package Input")

# Car Type
car_type = st.selectbox("Car Type", car_options)

# Hotel Type
hotel_type = st.selectbox("Hotel Type", hotel_options)

# Room Type
room_type = st.text_input("Room Type", "e.g., Double occupancy 1 room")

# Bhasmarathi requirement
bhasmarathi_required = st.selectbox("Bhasmarathi Requirement", ["Yes", "No"])

# Bhasmarathi Type
bhasmarathi_type = st.selectbox("Bhasmarathi Type", bhasma_types)

# Arrival Date
arrival_date = st.date_input("Arrival Date", datetime.today())

# Arrival Time
arrival_time = st.time_input("Arrival Time", datetime.now().time())

# Departure Time
departure_time = st.time_input("Departure Time", datetime.now().time())

# Total Days
total_days = st.selectbox("Total Days of Travel", range(1, 11))
total_nights = total_days - 1

# Total Pax
total_pax = st.number_input("Total Pax", min_value=1, step=1)

# Arrival and Departure City
arrival_city = st.selectbox("Arrival City", city_options)
departure_city = st.selectbox("Departure City", city_options)

# Costs
package_car_cost = st.number_input("Package Car Cost", min_value=0)
actual_car_cost = st.number_input("Actual Car Cost", min_value=0)
package_hotel_cost = st.number_input("Package Hotel Cost", min_value=0)
actual_hotel_cost = st.number_input("Actual Hotel Cost", min_value=0)
package_bhasmarathi_cost = st.number_input("Package Bhasmarathi Cost", min_value=0)
actual_bhasmarathi_cost = st.number_input("Actual Bhasmarathi Cost", min_value=0)

# Auto Calculations
departure_date = arrival_date + timedelta(days=total_days)
day_labels = [(f"Day {i+1}", (arrival_date + timedelta(days=i)).strftime("%Y-%m-%d")) for i in range(total_days)]

st.subheader("Auto Calculations")
st.write(f"Total Nights: {total_nights}")
st.write(f"Departure Date: {departure_date.strftime('%Y-%m-%d')}")
for day, date in day_labels:
    st.write(f"{day}: {date}")

# Submit button
if st.button("Submit"):
    st.success("Form submitted successfully!")
