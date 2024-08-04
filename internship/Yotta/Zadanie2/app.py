import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
import streamlit as st
from streamlit_folium import st_folium
import folium

def get_weather_data(location, start_date, end_date):
    data = Daily(location, start_date, end_date)
    data = data.fetch()
    return data

def aggregate_weekly(data):
    data['week'] = data.index.to_period('W').start_time
    weekly_data = data.groupby('week').agg({
        'tavg': 'mean',
        'tmin': 'min',
        'tmax': 'max',
        'prcp': 'sum',
        'wdir': 'mean',
        'wspd': 'mean',
        'wpgt': 'max',
        'pres': 'mean',
    }).reset_index()
    
    weekly_data['week'] = weekly_data['week'].dt.strftime('%Y-%m-%d')
    
    weekly_data.rename(columns={
        'week': 'Week',
        'tavg': 'Average Temperature (°C)',
        'tmin': 'Minimum Temperature (°C)',
        'tmax': 'Maximum Temperature (°C)',
        'prcp': 'Total Precipitation (mm)',
        'wdir': 'Average Wind Direction (°)',
        'wspd': 'Average Wind Speed (km/h)',
        'wpgt': 'Maximum Wind Gust (km/h)',
        'pres': 'Average Pressure (hPa)',
    }, inplace=True)
    
    return weekly_data

def main():
    st.title("Analiza Danych Pogodowych")
    st.write("Wybierz miasto i okres czasu, aby pobrać dane pogodowe.")

    cities = ["Warszawa", "Katowice", "Kraków", "Gdańsk", "Wrocław", "Inne"]

    city = st.selectbox("Wybierz miasto", cities)

    if city == "Inne":
        st.write("Wybierz lokalizację na mapie")
        if 'selected_location' not in st.session_state:
            st.session_state.selected_location = None

        m = folium.Map(location=[52.2297, 21.0122], zoom_start=6)

        if st.session_state.selected_location:
            folium.Marker(
                location=[st.session_state.selected_location[0], st.session_state.selected_location[1]], 
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        map_data = st_folium(m, width=700, height=500)

        if map_data and 'last_clicked' in map_data and map_data['last_clicked']:
            st.session_state.selected_location = (
                map_data['last_clicked']['lat'], 
                map_data['last_clicked']['lng']
            )
            m = folium.Map(location=[st.session_state.selected_location[0], st.session_state.selected_location[1]], zoom_start=10)
            folium.Marker(
                location=[st.session_state.selected_location[0], st.session_state.selected_location[1]], 
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            st_folium(m, width=700, height=500)
            st.write(f'Wybrana lokalizacja: Szerokość geograficzna {st.session_state.selected_location[0]}, Długość geograficzna {st.session_state.selected_location[1]}')
    else:
        locations = {
            "Warszawa": Point(52.2297, 21.0122),
            "Katowice": Point(50.2649, 19.0238),
            "Kraków": Point(50.0647, 19.9450),
            "Gdańsk": Point(54.3520, 18.6466),
            "Wrocław": Point(51.1079, 17.0385)
        }
        location = locations[city]

    start_date = st.date_input("Data początkowa", datetime(2022, 1, 1).date())
    end_date = st.date_input("Data końcowa", datetime(2024, 1, 31).date())

    if city == "Inne" and st.session_state.selected_location:
        location = Point(st.session_state.selected_location[0], st.session_state.selected_location[1])

    if st.button("Pobierz dane"):
        if start_date < end_date:
            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.min.time())

            data = get_weather_data(location, start_datetime, end_datetime)
            if not data.empty:
                weekly_data = aggregate_weekly(data)

                st.write(f"Dane pogodowe dla {city} od {start_date} do {end_date}")
                st.dataframe(weekly_data)

                st.write("Podsumowanie statystyk")
                st.write(weekly_data.describe())
            else:
                st.error("Nie można pobrać danych dla wybranego miasta.")
        else:
            st.error("Data początkowa musi być wcześniejsza niż data końcowa.")

if __name__ == "__main__":
    main()