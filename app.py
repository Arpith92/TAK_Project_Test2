import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ========== Load Excel Data ==========
excel_url = 'https://raw.githubusercontent.com/Arpith92/TAK_Project_Test2/main/Code.xlsx'
df = pd.read_excel(excel_url, sheet_name="Code", engine='openpyxl')

# ========== Helper Functions ==========

# Fetch itinerary details based on the travel code
def get_day_itinerary(code_input):
    match_row = df[df['Code'].str.lower() == code_input.lower()]
    if not match_row.empty:
        particulars = match_row.iloc[0]['Particulars']
        return particulars
    return None

# Generate the travel route based on entered codes
def generate_route(total_days):
    route_parts = []
    for day in range(1, total_days + 1):
        code_input = st.session_state.get(f"code_day{day}", "")
        if code_input:
            match_row = df[df['Code'].str.lower() == code_input.lower()]
            if not match_row.empty:
                route = match_row.iloc[0]['Route']
                route_parts.append(route)
    raw_route = '-'.join(route_parts).replace(' -', '-').replace('- ', '-')
    route_list = raw_route.split('-')
    cleaned_route = [route_list[i] for i in range(len(route_list)) if i == 0 or route_list[i] != route_list[i - 1]]
    return '-'.join(cleaned_route)

# ========== Streamlit UI ==========
st.title("🧳 Travel Package Builder")

st.header("1. Client & Package Details")

# Inputs
Client_Name = st.text_input("Client Name", "Test Client")

car_options = ["AC Sedan car", "AC Ertiga Car", "AC Innova Crysta", "AC Tempo Travel"]
hotel_options = [
    "Non AC Hotel room", "Standard AC Hotel room", "3star AC Hotel room",
    "3star AC Hotel room with Breakfast", "4star AC Hotel room with Breakfast", "5star AC Hotel room with Breakfast"
]
bhasma_types = ["Ticket", "Pandit ji", "Nandi hall"]
city_options = ["Indore", "Ujjain", "Omkareshwar", "Bhopal"]

car_type = st.selectbox("Car Type", car_options)
hotel_type = st.selectbox("Hotel Type", hotel_options)
room_type = st.text_input("Room Type", "Double occupancy 1 room")
bhasmarathi_required = st.selectbox("Bhasmarathi Required", ["Yes", "No"])
bhasmarathi_type = st.selectbox("Bhasmarathi Type", bhasma_types)

arrival_date = st.date_input("Arrival Date", datetime.today())
arrival_time = st.time_input("Arrival Time", datetime.now().time())
departure_time = st.time_input("Departure Time", datetime.now().time())

total_days = st.number_input("Total Days of Travel", min_value=1, max_value=10, step=1)
total_nights = total_days - 1
total_pax = st.number_input("Total Pax", min_value=1, step=1)

arrival_city = st.selectbox("Arrival City", city_options)
departure_city = st.selectbox("Departure City", city_options)

package_car_cost = st.number_input("Package Car Cost", min_value=0)
actual_car_cost = st.number_input("Actual Car Cost", min_value=0)
package_hotel_cost = st.number_input("Package Hotel Cost", min_value=0)
actual_hotel_cost = st.number_input("Actual Hotel Cost", min_value=0)
package_bhasmarathi_cost = st.number_input("Package Bhasmarathi Cost", min_value=0)
actual_bhasmarathi_cost = st.number_input("Actual Bhasmarathi Cost", min_value=0)

# Final package cost rounded down to nearest 1000
Package_Cost = int(((package_car_cost + package_hotel_cost + package_bhasmarathi_cost) / 1000) * 1000 - 1)

departure_date = arrival_date + timedelta(days=total_days)

# ========== Travel Code Entry ==========
st.header("2. Enter Travel Codes per Day")

daily_particulars = {}
grouped_itinerary = {}
itinerary_message = ""

for day in range(1, total_days + 1):
    travel_date = (arrival_date + timedelta(days=day - 1)).strftime('%d-%b-%Y')
    code_input = st.text_input(f"Travel Code for Day {day}", key=f"code_day{day}")

    if code_input:
        itinerary = get_day_itinerary(code_input)
        if itinerary:
            # Store itinerary
            daily_particulars[f"Day-{day} ({travel_date})"] = itinerary
            itinerary_message += f"*Day-{day} ({travel_date}):*\n{itinerary}\n\n"
        else:
            itinerary_message += f"*Day-{day} ({travel_date}):*\nCode not found in database.\n\n"

# ========== Route Generation ==========
st.header("3. Final Route")
final_route = generate_route(total_days)
st.markdown(f"**Route:** {final_route}")

# ========== Inclusions ==========
st.header("4. Inclusions")
inclusions = []

# Car
if car_type:
    inclusions.append(f"Entire travel as per itinerary by {car_type}.")
    inclusions.append("Toll, parking, and driver bata are included.")
    inclusions.append("Airport/ Railway station pickup and drop.")

# Bhasmarathi
if bhasmarathi_required == "Yes":
    inclusions.append(f"{bhasmarathi_type} for {total_pax} {'person' if total_pax == 1 else 'persons'}.")
    inclusions.append("Bhasm-Aarti pickup and drop.")

# Hotel
if hotel_type:
    inclusions.append("Standard check-in at 12:00 PM and check-out at 09:00 AM.")
    inclusions.append("Early check-in and late check-out are subject to room availability.")
    if "with Breakfast" in hotel_type:
        inclusions.append("Breakfast included.")

# Room
if room_type:
    inclusions.append(f"Hotel stay with {room_type} in {hotel_type}.")

# ========== Display All Summary ==========
st.header("5. Final Package Summary")

st.subheader("Client Summary")
st.markdown(f"""
- **Client Name:** {Client_Name}  
- **Travel Duration:** {total_days} day(s) / {total_nights} night(s)  
- **Total Pax:** {total_pax}  
- **Arrival:** {arrival_city} on {arrival_date.strftime('%d-%b-%Y')} at {arrival_time.strftime('%H:%M')}  
- **Departure:** {departure_city} on {departure_date.strftime('%d-%b-%Y')} at {departure_time.strftime('%H:%M')}  
- **Total Package Cost:** ₹{Package_Cost}
""")

st.subheader("Itinerary Details")
st.markdown(itinerary_message)

st.subheader("Inclusions")
st.markdown("*Inclusions:-*\n" + "\n".join([f"{i + 1}. {line}" for i, line in enumerate(inclusions)]))

st.subheader("Payment Terms")
st.markdown("""*Payment Terms:-*
1. 50% advance and remaining 50% after arrival at Ujjain.
2. For booking confirmation, please make the advance payment to the company's current account provided below.

*Company Account details:-*  
- Account Name: **ACHALA HOLIDAYS PVT LTD**  
- Bank: **Axis Bank**  
- Account No: **923020071937652**  
- IFSC Code: **UTIB0000329**
""")
