import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import folium 
from streamlit_folium import st_folium

def user_inputs():
    date = st.date_input(
        "Select Date",
        datetime.date(2023, 4, 29))
    
    speed = st.sidebar.slider('The Speed', 0, 200, 60)

    data = pd.DataFrame({'date': date, 'speed': speed}, index=[0])

    return data


st.write('''
         # App Simple pour la prédiction des états des rue de la ville de nantes 
         
         ''')

st.sidebar.header('The inputs' )

data = user_inputs()
st.subheader('We will predict the status of all the streets in nantes city')
st.write(data)



with open('coordinates.json', 'r') as f:
    coordinates = json.load(f)

c = folium.Map(location = [47.219251, -1.554291],)


i = 0
for coordinate in coordinates:
    # Dessiner une ligne rouge le long de la Rue de Strasbourg
    if i <= 600:
        folium.PolyLine(coordinate, color="green").add_to(c)
    elif i < 650:
        folium.PolyLine(coordinate, color="blue").add_to(c)
    elif i < 700:
        folium.PolyLine(coordinate, color="red").add_to(c)
    else:
        folium.PolyLine(coordinate, color="orange").add_to(c)
    i += 1 
        

# call to render Folium map in Streamlit
st_data = st_folium(c, width=725)


