import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import datetime
import plotly.graph_objects as go
@st.cache_data
def get_data():
    DATA_URL = "https://data.incovid19.org/csv/latest/case_time_series.csv"
    DATA_URL_statewise_timeseries = "https://data.incovid19.org/csv/latest/state_wise_daily.csv"
    DATA_URL_statewise = "https://data.incovid19.org/csv/latest/state_wise.csv"
    return DATA_URL, DATA_URL_statewise, DATA_URL_statewise_timeseries

DATA_URL, DATA_URL_statewise, DATA_URL_statewise_timeseries = get_data()

st.title("Covid-19 in India Tracker")
options = ["National Data", "Statewise Data"]
optionSelected = st.sidebar.radio("Navigation", options)

if optionSelected == "Statewise Data":
    st.markdown("### Statewise Covid-19 cases in India")
    series1 = pd.read_csv(DATA_URL_statewise, header=0, index_col=0, parse_dates=True).squeeze("columns")
    series1 = series1[["Confirmed", "Recovered", "Deaths", "Active"]]
    
    st.subheader("Statewise Data")
    stateDict = {
        "Andhra Pradesh":"AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chhattisgarh":"CG",
        "Goa":"GA","Gujarat":"GJ","Haryana":"HR","Himachal Pradesh":"HP","Jammu and Kashmir":"JK",
        "Jharkhand":"JH","Karnataka":"KA","Kerala":"KL","Madhya Pradesh":"MP","Maharashtra":"MH",
        "Manipur":"MN","Meghalaya":"ML","Mizoram":"MZ","Nagaland":"NL","Odisha":"OR","Punjab":"PB",
        "Rajasthan":"RJ","Sikkim":"SK","Tamil Nadu":"TN","Tripura":"TR","Uttarakhand":"UK",
        "Uttar Pradesh":"UP","West Bengal":"WB","Andaman and Nicobar Islands":"AN",
        "Chandigarh":"CH","Delhi":"DL","Lakshadweep":"LD","Puducherry":"PY"
    }

    selectedState = st.selectbox("Select a state :", sorted(stateDict.keys()))
    series2 = series1.loc[selectedState]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Confirmed", int(series2["Confirmed"]))
    col2.metric("Recovered", int(series2["Recovered"]))
    col3.metric("Active", int(series2["Active"]))
    col4.metric("Deaths", int(series2["Deaths"]))

    series_statewise_daily = pd.read_csv(DATA_URL_statewise_timeseries, header=0, index_col=0)
    stateForTimeSeries = stateDict[selectedState]
    
    timeSeriesDataforLast30DaysConfirmed = series_statewise_daily[stateForTimeSeries][-90::3]
    timeSeriesDataforLast30DaysRecovered = series_statewise_daily[stateForTimeSeries][-89::3]
    timeSeriesDataforLast30DaysDeceased = series_statewise_daily[stateForTimeSeries][-88::3]
    
    option = st.radio('Select a category:', ["Daily Confirmed", "Daily Recovered", "Daily Deceased"])
    
    if option == "Daily Confirmed":
        figD = px.line(timeSeriesDataforLast30DaysConfirmed, title=f"Daily confirmed in {selectedState}")
    elif option == "Daily Recovered":
        figD = px.line(timeSeriesDataforLast30DaysRecovered, title=f"Daily recovered in {selectedState}")
    else:
        figD = px.line(timeSeriesDataforLast30DaysDeceased, title=f"Daily deceased in {selectedState}")
    
    st.plotly_chart(figD, use_container_width=True)

elif optionSelected == "National Data":
    series = pd.read_csv(DATA_URL, header=0, index_col=0, parse_dates=True).squeeze("columns")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Cases", series["Total Confirmed"].iloc[-1])
    col2.metric("Recovered", series["Total Recovered"].iloc[-1])
    col3.metric("Deaths", series["Total Deceased"].iloc[-1])

    option = st.selectbox('Select a category:', ["Daily Confirmed", "Daily Recovered", "Daily Deceased", "Total Confirmed", "Total Recovered", "Total Deceased"])
    dateStart = st.date_input('Start date', datetime.date(2020, 5, 30))
    
    linedata = series[series.index >= pd.to_datetime(dateStart)][option]
    fig = px.line(linedata)
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.subheader("Aryan Kumar Thakur")


