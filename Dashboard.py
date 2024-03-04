import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read data
df = pd.read_csv('all_data.csv')  

# Title
st.title('Bike Sharing Data Analysis') 

# Sidebar 
st.sidebar.title('Navigation')
options = st.sidebar.radio('Choose', ['Data Information', 'Data Analysis', 'Answers & Conclusion'])

# Data Information
if options == 'Data Information':

  st.header('Data Information')
  st.write("""
  - Total rows: 731
  + Columns: 
    - instant (Sample index)
    - dteday (Date)
    + season (Season) :
        - 1: Spring 
        - 2: Summer 
        - 3: Fall 
        - 4: Winter
    + yr (Year) 
        - The value 0 is used to represent the year 2011
        - The value 1 is used to represent the year 2012
    - mnth (Month) = 1 to 12
    - holiday = Weather day is holiday or not (extracted from http://dchr.dc.gov/page/holiday-schedule)
    - weekday = Day of the week
    - workingday = If day is neither weekend nor holiday is 1, otherwise is 0.
    + weathersit  
        - 1: Clear, Few clouds, Partly cloudy, Partly cloudy 
        - 2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist 
        - 3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds 
    - temp = Normalized temperature in Celsius. The values are divided to 41 (max)
    - atemp = Normalized feeling temperature in Celsius. The values are divided to 50 (max)
    - hum = Normalized humidity. The values are divided to 100 (max)
    - windspeed = Normalized wind speed. The values are divided to 67 (max)
    - casual = Count of casual users
    - registered = Count of registered users
    - cnt = Count of total rental bikes including both casual and registered
  """)
  
  st.write("""
  \n**Questions:**
  1. When did the bike sharing rentals reach the highest number in a day?
  2. What is the bike sharing rental count for each month?
  3. How is the bike sharing rental distribution across different weather conditions?
  """)
  
# Data Analysis  
elif options == 'Data Analysis':
  
  st.header('Data Analysis')
  analysis_option = st.selectbox('Choose Analysis',
                      ['Bike Rental and Revenue per Month',
                       'Bike Rental Distribution Per Season',
                       'Bike Rental Distribution Per Weekday',
                       'Frequency, Recency, and Monetary Analysis'])
                       
  if analysis_option == 'Bike Rental and Revenue per Month':
    
    monthly_df = df.groupby('month')[['instant','cnt']].sum().reset_index()
    monthly_df['revenue'] = monthly_df['cnt'] * 3
    st.write(monthly_df)
    
  elif analysis_option == 'Bike Rental Distribution Per Season':
    
    season_map = {1:'Spring', 2:'Summer', 3:'Fall', 4:'Winter'}
    season_df = df.groupby('season')['instant'].count().reset_index()
    season_df['season'] = season_df['season'].map(season_map)
    st.bar_chart(season_df.set_index('season'))
    
  elif analysis_option == 'Bike Rental Distribution Per Weekday':
    
    weekday_map = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 
                   4:'Friday', 5:'Saturday', 6:'Sunday'}
    weekday_df = df.groupby('weekday')['cnt'].count().reset_index()
    weekday_df['weekday'] = weekday_df['weekday'].map(weekday_map)
    st.bar_chart(weekday_df.set_index('weekday'))
    
  elif analysis_option == 'Frequency, Recency, and Monetary Analysis':
    df['dteday'] = pd.to_datetime(df['dteday'])
    recency = (df['dteday'].max() - df['dteday']).dt.days
    frequency = df.groupby('dteday').size().mean()
    monetary = df.groupby('dteday')['cnt'].sum()

    st.write("RFM Analysis:")
    st.write("Recency:", recency)
    st.write("Frequency:", frequency)
    st.write("Monetary:", monetary)
    st.write("\nClustering Results:")

      
# Answers & Conclusion
elif options == 'Answers & Conclusion':

  st.header('Answers & Conclusion')
  visualization = st.selectbox('Choose Visualization',
                        ['Highest Rental in a Day',
                         'Rental Count Per Month',
                         'Rental Distribution Per Weather Condition'])
                         
  if visualization == 'Highest Rental in a Day':
        hourly_average = df.groupby('hr')['cnt'].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=hourly_average, x='hr', y='cnt', marker='o', color='skyblue', linewidth=2, linestyle='--', dashes=(5, 2))
        plt.title('Average Pattern of Bike Sharing Bicycle Use in a Day', fontsize=16)
        plt.xlabel('Hour', fontsize=12)
        plt.ylabel('Average Loan Amount', fontsize=12)
        plt.xticks(np.arange(24), fontsize=10)  # Menampilkan semua jam dalam sumbu x
        plt.yticks(fontsize=10)
        plt.grid(True)  # Menambahkan grid untuk memudahkan pembacaan

        st.pyplot(fig)

        st.write("""
        **Conclusion:** 
                 1. From the graph obtained, it can be seen that Bike Sharing lending reaches its highest peak at 17:00 in a day, while the lowest borrowing occurs at 04:00. This shows that the pattern of sharing bicycle use varies throughout the 24 hours of the day. The peak of borrowing at 17:00 may occur due to work time so people choose to use bike sharing as a means of transportation. On the other hand, the lowest borrowing at 04:00 is caused by the lack of activity or activities at that time, such as sleeping and the few people who are outside the house at that time. Therefore, understanding this pattern can help in planning bike sharing resource management, such as bicycle stock management and customer service planning, to optimize the use of bike sharing throughout the day.
        """)
  
  elif visualization == 'Rental Count Per Month':
        monthly_rentals = df.groupby('mnth')['cnt'].sum()

        fig, ax = plt.subplots(figsize=(10, 6))
        monthly_rentals.plot(kind='bar', color='Green')
        plt.title('Number of Bike Sharing Borrowed Every Month')
        plt.xlabel('Month')
        plt.ylabel('Borrowing Amount')
        plt.xticks(rotation=0)
        plt.grid(axis='y')

        # Menambahkan marker untuk puncak tertinggi
        max_month = monthly_rentals.idxmax()
        max_rentals = monthly_rentals.max()
        plt.text(max_month - 1, max_rentals + 1000, f'Peak: {max_rentals}', ha='center', color='red', fontsize=12)

        # Mengatur skala sumbu y agar lebih mudah dibaca
        plt.ticklabel_format(style='plain', axis='y')

        st.pyplot(fig)

        st.write("""
        **Conclusion:** 
                 2. If the hour and day data are combined and analyzed, it can be seen that August has the highest number of bike sharing loans, reaching 702,388. This may be due to several factors such as holidays or weather that is conducive to cycling. In contrast, January has the lowest loan amounts. This can be caused by weather that is less conducive to cycling, such as winter or bad weather conditions. By knowing these patterns, bike sharing service providers can carry out more effective marketing strategies, such as targeting promotions in months with high borrowing and optimizing bicycle stock based on seasonal trends. In addition, this can also be a consideration in operational planning, such as bicycle care and maintenance, as well as resource allocation during various seasons of the year.
        """)

  elif visualization == 'Rental Distribution Per Weather Condition':
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='weathersit', palette='viridis')
    plt.title('Distribution of Bike Sharing Use Based on Weather Conditions')
    plt.xlabel('Weather')
    plt.ylabel('Borrowing Amount')
    plt.xticks(ticks=[0, 1, 2, 3], labels=['1. Bright', '2. Fog', '3. Drizzle', '4. Rain'], rotation=45)
    
    st.pyplot(plt.gcf())

    st.write("""
    **Conclusion:** 
    3. From the diagram obtained, it can be seen that weather plays an important role in the use of bike sharing services. On days with sunny weather (labelled as 1: Bright), there is a significant spike in the use of bike sharing, while on days with foggy weather (labelled as 2: Fog) and drizzling (labelled as 3: Drizzle), the use of bike sharing is lower. This suggests that people prefer to use bike sharing services more when the weather is clear and less favorable when it's foggy or drizzling. Understanding this pattern can help bike sharing service providers adjust their operational strategies, such as offering promotions during good weather to encourage usage or improving service reliability during inclement weather to retain customers.
    """)

