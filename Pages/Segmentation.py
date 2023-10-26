import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from utils.load_data import *
from utils.plot import *
from plotly.subplots import make_subplots
import calendar
import pickle

import plotly.express as px
import plotly.graph_objects as go    
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, RobustScaler, StandardScaler



if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

st.set_page_config(page_title="Customer Segmentation",page_icon = "👥" ,layout="wide",initial_sidebar_state=st.session_state.sidebar_state)
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Segmentation with RFM</h1>", unsafe_allow_html=True)

st.warning("**What is RFM ?**", icon="📌")

st.warning("▪️    🗓️**R |** Recency  :  How recently a customer made a purchase.")
st.warning("▪️    📈**F |** Frequency  :  How often a customer makes purchases.")
st.warning("▪️    💰**M |** Monetary  :  How much money a customer spends.")


st.markdown("""
    <div class="title">
        <div class="line"></div>
        <h3>Live Segmentation</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)
min_date=pd.to_datetime("1/1/2010")
max_date=pd.to_datetime("31/12/2050")


with st.form("my_form"):
    df1=pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\MLOPS Project\Data\clean_data2.csv")
    id=df1["Customer ID"].max()
    st.write("Please Enter An ID High Than",id)
    col1,col2,col3,col4,col5,col6=st.columns(6)
    with col1:
        date_last_quarter=st.date_input("Last Date Of The Quarter",min_value=min_date,max_value=max_date)
    with col2:
        customer_id=st.number_input("Customer ID",min_value=0,step=1)
    with col3:
        customer_name=st.text_input("Customer Name")
    with col4:
        spent=st.number_input("Sales")
    with col5:
        nb_orders=st.number_input("Orders",min_value=0,step=1)
    with col6:
        sales_key=st.number_input("Sales Key",min_value=0,step=1)
   
    submitted = st.form_submit_button("Submit")
    if submitted:
        
        # Create a DataFrame
        df = pd.DataFrame({
            'Date Last Quarter': [date_last_quarter],
            'Customer ID': [customer_id],
            'Customer Name': [customer_name],
            'Spent': [spent],
            'Number of Orders': [nb_orders]
        })
        today = datetime.today().date()
        days_difference = (today - date_last_quarter).days
        frequency=nb_orders
        monetary=spent
        df["recency"]=days_difference
       
        kmeans = pickle.load(open(r"D:\Users\ameni\OneDrive\Bureau\MLOPS Project\notebooks\kmeans.pkl", "rb"))
        y=kmeans.predict(df[['recency', 'Spent', 'Number of Orders']])
        
        
        df["segment"]=y
        seg = {
            3: 'Potentiel',
            0: 'Zappeur',
            1: 'Habituel',
            2: 'Fidele'
        }

        df['segment_name'] = df['segment'].replace(seg, regex=True)
        
        
        selected_segment_name = df[df['Customer ID'] == customer_id ]['segment_name'].iloc[0]

        st.write("The Customer named",customer_name,"With ID",customer_id,"Is a" ,selected_segment_name,"Customer")




with st.form("my_form1"):
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        
        
        #data contain Last Date Of The Quarter | Customer ID | Customer Name | Sales | Orders | Sales Key
        today = datetime.today()
        # days_difference = (today - data[""]).days
        data["Date Last Quarter"]=pd.to_datetime(data["Date Last Quarter"],format="%d/%m/%Y")
        data["recency"]=(today - data["Date Last Quarter"]).dt.days
        data.dropna(inplace=True)
        kmeans = pickle.load(open(r"D:\Users\ameni\OneDrive\Bureau\MLOPS Project\notebooks\kmeans.pkl", "rb"))
        y=kmeans.predict(data[['recency', 'Spent', 'Number of Orders']])
        
        
        
        data["segment"]=y
        seg = {
            3: 'Potentiel',
            0: 'Zappeur',
            1: 'Habituel',
            2: 'Fidele'
        }

        data['segment_name'] = data['segment'].replace(seg, regex=True)
                        
    submitted1 = st.form_submit_button("Submit")
    if submitted1:
        col1,col2=st.columns(2)
        with col1:
            st.write(data[["Customer ID","Customer Name","Spent","Number of Orders","recency","segment_name"]])
        with col2:
            fig = px.histogram(data, x='segment_name', color=data['segment_name'])
            title_with_space = '\xa0\xa0\xa0\xa0' + "Distribution Of The Clusters" # Add four non-breaking spaces for example
            fig.update_layout(
            title_text=title_with_space,
            title_font=dict(size=22)
        )
            st.plotly_chart(fig,use_container_width=True)
        


st.markdown("""
    <div class="title">
        <div class="line"></div>
        <h3>Actual Segmentation</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

df=pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\MLOPS Project\dff.csv")

col1,col2=st.columns(2)
with col1:
    fig = px.histogram(df, x='segment_name', color=df['segment_name'])
    title_with_space = '\xa0\xa0\xa0\xa0' + "Distribution Of The Clusters" # Add four non-breaking spaces for example
    fig.update_layout(
    title_text=title_with_space,
    title_font=dict(size=22)
)
    st.plotly_chart(fig,use_container_width=True)
with col2:
    def three_d_scatter(data,x,y,z,title):
        fig = px.scatter_3d(data, x=x, y=y, z=z,
                    color='segment_name')
        title_with_space = '\xa0\xa0\xa0\xa0' + title # Add four non-breaking spaces for example
        fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)
        )
        st.plotly_chart(fig,use_container_width=True)
    three_d_scatter(df,"Number of Orders","Spent","recency","Segments par RFM")
    
    
    
    
fig = px.scatter(df, x='Spent', y='Number of Orders', color=df['segment_name'])
title_with_space = '\xa0\xa0\xa0\xa0' + "Cluster's Profile Based On Frequency And Monetary"# Add four non-breaking spaces for example
fig.update_layout(
title_text=title_with_space,
title_font=dict(size=22)
)
st.plotly_chart(fig,use_container_width=True)
