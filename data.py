import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import sqlalchemy as db

engine = db.create_engine("mysql+mysqldb://test:test123@db:3306/test")
engine.connect()

confirmed_melted = pd.read_sql_table("confirmed_melted", engine)
deaths_melted = pd.read_sql_table("deaths_melted", engine)
recovered_melted = pd.read_sql_table("recovered_melted", engine)

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
        fecha = st.selectbox("Select date" , confirmed_melted['fecha'].unique())
        
        pais = st.selectbox("Select country to check data" , confirmed_melted['Country/Region'].unique())
        confirmado_hasta_la_fecha = confirmed_melted[confirmed_melted["Country/Region"] == pais][confirmed_melted["fecha"] == fecha]
        st.text("De casos confirmados hasta la fecha : " + fecha)
        st.write(confirmado_hasta_la_fecha)
        confirmado_por_pais = confirmed_melted[confirmed_melted["Country/Region"] == pais]
        st.bar_chart(confirmado_por_pais['confirmed'])
        st.text("total por fecha")
        st.write(confirmado_por_pais)
        

    elif metricstoshow == 'deaths':
         fecha = st.selectbox("Select date" , deaths_melted['fecha'].unique())
        
         pais = st.selectbox("Select country to check data" , deaths_melted['Country/Region'].unique())
         deaths_hasta_la_fecha = deaths_melted[deaths_melted["Country/Region"] == pais][deaths_melted["fecha"] == fecha]
         st.text("De casos deathss hasta la fecha : " + fecha)
         st.write(deaths_hasta_la_fecha)
         deaths_por_pais = deaths_melted[deaths_melted["Country/Region"] == pais]
         st.bar_chart(deaths_por_pais['deaths'])
         st.text("total por fecha")
         st.write(deaths_por_pais)
        
    else:

         st.title("recovered cases")
         fecha = st.selectbox("Select date" , recovered_melted['fecha'].unique())
        
         pais = st.selectbox("Select country to check data" , recovered_melted['Country/Region'].unique())
         recovered_hasta_la_fecha = recovered_melted[recovered_melted["Country/Region"] == pais][recovered_melted["fecha"] == fecha]
         st.text("Casos recuperados a la fecha :  : " + fecha)
         st.write(recovered_hasta_la_fecha)
         recovered_por_pais = recovered_melted[recovered_melted["Country/Region"] == pais]
         st.bar_chart(recovered_por_pais['recovered'])
         st.text("total por fecha")
         st.write(recovered_por_pais)


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
                    data=recovered_melted,
                    get_position= '[Long , Lat]',
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,

                ),
                pdk.Layer(
                    'ScatterplotLayer',
                    data=recovered_melted,
                    get_position='[Long, Lat]',
                    get_color='[200, 30, 0, 160]',
                    get_radius=200,

                ),
            ],
        ))