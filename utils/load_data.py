import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import calendar
import plotly.express as px
import plotly.graph_objects as go




data_train = pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\Dynamic Pricing\Data\train.csv",sep="|")
data_items = pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\Dynamic Pricing\Data\items.csv",sep="|")
data_new = pd.merge( data_train, data_items, how='left', on='pid' )

data_class = pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\Dynamic Pricing\Data\class.csv",sep="|")
data_class.set_index('lineID',inplace=True,drop=True)
data_realclass = pd.read_csv(r"D:\Users\ameni\OneDrive\Bureau\Dynamic Pricing\Data\realclass.csv",sep="|")
data_realclass.rename(columns={'revenue':'actual_revenue'},inplace=True)
data_realclass.set_index("lineID",inplace=True,drop=True)
test_data = data_class.join(data_realclass,on='lineID',how='inner')
test_data = pd.merge( test_data, data_items, how='left', on='pid' )



# Define the year and the starting date for that year
year = 2023  # Replace with the actual year
start_date = pd.to_datetime(f'{year}-01-01')

# Convert 'day' column to datetime
data_new['day'] = pd.to_datetime(data_new['day'], format='%j')
# Add the reference date to the 'day' column
data_new['date'] = start_date + pd.to_timedelta(data_new['day'].dt.dayofyear - 93, unit='D')