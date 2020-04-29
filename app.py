import streamlit as st
import pandas as pd
import numpy as np



st.title("Motor Vehicle Collisions in New York City")
st.markdown("A Streamlit dashboard that can be used to monitor and analyse motor vehicle collisions in NYC")

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv', nrows=nrows, parse_dates=[['CRASH DATE', 'CRASH TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash date_crash time':'date/time'}, inplace=True)
    data.rename(columns={'number of persons injured':'injured_persons'}, inplace=True)

    return data


data=load_data(100000)


st.header("Where are the most people injured in NYC")
injured_people=st.slider("Number of people injured in vehicle collisions", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[['latitude','longitude']].dropna(how='any'))

st.header("How many people got injured within a given time of date")
hour =st.selectbox("Hour", range(0,24),1)
data = data[data['date/time'].dt.hour == hour]

if(st.checkbox('Show data', False)):
    st.subheader('Raw Data')
    st.write(data)
