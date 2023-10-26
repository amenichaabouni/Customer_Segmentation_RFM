import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from utils.load_data import *
from utils.plot import *
from plotly.subplots import make_subplots
import calendar
import plotly.express as px
import plotly.graph_objects as go    




if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'

st.set_page_config(page_title="Customer Segmentation",page_icon = "👥" ,layout="wide",initial_sidebar_state=st.session_state.sidebar_state)
with open('assets/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>Customer Segmentation with RFM</h1>", unsafe_allow_html=True)

data = pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\MLOPS Project\Data\clean_data.csv")
data1 = pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\MLOPS Project\Data\marketing_campaign.csv",sep="\t")

ed_inc=data.groupby("Education")["Income"].sum().reset_index()
ed_inc1=data.groupby("Education")["Spent"].sum().reset_index()
data1["ID"]="ID-"+(data1["ID"]).astype(str)
nbr_cust=data1["ID"].nunique()
nbr_deal_pur=data1["NumDealsPurchases"].sum()
nbr_web_pur=data1["NumWebPurchases"].sum()
nbr_catag_pur=data1["NumCatalogPurchases"].sum()
nbr_store_pur=data1["NumStorePurchases"].sum()
nbr_visits=data1["NumWebVisitsMonth"].sum()
Total_Revenu=data['Spent'].sum()



frame_style = "padding: 1px; border: 3px solid rgba(36, 18, 91, 0.1)  ; border-radius: 10px;"
st.write(f"<div style='{frame_style}'><h3 style='font-size:20px;text-align:center;color:#283747;'>Total Revenu</h3><p style='font-size:20px; text-align:center;font-weight:bold;'> {Total_Revenu} </p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1,col2,col3,col4,col5,col6=st.columns(6)
with col1:
    frame_style = "padding: 1px; border: 3px solid rgba(36, 18, 91, 0.1)  ; border-radius: 10px;"
    st.write(f"<div style='{frame_style}'><h3 style='font-size:15px;text-align:center;color:#283747;'>Customers</h3><p style='font-size:15px; text-align:center;font-weight:bold;'> {nbr_cust} </p></div>", unsafe_allow_html=True)
with col2:
    st.write(f"<div style='{frame_style}'><h3 style='font-size:15px;text-align:center;color:#283747;'> Web Visits</h3><p style='font-size:15px; text-align:center;font-weight:bold;'> {nbr_visits} </p></div>", unsafe_allow_html=True)
with col3:
    st.write(f"<div style='{frame_style}'><h3 style='font-size:15px;text-align:center;color:#283747;'>Web Purchases</h3><p style='font-size:15px; text-align:center;font-weight:bold;'> {nbr_web_pur} </p></div>", unsafe_allow_html=True)
with col4:
    st.write(f"<div style='{frame_style}'><h3 style='font-size:15px;text-align:center;color:#283747;'>Store Purchases</h3><p style='font-size:15px; text-align:center;font-weight:bold;'> {nbr_store_pur} </p></div>", unsafe_allow_html=True)
with col5:
    st.write(f"<div style='{frame_style}'><h3 style='font-size:15px;text-align:center;color:#283747;'>Catalogue Purchases</h3><p style='font-size:15px; text-align:center;font-weight:bold;'> {nbr_catag_pur} </p></div>", unsafe_allow_html=True)
with col6:
    st.write(f"<div style='{frame_style}'><h3 style='font-size:15px;text-align:center;color:#283747;'>Deals Purchases</h3><p style='font-size:15px; text-align:center;font-weight:bold;'> {nbr_deal_pur} </p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
    <div class="title">
        <div class="line"></div>
        <h3>📚 Education Level</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)


col1,col2,col3=st.columns(3)
with col1:
        # Count the occurrences of each education level
    education_counts = data['Education'].value_counts().reset_index()

    # Rename the columns for clarity
    education_counts.columns = ['Education', 'Count']

    # Create a bar plot
    fig = px.bar(education_counts, x='Education', y='Count')
    title_with_space = '\xa0\xa0\xa0\xa0' + 'Count of Education Levels'  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)
    )

    st.plotly_chart(fig,use_container_width=True)
with col2:
    # Assuming you have already calculated ed_inc
    fig = px.bar(ed_inc, x='Education', y='Income', labels={'Income':'Total Income'})
    title_with_space = '\xa0\xa0\xa0\xa0' + 'Total Income by Education Level'  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)
    )
    st.plotly_chart(fig,use_container_width=True)
with col3:
    # Assuming you have already calculated ed_inc
    fig = px.bar(ed_inc1, x='Education', y='Spent', labels={'Spent':'Spent'})
    title_with_space = '\xa0\xa0\xa0\xa0' + 'Spent by Education Level'  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)
    )
    st.plotly_chart(fig,use_container_width=True)
    


st.markdown("""
    <div class="title">
        <div class="line"></div>
        <h3>🔝 TOPs</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

data1["Spent"] = data1["MntWines"]+ data1["MntFruits"]+ data1["MntMeatProducts"]+ data1["MntFishProducts"]+ data1["MntSweetProducts"]+ data1["MntGoldProds"]

top_clients = (data1.groupby(['Education','ID'])['Spent']
            .sum().reset_index()
            .sort_values(by=['Education', 'Spent'], ascending=[True, False])
            .groupby('Education').head(5))

categories = list(data1['Education'].unique())
        
        
selected_category  = st.selectbox(
        'Education',
        categories)



filtered_clients = top_clients[top_clients['Education'] == selected_category]


fig = px.bar(filtered_clients, x='ID', y='Spent', labels={'Spent':'Spent'})

title_with_space = '\xa0\xa0\xa0\xa0' + 'TOP 5 Customers By Education Level'  # Add four non-breaking spaces for example
fig.update_layout(
    title_text=title_with_space,
    title_font=dict(size=22)
)
st.plotly_chart(fig,use_container_width=True)





st.markdown("""
    <div class="title">
        <div class="line"></div>
        <h3>💍 Marital Status</h3>
        <div class="line"></div>
    </div>
    """, unsafe_allow_html=True)

income_st=data1.groupby("Marital_Status")["Income"].sum().reset_index()
spent_st=data1.groupby("Marital_Status")["Spent"].sum().reset_index()

col1,col2,col3=st.columns(3)
with col1:
    fig = go.Figure()

    # Créer un graphique en secteurs
    fig.add_trace(go.Pie(labels=data1['Marital_Status'].value_counts().index, values=data1['Marital_Status'].value_counts(), textinfo='percent+value', name='Number of Each Marital Status'))
    title_with_space = '\xa0\xa0\xa0\xa0' + "Number of Each Marital Status"  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)  # Adjust the size as needed
    )
    fig.update_layout(
        showlegend=True,
        autosize=False
    )

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)
   
with col2:
    # Assuming you have already calculated ed_inc
    fig = px.bar(income_st, x='Marital_Status', y='Income', labels={'Income':'Total Income'})
    title_with_space = '\xa0\xa0\xa0\xa0' + 'Total Income by Marital Status'  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)
    )
    st.plotly_chart(fig,use_container_width=True)
with col3:
    # Assuming you have already calculated ed_inc
    fig = px.bar(spent_st, x='Marital_Status', y='Spent', labels={'Spent':'Spent'})
    title_with_space = '\xa0\xa0\xa0\xa0' + 'Spent by Marital Status'  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=22)
    )
    st.plotly_chart(fig,use_container_width=True)




html_string='''
<script>
// To break out of iframe and access the parent window
const streamlitDoc = window.parent.document;

// Make the replacement
document.addEventListener("DOMContentLoaded", function(event){
        streamlitDoc.getElementsByTagName("footer")[0].innerHTML = "Provided by <a href='https://www.linkedin.com/in/ameni-chaabouni-3488181b4/' target='_blank' class='css-z3au9t egzxvld2'>Ameni CHAABOUNI</a>";
    });
</script>
'''
components.html(html_string)