
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Research of Second-hand Car price in India from 1998 to 2019, By Lianxi Huang & Chenxi Shang')
df = pd.read_csv('train-data.csv')



st.subheader('Part I: Year -- average price & VOL, respective changes')
year_choose = st.text_input('Choose a year from 1999 to 2019 (Then press "enter")', 2019)
col1, col2 = st.columns(2)
if int(year_choose)>2019 or int(year_choose)<1999:
    st.write('Wrong enter! Out of range')
else:

    df_year_choose  = df[df.Year == int(year_choose)]
    df_year_past = df[df.Year == int(year_choose) -1 ]
    mean_now = df_year_choose['Price'].mean()
    mean_past = df_year_past['Price'].mean()

    current_year_vol = len(df_year_choose)
    past_year_vol = len(df_year_past)
    vol_difference = current_year_vol - past_year_vol

    col1.metric(label=(f"Price change in past year of {year_choose}"), value= mean_now, delta= mean_now - mean_past)
    col2.metric(label=(f"VOL change in past year of {year_choose}"), value= current_year_vol, delta= vol_difference)



st.subheader('Part II: Meaningful Charts')
fig, ax = plt.subplots(2,2,figsize=(15, 10))

df.Price.plot(ax=ax[0,0])
ax[0,0].set_title('price-plot of all data')

df_mean_price_year = df.groupby('Year')['Price'].mean()
df_mean_price_year.plot(ax=ax[0,1]).set_ylabel('Price')
ax[0,1].set_title('plot of year mean price')

df_vol_year = df.groupby('Year').size()
df_vol_year.plot(ax=ax[1,0])
ax[1,0].set_title('Vol changes by years')

df_mean_price_seats = df.groupby('Seats')['Price'].mean()
df_mean_price_seats.plot.bar(ax=ax[1,1]).set_ylabel('Price')
ax[1,1].set_title('plot of seats mean price')

st.pyplot(fig)


st.sidebar.subheader('Part III: Refine the information to obtain specific transaction data')
st.subheader('Part III: Specific transaction data')
st.write('Restricted condition')

#filter in Kilometers_Driven, location_type, Fuel_Type, (car_condition), Transmission
location_type_filter = st.sidebar.multiselect('Choose the city which is close to you', df.Location.unique(), df.Location.unique())
Fuel_Type_filter = st.sidebar.radio('Choose fuel type', ('CNG', 'Diesel', 'Petrol', 'LPG', 'Electric', 'All'))
car_condition_filter = st.sidebar.radio('Choose the car condition', ('New', 'Sub-new', 'Old', 'All'))
st.sidebar.write('new: Kilometers_Driven <= 60000; Sub-new: 60000 < Kilometers_Driven <120000; Old: Kilometers_Driven >= 120000')
Transmission_filter = st.sidebar.radio('Choose the car transmission', ('Manual','Automatic','All'))
Owner_Type_filter = st.sidebar.radio('Choose the owner type of the car', ('First','Second','Third','Fourth & Above','All'))


df = df[df.Location.isin(location_type_filter)]

if Fuel_Type_filter == 'All':
    pass
elif Fuel_Type_filter == 'CNG':
    df = df[df.Fuel_Type == 'CNG']
elif Fuel_Type_filter == 'Diesel':
    df = df[df.Fuel_Type == 'Diesel']
elif Fuel_Type_filter == 'Petrol':
    df = df[df.Fuel_Type == 'Petrol']
elif Fuel_Type_filter == 'LPG':
    df = df[df.Fuel_Type == 'LPG']
elif Fuel_Type_filter == 'Electric':
    df = df[df.Fuel_Type == 'Electric']

if car_condition_filter == 'All':
    pass
elif car_condition_filter == 'New':
    df = df[df.Kilometers_Driven <= 60000]
elif car_condition_filter == 'Sub-new':
    df = df[(df.Kilometers_Driven > 60000) & (df.Kilometers_Driven < 120000)]
else:
    df = df[df.Kilometers_Driven > 120000]

if Transmission_filter == 'All':
    pass
elif Transmission_filter == 'Automatic':
    df = df[df.Transmission == 'Automatic']
elif  Transmission_filter== 'Manual':
    df = df[df.Transmission == 'Manual']

if Owner_Type_filter == 'All':
    pass
elif Owner_Type_filter == 'First':
    df = df[df.Owner_Type == 'First']
elif Owner_Type_filter == 'Second':
    df = df[df.Owner_Type == 'Second']
elif Owner_Type_filter == 'Third':
    df = df[df.Owner_Type == 'Third']
elif Owner_Type_filter == 'Fourth & Above':
    df = df[df.Owner_Type == 'Fourth & Above']

col3, col4 = st.columns(2)
col3.write('Car-types that have been traded:')
col3.write(df.Name.unique())
col4.write('All data:')
col4.write(df)
