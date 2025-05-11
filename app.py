import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ========== Travel Code Lookup ==========

# Load Excel file from GitHub
excel_url = 'https://raw.githubusercontent.com/Arpith92/TAK_Project_Test2/main/Code.xlsx'
df = pd.read_excel(excel_url, sheet_name="Code", engine='openpyxl')

# ========== Helper Functions ==========

# Function to get itinerary details for a given day
def get_day_itinerary(code_input):
    match_row = df[df['Code'].str.lower() == code_input.lower()]
    if not match_row.empty:
        particulars = match_row.iloc[0]['Particulars']  # Assuming 'Particulars' has the itinerary list
        return particulars
    return None

# Function to generate the route from codes entered
def generate_route():
    route_parts = []
    # Collect all codes entered by the user
    for day in range(1, total_days + 1):
        code_input = st.session_state.get(f"code_day{day}", "")
        if code_input:
            match_row = df[df['Code'].str.lower() == code_input.lower()]
            if not match_row.empty:
                route = match_row.iloc[0]['Route']
                route_parts.append(route)

    # Join the route parts
    raw_route = '-'.join(route_parts).replace(' -', '-').replace('- ', '-')

    # Remove consecutive duplicate city names
    route_list = raw_route.split('-')
    cleaned_route_list = [route_list[i] for i in range(len(route_list)) if i == 0 or route_list[i] != route_list[i - 1]]

    # Final route string
    return '-'.join(cleaned_route_list)

# ========== Travel Package Input Form ==========

st.title("Travel Package Builder")

st.header("1. Package Details")

# Dropdown options
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

# User inputs
Client_Name = st.text_input("Client Name", "test1")
car_type = st.selectbox("Car Type", car_options)
hotel_type = st.selectbox("Hotel Type", hotel_options)
room_type = st.text_input("Room Type", "e.g., Double occupancy 1 room")
bhasmarathi_required = st.selectbox("Bhasmarathi Requirement", ["Yes", "No"])
bhasmarathi_type = st.selectbox("Bhasmarathi Type", bhasma_types)

arrival_date = st.date_input("Arrival Date", datetime.today())
arrival_time = st.time_input("Arrival Time", datetime.now().time())
departure_time = st.time_input("Departure Time", datetime.now().time())

total_days = st.number_input("Total Days of Travel", min_value=1, max_value=10, step=1)
total_nights = total_days - 1

total_pax = st.number_input("Total Pax", min_value=1, step=1)

day_1 = "day" if total_days == 1 else "days"
night = "" if total_nights == 0 else "night" if total_nights == 1 else "nights"
plan_night = "" if total_nights == 0 else f"and {total_nights}"

person = "person" if total_pax == 1 else "persons"

arrival_city = st.selectbox("Arrival City", city_options)
departure_city = st.selectbox("Departure City", city_options)

package_car_cost = st.number_input("Package Car Cost", min_value=0)
actual_car_cost = st.number_input("Actual Car Cost", min_value=0)
package_hotel_cost = st.number_input("Package Hotel Cost", min_value=0)
actual_hotel_cost = st.number_input("Actual Hotel Cost", min_value=0)
package_bhasmarathi_cost = st.number_input("Package Bhasmarathi Cost", min_value=0)
actual_bhasmarathi_cost = st.number_input("Actual Bhasmarathi Cost", min_value=0)

departure_date = arrival_date + timedelta(days=total_days)

# ========== Travel Code Entry Section ==========

daily_particulars = {}
grouped_itinerary = {}

for day in range(1, total_days + 1):
    code_input = st.text_input(f"Travel Code for Day {day} (e.g., ip-id)", key=f"code_day{day}")
    if code_input:
        itinerary = get_day_itinerary(code_input)
        if itinerary:
            daily_particulars[f'Day {day}'] = itinerary
            for entry in itinerary:
                # Ensure 'Date' key exists and is not 'N/A' before comparing
                if isinstance(entry, dict) and 'Date' in entry and entry['Date'] != 'N/A':
                    if pd.notna(entry['Date']):
                        date = pd.to_datetime(entry['Date']).strftime('%d-%b-%Y')
                        if date not in grouped_itinerary:
                            grouped_itinerary[date] = []
                        grouped_itinerary[date].append(f"{entry.get('Time', 'N/A')}: {entry.get('Description', 'No description available.')}")
        else:
            daily_particulars[f'Day {day}'] = 'Code not found in database.'

# ========== Auto Calculations ==========

st.header("3. Auto Calculations")

st.write(f"Total Nights: {total_nights}")
st.write(f"Departure Date: {departure_date.strftime('%Y-%m-%d')}")

for i in range(total_days):
    st.write(f"Day {i+1}: {(arrival_date + timedelta(days=i)).strftime('%Y-%m-%d')}")

# ========== Generate Route ==========

final_route = generate_route()

# ========== Output Preview ==========

st.header("4. Day-wise Itinerary Preview")
st.write(f"Greetings from TravelAajkal,")
st.write(f"Client Name: {Client_Name}")
st.write(f"Plan: {total_days} {day_1} {plan_night} {night} {final_route} for {total_pax} {person}")

if daily_particulars:
    for day, detail in daily_particulars.items():
        st.write(f"**{day}**: {detail}")

# ========== Final Submit ==========

if st.button("Submit"):
    st.success("Form submitted successfully!")
