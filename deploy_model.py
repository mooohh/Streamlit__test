import streamlit as st
import pandas as pd
import numpy as np
import datetime

def user_inputs():
    date = st.date_input(
        "Date Of The Predictions",
        datetime.date(2023, 4, 29))
    
    speed = st.sidebar.slider('The Speed', 0, 200, 60)

    data = pd.DataFrame({'date': date, 'speed': speed}, index=[0])


    return data


st.write('''
         # App Simple pour la prédiction des états des rue de la ville de nantes 
         
         ''')

st.sidebar.header('Les parametres d entrée' )

data = user_inputs()
st.subheader('We will predict the status of all the streets in nantes city')
st.write(data)


