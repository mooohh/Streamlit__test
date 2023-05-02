import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import folium 
import pickle
from streamlit_folium import st_folium
from PIL import Image
from functions import predict_status, download_models, user_inputs, inverse_coordinate

# Render the image with a link

link_url = "https://www.mis.u-picardie.fr/"

image_url = "https://home.mis.u-picardie.fr/~devismes/WWW/images/mis.png"

st.markdown(f'<a  href="{link_url}" target="_blank"><img  src="{image_url}" width="130"></a>', unsafe_allow_html=True)

st.write('''
         ## App For Predicting The Status Of The :red[Nantes] Streets. 
         ''')

st.sidebar.header('The Inputs' )

data = user_inputs()
st.write('The Parametres That You Already Choose')
st.write(data) 


c = folium.Map(location = [47.219251, -1.554291],)


final_result = download_models(data)

colors = final_result['couleur_tp']
coordinates = final_result['geo_shape']

color_dict = { 'Fluide    ' : 'green', 'Indéterminé      ' : 'blue', 'Dense      ': 'black', 'Saturé      ' : 'yellow', 'Bloqué      ' : 'red'}

text = ''
for name, color in color_dict.items():
    text += f'<div style="background-color: {color}; display: inline-block; width: 20px; height: 20px;"></div> {name}'
    
st.write(text, unsafe_allow_html=True)


c = folium.Map(location = [47.219251, -1.554291],)

for i, coordinate in enumerate(coordinates):
    # Dessiner une ligne rouge le long de la Rue de Strasbourg
    coordinate = coordinate['coordinates']
    color_number = colors[i] 
    if  color_number == 3:
        folium.PolyLine(coordinate, color="green").add_to(c)
    elif color_number == 2:
        folium.PolyLine(coordinate, color="blue").add_to(c)
    elif color_number == 4:
        folium.PolyLine(coordinate, color="black").add_to(c)
    elif color_number == 5:
        folium.PolyLine(coordinate, color="yellw").add_to(c)
    else:
        folium.PolyLine(coordinate, color="red").add_to(c)



# call to render Folium map in Streamlit
st_data = st_folium(c, width=725)
