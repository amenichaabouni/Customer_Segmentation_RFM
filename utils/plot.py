import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import calendar
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st 



def bar_plot(data,x,y,title,label1,label2):
    data_sorted = data.sort_values(by=y, ascending=True)
    fig = px.bar(data_sorted, y=x, x=y, orientation='h',
                 labels={x: label1, y: label2})
    title_with_space = '\xa0\xa0\xa0\xa0' + title  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=24)  # Adjust the size as needed
    )
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
    
    
def bar_plot_v(data,x,y,title,label1,label2):
    data_sorted = data.sort_values(by=y, ascending=True)
    fig = px.bar(data_sorted, y=y, x=x, 
                 labels={x: label1, y: label2})
    title_with_space = '\xa0\xa0\xa0\xa0' + title  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=24)  # Adjust the size as needed
    )
    # Show the plot
    st.plotly_chart(fig, use_container_width=True)
    
    
def line_plot(data, x_column, y_column, title, x_label, y_label):
    fig = go.Figure(data=go.Scatter(x=data[x_column], y=data[y_column], mode='lines+markers'))
    fig.update_layout(xaxis_title=x_label, yaxis_title=y_label)
    title_with_space = '\xa0\xa0\xa0\xa0' + title  # Add four non-breaking spaces for example
    fig.update_layout(
        title_text=title_with_space,
        title_font=dict(size=24)  # Adjust the size as needed
         )
    st.plotly_chart(fig, use_container_width=True)
    