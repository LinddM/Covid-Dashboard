import streamlit as st
import numpy as np
import pandas as pd
from streamlit import cache
import pydeck as pdk

st.title("Uber Pickups")

DATE_COLUMN = 'Date/Time'
DATA_URL=('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@cache
def load_data(nrows):
    data=pd.read_csv(DATA_URL, parse_dates=[DATE_COLUMN], nrows=nrows).rename(columns={
        "Lat":"latitude",
        "Lon":"longitude"
    })
    return data

# create text element and let the reader know the data is loading
data_load_state = st.text("Loading data...")
data=load_data(10000)
data_load_state.text("Done!")

st.subheader("Raw data")
if st.checkbox("Show raw data"):
    st.write(data)

st.subheader("Number of pickups by hour")
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0, 24))[0]

st.bar_chart(hist_values)

st.subheader("Map of all pickups")
#st.map(data)

hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f"Map of all pickups at {hour_to_filter}:00")
st.map(filtered_data)

# extra plots *tarea*
st.title("Extra plots (tarea)")

st.subheader("Number of pickups by day")

date_to_filter_hist = st.slider('Select the day range',1, 8, (3, 5))
hist_vals_day = np.histogram(
    data[DATE_COLUMN].dt.day, range=date_to_filter_hist)[0]

st.line_chart(hist_vals_day)

st.subheader("Map of pickups per day")

date_to_filter_map = st.slider('Select the date',1, 8, 5)
filtered_day = data[data[DATE_COLUMN].dt.day == date_to_filter_map]
st.subheader(f"Map of all pickups at Sep {date_to_filter_map}, 2014")
#st.map(filtered_day)


st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=40.73,
         longitude=-74,
         zoom=11,
         pitch=50,
     ),
     layers=[
         pdk.Layer(
            'HexagonLayer',
            data=filtered_day,
            get_position='[longitude, latitude]',
            radius=200,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=filtered_day,
             get_position='[longitude, latitude]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
 ))

print(filtered_day.head(10))