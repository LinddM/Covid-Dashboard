import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime
import time
import sqlalchemy as db

engine = db.create_engine("mysql+mysqldb://test:test123@db:3306/test")
engine.connect()

confirmed_melted = pd.read_sql_table("confirmed_melted", engine)
deaths_melted = pd.read_sql_table("deaths_melted", engine)
recovered_melted = pd.read_sql_table("recovered_melted", engine)

recoveredmelted2 = recovered_melted
confirmedmelted2 = confirmed_melted
deathsmelted2 = deaths_melted


del(recoveredmelted2['Province/State'])
del(confirmedmelted2['Province/State'])
del(deathsmelted2['Province/State'])


#del(recoveredmelted2['Country/Region'])
#del(recoveredmelted2['fecha'])


recoveredmelted2.notna()


#####----- STREAMLIT INFO -------- #####

st.beta_set_page_config(layout="wide")
st.title("This app shows COVID recovered, death and confirmed cases per country")


#SELECTBOX

metrics= ['confirmed' , 'deaths' , 'recovered']
cols = st.selectbox('Covid metric' , metrics)

if cols in metrics:
    metricstoshow = cols
    if metricstoshow == 'confirmed':
        st.title("Confirmed cases")
        #confirmed_cases = st.slider("Number of confirmed cases", 1 , int(confirmed_melted["confirmed"].max()))
        fecha = st.selectbox("Select date" , confirmed_melted['fecha'].unique())
        
        pais = st.selectbox("Select country to check data" , confirmed_melted['Country/Region'].unique())
        confirmado_hasta_la_fecha = confirmed_melted[confirmed_melted["Country/Region"] == pais][confirmed_melted["fecha"] == fecha]
        st.text("Casos confirmados a la fecha  : " + fecha)
        st.write(confirmado_hasta_la_fecha)
        confirmado_por_pais = confirmed_melted[confirmed_melted["Country/Region"] == pais]#[confirmed_melted["fecha"] == fecha]
        st.header("Casos de Covid en " + pais)
        st.bar_chart(confirmado_por_pais['confirmed'])
        st.text("Total de casos en todas las fechas del pais: " + pais)
        st.write(confirmado_por_pais)
        total1 = confirmed_melted.loc[confirmed_melted['Country/Region'] == pais][confirmed_melted["fecha"] == fecha]['confirmed'].sum()
        st.text( "Casos totales en " + pais + " a la fecha : " + fecha)
        st.text(total1)
        confirmed_melted['fecha'] = pd.to_datetime(confirmed_melted['fecha'],format= '%m/%d/%y', errors="ignore")
        # fecha1 = datetime.date(20,1,22)
        view = pdk.ViewState(latitude=0,longitude=0,zoom=0.2,)

        covidLayer1 = pdk.Layer(
             "ScatterplotLayer",
             data=confirmed_melted,
             pickable= True,
             opacity=0.3,
             stroked=True,
             filled=True,
             radius_scale=10,
             radius_min_pixels=5,
             radius_max_pixels=60,
             line_width_min_pixels=1,
             get_position=["lon", "lat"],
             get_radius = metricstoshow,
             auto_highlight=True,
             get_fill_color=[252, 136, 3],
             get_line_color=[255,0,0],
             tooltip="test test",

         )
        r = pdk.Deck(
         layers=[covidLayer1],
         initial_view_state=view,
         map_style="mapbox://styles/mapbox/light-v10",
         )
        map = st.pydeck_chart(r)
        

    elif metricstoshow == 'deaths':
         fecha = st.selectbox("Select date" , deaths_melted['fecha'].unique())
        
         pais = st.selectbox("Select country to check data" , deaths_melted['Country/Region'].unique())
         deaths_hasta_la_fecha = deaths_melted[deaths_melted["Country/Region"] == pais][deaths_melted["fecha"] == fecha]
         st.text("Muertos confirmados a la fecha de  : " + fecha)
         st.write(deaths_hasta_la_fecha)
         deaths_por_pais = deaths_melted[deaths_melted["Country/Region"] == pais]#[deaths_melted["fecha"] == fecha]
         st.header("Casos de muertes de Covid en " + pais)

         st.bar_chart(deaths_por_pais['deaths'])
         st.text("Total de muertes en el pais : " + pais )
         st.write(deaths_por_pais)
         total2 = deaths_melted.loc[deaths_melted['Country/Region'] == pais][deaths_melted["fecha"] == fecha]['deaths'].sum()
         st.text( "Muertes totales en " + pais + "a la fecha : " + fecha)
         st.text(total2)
         deaths_melted['fecha'] = pd.to_datetime(deaths_melted['fecha'],format= '%m/%d/%y', errors="ignore")
         # fecha1 = datetime.date(20,1,22)
         view = pdk.ViewState(latitude=0,longitude=0,zoom=0.2,)

         covidLayer2 = pdk.Layer(
             "ScatterplotLayer",
             data=deaths_melted,
             pickable= True,
             opacity=0.3,
             stroked=True,
             filled=True,
             radius_scale=10,
             radius_min_pixels=5,
             radius_max_pixels=60,
             line_width_min_pixels=1,
             get_position=["lon", "lat"],
             get_radius = metricstoshow,
             auto_highlight=True,
             get_fill_color=[252, 136, 3],
             get_line_color=[255,0,0],
             tooltip="test test",

         )
         r = pdk.Deck(
         layers=[covidLayer2],
         initial_view_state=view,
         map_style="mapbox://styles/mapbox/light-v10",
         )
         map = st.pydeck_chart(r)
         x = deaths_melted['fecha'].__len__
         

         
         
        
    else:

         st.title("Recovered cases")
         fecha = st.selectbox("Select date" , recovered_melted['fecha'].unique())
         #recovered_cases = st.slider("Number of recovered cases", 1 , int(recovered_melted["recovered"].max()))
         pais = st.selectbox("Select country to check data" , recovered_melted['Country/Region'].unique())
         recovered_hasta_la_fecha = recovered_melted[recovered_melted["Country/Region"] == pais][recovered_melted["fecha"] == fecha]
         st.text("Casos recuperados a la fecha : " + fecha)
         st.write(recovered_hasta_la_fecha)
         recovered_por_pais = recovered_melted[recovered_melted["Country/Region"] == pais]#[recovered_melted["fecha"] == fecha]
         st.header("Casos de Covid recuperados en " + pais)

         st.bar_chart(recovered_por_pais['recovered'])
         st.text("total por fecha")
         st.write(recovered_por_pais)

         total = recovered_melted.loc[recovered_melted['Country/Region'] == pais][recovered_melted["fecha"] == fecha]['recovered'].sum()
         st.text( "Casos totales en " + pais + " a la fecha : " + fecha + ":")
         st.text(total)
         #recovered_cases2 = st.slider("Number of recovered cases", -1 , int(total.max()))

         recovered_melted['fecha'] = pd.to_datetime(recovered_melted['fecha'],format= '%m/%d/%y', errors="ignore")
         # fecha2 = datetime.date(20,1,22)


         #st.map(recovered_melted)


         view = pdk.ViewState(latitude=0,longitude=0,zoom=0.2,)

         covidLayer = pdk.Layer(
             "ScatterplotLayer",
             data=recovered_melted,
             pickable= True,
             opacity=0.3,
             stroked=True,
             filled=True,
             radius_scale=10,
             radius_min_pixels=5,
             radius_max_pixels=60,
             line_width_min_pixels=1,
             get_position=["lon", "lat"],
             get_radius = metricstoshow,
             auto_highlight=True,
             get_fill_color=[252, 136, 3],
             get_line_color=[255,0,0],
             extruded= True,
             tooltip="test test",

         )
         r = pdk.Deck(
         layers=[covidLayer],
         initial_view_state=view,
         map_style="mapbox://styles/mapbox/light-v10",
         )
         map = st.pydeck_chart(r)