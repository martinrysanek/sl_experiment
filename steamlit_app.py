﻿import streamlit as st
import requests
import pandas as pd

# Configure Streamlit page layout for a wide style
st.set_page_config(
    layout="wide",  # Set the layout to wide
    initial_sidebar_state="auto"  # Set the initial state of the sidebar
)

# Define the CSS style
css = """
{visibility: hidden;}
footer {visibility: hidden;}
body {overflow: hidden;}
data-testid="ScrollToBottomContainer"] {overflow: hidden;}
            # .sidebar .sidebar-content {{
            #     width: 375px;
            # }}
section[data-testid="stSidebar"] {
    width: 360px !important; # Set the width to your desired value
}
"""

# Display the dataframe with the custom CSS style
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

# URL of the raw Excel file in your GitHub repository
excel_file_url = 'https://raw.githubusercontent.com/martinrysanek/sl_experiment/main/slevy.xlsx'
# Send an HTTP GET request to the URL to download the file
response = requests.get(excel_file_url)

loading_text = st.text('Loading data...')
# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Create a Pandas DataFrame from the Excel file content
    data = pd.read_excel(response.content)
else:
    st.error(f"Failed to download file. Status code: {response.status_code}")
    exit(1)
loading_text.empty()

NADPISY = False
RADKY = True

# data.sort_values(by='Unit_num', ascending=True, inplace = True)

if NADPISY:
    st.sidebar.header('Hlavní kategorie zboží')

L1_selected = st.sidebar.selectbox('Vyber hlavní kategorii zboží', data['Kategorie'].unique())
if RADKY:
    st.sidebar.write("&nbsp;")
filtered_data = data[data['Kategorie'] == L1_selected].sort_values(by='Podkategorie', ascending=True)

if NADPISY:
    st.sidebar.header('Vedlejší kategorie zboží')
L2_selected = st.sidebar.selectbox('Vyber vedlejší kategorii zboží', filtered_data['Podkategorie'].unique(), index=0)
if RADKY:
    st.sidebar.write("&nbsp;")
# filtered_data = data[(data['Kategorie'] == L1_selected) & (data['Podkategorie'] == L2_selected)].sort_values(by='Druh', ascending=True)
filtered_data = filtered_data[filtered_data['Podkategorie'] == L2_selected].sort_values(by='Druh', ascending=True)

if NADPISY:
    st.sidebar.header('Druh zboží')
L3_selected = st.sidebar.multiselect('Vyber druh zboží', filtered_data['Druh'].unique(), default=filtered_data['Druh'].unique())

# st.title('Tabulka zboží')
st.write(f"**Hlavní kategorie**: *{L1_selected}* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + f"**Vedlejší kategorie**: *{L2_selected}* &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" + f"**Druh**: *{', '.join(L3_selected)}*")

# Filter the data 
filtered_data = filtered_data[filtered_data['Druh'].isin(L3_selected)].sort_values(by='Unit_num', ascending=True)
# selected_columns = ['Kategorie', 'Podkategorie', 'Druh', 'Název', 'Obchod', 'Cena', 'Cena za', 'Jednotková cena', 'Platnost']
selected_columns = ['Druh', 'Název', 'Obchod', 'Cena', 'Cena za', 'Jednotková cena', 'Platnost']
st.dataframe(filtered_data[selected_columns], hide_index=True, use_container_width=True, height=770)



