import streamlit as st
import pandas as pd
import numpy as np
import datetime
import json
import folium 
import pickle

def user_inputs():
    date = st.sidebar.date_input(
        "Select Date",
        datetime.date(2023, 4, 29))

    time = st.sidebar.time_input('Select time', value=datetime.time(0, 0), step=datetime.timedelta(minutes=1))

    speed = st.sidebar.slider('Select Speed', 0, 200, 60)

    option = st.sidebar.selectbox(
    'How would you like to predeict your results?',
    ('SVM', 'k_neighbors_classifier', 'Clustering', 'Random Forest'))

    data = pd.DataFrame({'date': date, 'speed': speed, 'time': time, 'model': option}, index=[0])

    return data


def predict_status(model , month = 4, day =12, hour = 6, minute = 7, week = 3, num_day_in_week = 6):
    
    with open('data_information', 'rb') as f:
        (stable_data, unstable_data) = pickle.load(f)

    x = np.array([month, day, hour, minute, week, num_day_in_week]).reshape(1, 6)           
    predictions = {}
    for id_, stb_data in stable_data.items():
        predictions[id_] = stb_data
    for id_ in unstable_data:
        try:
            predictions[id_] = model[id_].predict(x)[0]
        except UserWarning:
            continue
    return predictions

def download_models(data):
    # Download data and predict the result 
    
    #date
    date = data['date'][0]
    date = pd.to_datetime(date)

    time = data['time'][0]

    minute = time.minute
    hour = time.hour
    month = int(date.month)
    day = int(date.day)
    speed = data['speed'][0]

    selected_models = data['model'][0]

    # For The Week 
    week = int((day-1)/7 + 1) 

    #For The Day In The Week 
    num_day_in_week = day%7 + 1

    if selected_models == 'SVM':
        with open('save_models', 'rb') as f:
            models = pickle.load(f)

    elif selected_models == 'k_neighbors_classifier':
         with open('save_modelsKNeighborsClassifier', 'rb') as f:
            models = pickle.load(f)

    with open('coordinates', 'rb') as f:
        geo_points = pickle.load(f)
    


    predictions = predict_status(models, month, day, hour, minute, week, num_day_in_week)
    predictions = pd.DataFrame({ 'cha_id' : list(map(int, predictions.keys())), 'couleur_tp' : list(predictions.values())})
    geo_points['cha_id'] = geo_points['cha_id'].apply(lambda x: int(x))
    final_result = pd.merge(predictions, geo_points, on= 'cha_id')

    return final_result
    
def inverse_coordinate(coordinates):
    coordinates_finale = []
    for coordinate in coordinates:
        temps = coordinate[0]
        coordinate[0] = coordinate[1]
        coordinate[1] = temps
        coordinates_finale.append(coordinate)
    
    return coordinates_finale
