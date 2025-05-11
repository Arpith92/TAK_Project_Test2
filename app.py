import pandas as pd
import streamlit as st

st.title("Day-wise Travel Code Lookup")

# Read Excel from GitHub
excel_url = 'https://raw.githubusercontent.com/Arpith92/TAK_Project_Test2/main/Code.xlsx'
df = pd.read_excel(excel_url, sheet_name="Code", engine='openpyxl')

# Input: Total number of days
total_days = st.number_input("Enter total number of travel days:", min_value=1, max_value=30, step=1)

daily_particulars = {}

if total_days:
    for day in range(1, total_days + 1):
        code_input = st.text_input(f"Enter travel code for Day {day} (e.g., ip-id)", key=f"day{day}")
        
        if code_input:
            match_row = df[df['Code'].str.lower() == code_input.lower()]
            
            if not match_row.empty:
                particulars = match_row.iloc[0]['Particulars']
                daily_particulars[f'Day {day}'] = particulars
            else:
                daily_particulars[f'Day {day}'] = 'Code not found in database.'

# Display result
if daily_particulars:
    st.subheader("Day-wise Particulars")
    for day, detail in daily_particulars.items():
        st.write(f"**{day}**: {detail}")
