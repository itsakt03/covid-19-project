import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
from matplotlib import pyplot
import datetime
import plotly.graph_objects as go

@st.cache
def get_data():
    DATA_URL = ("https://api.covid19india.org/csv/latest/case_time_series.csv")
    DATA_URL_statewise_timeseries = ("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    DATA_URL_statewise = ("https://api.covid19india.org/csv/latest/state_wise.csv")
    return DATA_URL,DATA_URL_statewise,DATA_URL_statewise_timeseries
DATA_URL,DATA_URL_statewise,DATA_URL_statewise_timeseries=get_data()
st.title("Covid-19 in India")
options=["National Data","Statewise Data"]
optionSelected=st.sidebar.radio("",options)

if optionSelected=="Statewise Data":
    st.markdown("Statewise Covid-19 cases in India ")
    series1=pd.read_csv(DATA_URL_statewise, header=0, index_col=0, parse_dates=True, squeeze=True)
    series1=series1[["Confirmed","Recovered","Deaths","Active"]]
    st.subheader("Statewise Data")
    stateDict={"Andhra Pradesh":"AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chhattisgarh":"CG",
                "Goa":"GA","Gujarat":"GJ","Haryana":"HR","Himachal Pradesh":"HP","Jammu and Kashmir":"JK","Jharkhand":"JH","Karnataka":"KA",
                "Kerala":"KL","Madhya Pradesh":"MP","Maharashtra":"MH","Manipur":"MN","Meghalaya":"ML","Mizoram":"MZ",
                "Nagaland":"NL","Orissa":"OR","Punjab":"PB","Rajasthan":"RJ","Sikkim":"SK","Tamil Nadu":"TN","Tripura":"TR",
                "Uttarakhand":"UK","Uttar Pradesh":"UP","West Bengal":"WB","Tamil Nadu":"TN","Tripura":"TR","Andaman and Nicobar Islands":"AN",
                "Chandigarh":"CH","Delhi":"DL","Lakshadweep":"LD","Pondicherry":"PY"}

    selectedState = st.selectbox(
    "Select a state :",
        sorted(stateDict.keys()))
    series2=series1.loc[[selectedState]]
    st.info("Total Confirmed Cases : {s}".format(s=int(series2["Confirmed"])))
    st.success("Recovered Cases : {s}".format(s=int(series2["Recovered"])))
    st.warning("Active Cases : {s}".format(s=int(series2["Active"])))
    st.error("Deaths : {s}".format(s=int(series2["Deaths"])))

    stateDict={"Andhra Pradesh":"AP","Arunachal Pradesh":"AR","Assam":"AS","Bihar":"BR","Chhattisgarh":"CG",
                "Goa":"GA","Gujarat":"GJ","Haryana":"HR","Himachal Pradesh":"HP","Jammu and Kashmir":"JK","Jharkhand":"JH","Karnataka":"KA",
                "Kerala":"KL","Madhya Pradesh":"MP","Maharashtra":"MH","Manipur":"MN","Meghalaya":"ML","Mizoram":"MZ",
                "Nagaland":"NL","Orissa":"OR","Punjab":"PB","Rajasthan":"RJ","Sikkim":"SK","Tamil Nadu":"TN","Tripura":"TR",
                "Uttarakhand":"UK","Uttar Pradesh":"UP","West Bengal":"WB","Tamil Nadu":"TN","Tripura":"TR","Andaman and Nicobar Islands":"AN",
                "Chandigarh":"CH","Delhi":"DL","Lakshadweep":"LD","Pondicherry":"PY"}
    series_statewise_daily = pd.read_csv(DATA_URL_statewise_timeseries, header=0, index_col=0)
    stateForTimeSeries=stateDict[selectedState]
    timeSeriesDataforLast30DaysConfirmed = series_statewise_daily[stateForTimeSeries][-90::3]
    timeSeriesDataforLast30DaysRecovered = series_statewise_daily[stateForTimeSeries][-89::3]
    timeSeriesDataforLast30DaysDeceased = series_statewise_daily[stateForTimeSeries][-88::3]
    listOfVariables=["Daily Confirmed","Daily Recovered","Daily Deceased"]
    option = st.radio(
        'Select a category:',
        listOfVariables)
    if option=="Daily Confirmed":
        figD=px.line(timeSeriesDataforLast30DaysConfirmed,title="Daily confirmed cases in {s}".format(s=selectedState),labels={stateForTimeSeries:selectedState})
    elif option=="Daily Recovered":
        figD=px.line(timeSeriesDataforLast30DaysRecovered,title="Daily recovered cases in {s}".format(s=selectedState))
    elif option=="Daily Deceased":
        figD=px.line(timeSeriesDataforLast30DaysDeceased,title="Daily deceased cases in {s}".format(s=selectedState))
    figD.update_yaxes(title_text='No. of Cases')
    figD.update_layout(legend_title_text = "State")
    figD.update_layout(paper_bgcolor="white",plot_bgcolor="black",xaxis={"showgrid" : False,"showticklabels": True})
    figD.update_layout(yaxis={"showgrid" : False,"showticklabels": True})
    st.write(figD)

    total_active_today = series2["Confirmed"] - series2["Recovered"] - series2["Deaths"]
    pie1 = [total_active_today,series2["Recovered"],series2["Deaths"]]
    name1=["Total Active Cases","Total Recovered Cases","Total Deaths"]
    colors1=["#f54242","#5df542","#4278f5"]
    fig2 = px.pie(pie1, values=pie1,names=name1,
                title='Distribution of total cases in {s}'.format(s = selectedState),
                color = name1,
                color_discrete_map={'Total Active Cases':"#f54242",
                                 "Total Recovered Cases": "#4278f5",
                                 "Total Deaths" : "#5df542"})
    st.write(fig2)
    st.subheader("Data for all States and Union Territories")
    fullData=st.checkbox("Show Data ")
    if fullData:
        fig = go.Figure(data=[go.Table(header=dict(values=["States","Confirmed","Recovered","Deaths","Active"]),
                    cells=dict(values=[series1.index,series1.Confirmed,series1.Recovered,series1.Deaths,series1.Active]))])
        fig.update_layout(width=800, height=1089)
        st.write(fig)
elif optionSelected=="National Data":

    series = pd.read_csv(DATA_URL, header=0, index_col=0, parse_dates=True, squeeze=True)
    st.info("Total Cases : "  + str(series["Total Confirmed"][-1]))
    st.success("Recovered Cases : " + str(series["Total Recovered"][-1]))
    st.error("Total Deaths : " + str(series["Total Deceased"][-1]))


    daily_confirmed = series["Daily Confirmed"]
    daily_recovered = series["Daily Recovered"]
    total_confirmed = series["Total Confirmed"]
    total_recovered = series["Total Recovered"]
    daily_deceased = series["Daily Deceased"]
    total_deceased = series["Total Deceased"]
    listOfVariables=["Daily Confirmed","Daily Recovered","Daily Deceased","Total Confirmed","Total Recovered","Total Deceased"]
    option = st.selectbox(
        'Select a category:',
        listOfVariables)
    option1=st.checkbox(
        "Select starting date")

    if option1==True:
        dateStart = st.date_input('start date', datetime.date(2020,5,30))
    else:
        dateStart= datetime.date(2020,5,30)
    startDate1=datetime.date(2020,1,30)
    delta = dateStart-startDate1
    linedata =series[option][delta.days:]
    fig = px.line(linedata)
    fig.update_xaxes(title_text='Date')
    fig.update_layout(hovermode="x")
    fig.update_layout(legend_title_text = "Parameter")
    fig.update_yaxes(title_text='No. of Cases')


    st.write(fig)

    total_active_today = series["Total Confirmed"][-1] - series["Total Recovered"][-1] - series["Total Deceased"][-1]
    pie = [total_active_today,series["Total Recovered"][-1],series["Total Deceased"][-1]]
    name=["Total Active Cases","Total Recovered Cases","Total Deaths"]
    colors=["#f54242","#5df542","#4278f5"]
    fig1 = px.pie(pie, values=pie,names=name,
                title='Distribution of total cases in India',
                color = name,
                color_discrete_map={'Total Active Cases':"#f54242",
                                 "Total Recovered Cases": "#4278f5",
                                 "Total Deaths" : "#5df542"})

    st.write(fig1)
else:
    pass
for i in range(18):
    st.sidebar.markdown(" ")
st.sidebar.subheader("Aryan Kumar Thakur")