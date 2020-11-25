import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pydeck as pdk
import datetime
import time

data_conf = ('confirmed.csv')
data_deaths= ('deaths.csv')
data_recovered = ('recovered.csv')



confirmed = pd.read_csv("confirmed.csv")
deaths = pd.read_csv("deaths.csv")
recovered = pd.read_csv("recovered.csv")

variables = [
    "Province/State",
    "Country/Region",
    "Lat",
    "Long"

]
confirmed_melted = pd.melt(frame=confirmed, id_vars= variables, var_name="fecha",value_name="confirmed")
confirmed_melted["confirmed"] = confirmed_melted["confirmed"].astype(int)
confirmed_melted=confirmed_melted.rename(columns={'Lat': 'lat' , 'Long': 'lon'})
#print(confirmed_melted.head(10))
#confirmed_melted.to_csv("confirmedMelted.csv")





deaths_melted = pd.melt(frame=deaths, id_vars= variables, var_name="fecha",value_name="deaths")
deaths_melted["deaths"] = deaths_melted["deaths"].astype(int)
deaths_melted=deaths_melted.rename(columns={'Lat': 'lat' , 'Long': 'lon'})

recovered_melted = pd.melt(frame=recovered, id_vars= variables, var_name="fecha",value_name="recovered")
recovered_melted["recovered"] = recovered_melted["recovered"].astype(int)
recovered_melted=recovered_melted.rename(columns={'Lat': 'lat' , 'Long': 'lon'})

recoveredmelted2 = recovered_melted



del(recoveredmelted2['Province/State'])
#del(recoveredmelted2['Country/Region'])
#del(recoveredmelted2['fecha'])


recoveredmelted2.notna()



#print(confirmed_melted.head(10))
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
        st.text("De casos confirmados hasta la fecha : " + fecha)
        st.write(confirmado_hasta_la_fecha)
        confirmado_por_pais = confirmed_melted[confirmed_melted["Country/Region"] == pais]#[confirmed_melted["fecha"] == fecha]
        st.bar_chart(confirmado_por_pais['confirmed'])
        st.text("total por fecha")
        st.write(confirmado_por_pais)
        

    elif metricstoshow == 'deaths':
         fecha = st.selectbox("Select date" , deaths_melted['fecha'].unique())
        
         pais = st.selectbox("Select country to check data" , deaths_melted['Country/Region'].unique())
         deaths_hasta_la_fecha = deaths_melted[deaths_melted["Country/Region"] == pais][deaths_melted["fecha"] == fecha]
         st.text("De casos deathss hasta la fecha : " + fecha)
         st.write(deaths_hasta_la_fecha)
         deaths_por_pais = deaths_melted[deaths_melted["Country/Region"] == pais]#[deaths_melted["fecha"] == fecha]
         st.bar_chart(deaths_por_pais['deaths'])
         st.text("total por fecha")
         st.write(deaths_por_pais)

         
         
        
    else:

         st.title("recovered cases")
         fecha = st.selectbox("Select date" , recovered_melted['fecha'].unique())
         #recovered_cases = st.slider("Number of recovered cases", 1 , int(recovered_melted["recovered"].max()))
         pais = st.selectbox("Select country to check data" , recovered_melted['Country/Region'].unique())
         recovered_hasta_la_fecha = recovered_melted[recovered_melted["Country/Region"] == pais][recovered_melted["fecha"] == fecha]
         st.text("Casos recuperados a la fecha :  : " + fecha)
         st.write(recovered_hasta_la_fecha)
         recovered_por_pais = recovered_melted[recovered_melted["Country/Region"] == pais]#[recovered_melted["fecha"] == fecha]
         st.bar_chart(recovered_por_pais['recovered'])
         st.text("total por fecha")
         st.write(recovered_por_pais)

         total = recovered_melted.loc[recovered_melted['Country/Region'] == pais][recovered_melted["fecha"] == fecha]['recovered'].sum()
         st.text( "Casos totales en " + pais + "a la fecha : " + fecha)
         st.text(total)
         #recovered_cases2 = st.slider("Number of recovered cases", -1 , int(total.max()))

         recovered_melted['fecha'] = pd.to_datetime(recovered_melted['fecha'],format= '%m/%d/%y')
         fecha2 = datetime.date(20,1,22)


         


         #st.map(recovered_melted)


         view = pdk.ViewState(latitude=0,longitude=0,zoom=0.2,)

         covidLayer = pdk.Layer(
             "ScatterplotLayer",
             data=recovered_melted,
             pickable= False,
             opacity=0.3,
             stroked=True,
             filled=True,
             radius_scale=10,
             radius_min_pixels=5,
             radius_max_pixels=60,
             line_width_min_pixels=1,
             get_position=["lon", "lat"],
             get_radius = metricstoshow,
             
             
             get_fill_color=[252, 136, 3],
             get_line_color=[255,0,0],
             tooltip="test test",

         )
         r = pdk.Deck(
         layers=[covidLayer],
         initial_view_state=view,
         map_style="mapbox://styles/mapbox/light-v10",
         )
         map = st.pydeck_chart(r)

         x = recovered_melted['fecha'].__len__
         for i in range(0,120,1):
             fecha2 += datetime.timedelta(days=1)
             covidLayer= recovered_melted[recovered_melted['fecha'] == fecha2.isoformat()]
             r.update()
             map.pydeck_chart(r)
             #st.write("text")

             
             time.sleep(0.05)

         

         

         
         

         

         






