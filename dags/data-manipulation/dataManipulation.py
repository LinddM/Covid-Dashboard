import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


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
        

        #confirmado_por_pais = confirmed_melted.Select(['Country/Region' , 'fecha'])['confirmed'].sum()
        confirmado_por_pais = confirmed_melted[confirmed_melted["Country/Region"] == pais]#[confirmed_melted["fecha"] == fecha]

        
        #st.map(confirmado_por_pais)

        st.bar_chart(confirmado_por_pais['confirmed'])
        #

        
        #


        st.text("total por fecha")
        st.write(confirmado_por_pais)
        

    elif metricstoshow == 'deaths':
        st.title("deaths cases")
        deaths_cases = st.slider("Number of deaths cases", 1 , int(deaths_melted["deaths"].max()))
        #fecha = st.selectbox("Select date" , deaths_melted['fecha'].unique())
        pais = st.selectbox("Select country to check data" , deaths_melted['Country/Region'].unique())

        #confirmado_por_pais = deaths_melted.Select(['Country/Region' , 'fecha'])['deaths'].sum()
        deahts_por_pais = deaths_melted[deaths_melted["Country/Region"] == pais]#[deaths_melted["fecha"] == fecha]
        #st.map(deahts_por_pais)

        st.bar_chart(deahts_por_pais['deaths'])
        #

        
        #



        st.write(deahts_por_pais)
        st.map(deaths_melted)
       
    else:

        st.title("recovered cases")
        #recovered_cases = st.slider("Number of recovered cases", 1 , int(recovered_melted["recovered"].max()))
        #fecha = st.selectbox("Select date" , recovered_melted['fecha'].unique())
        pais = st.selectbox("Select country to check data" , recovered_melted['Country/Region'].unique())

        #confirmado_por_pais = recovered_melted.Select(['Country/Region' , 'fecha'])['recovered'].sum()
        recovered_por_pais = recovered_melted[recovered_melted["Country/Region"] == pais]#[recovered_melted["fecha"] == fecha]
        #st.map(recovered_por_pais)

        st.bar_chart(recovered_por_pais['recovered'])
        #

        
        #



        st.write(recovered_por_pais)









