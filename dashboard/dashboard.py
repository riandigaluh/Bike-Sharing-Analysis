import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Memuat Dataset
url = "https://raw.githubusercontent.com/riandigaluh/Bike-Sharing-Analysis/refs/heads/master/dashboard/bike_day_2012.csv"
bike_df = pd.read_csv(url)

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/riandigaluh/Bike-Sharing-Analysis/refs/heads/master/dashboard/logo.png")
    
    months = bike_df['month'].unique()
    selected_month = st.selectbox('Filter by Month', months)

# Memfilter data berdasarkan bulan yang dipilih
main_df = bike_df[bike_df['month'] == selected_month]

# Konten Utama
st.title('Exploring the Impact of Weather on Bike Rentals in 2012')
st.subheader(f"Bike Rental Statistics in {selected_month}")

# Membuat kolom untuk metrik
col1, col2, col3, col4 = st.columns(4)

with col1: 
    total_rentals = main_df['total'].sum()
    st.metric("Total Rentals", value=f"{total_rentals:,.0f}")

with col2: 
    mean_rentals = main_df['total'].mean()
    st.metric("Mean", value=f"{mean_rentals:,.0f}")

with col3: 
    min_rentals = main_df['total'].min()
    st.metric("Min", value=f"{min_rentals:,.0f}")

with col4: 
    max_rentals = main_df['total'].max()
    st.metric("Max", value=f"{max_rentals:,.0f}")

# Menambahkan Pie Chart berdasarkan weathersit
st.subheader("Distribution of Bike Rentals by Weather Condition")

weathersit_data = main_df.groupby('weathersit')['total'].sum()
weathersit_count = main_df['weathersit'].value_counts()

weather_cols = st.columns(len(weathersit_count))
for i, (weather, count) in enumerate(weathersit_count.items()):
    with weather_cols[i]:
        st.metric(weather, f"{count} days")

color_mapping = {
    'Clear/Partly Cloudy': '#ff9999',
    'Misty/Cloudy': '#66b3ff',
    'Light Snow/Rain': '#99ff99',
    'Severe Weather': '#ffcc99'
}

colors = [color_mapping[ws] for ws in weathersit_data.index]

explode = (0.1,) * len(weathersit_data)
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    weathersit_data.values, 
    labels=None,
    autopct=lambda p: f'{p:.1f}%\n({int(p / 100 * total_rentals)})',  
    colors=colors,
    startangle=90, 
    explode=explode,
    textprops=dict(color="black")
)
ax.axis('equal')

ax.legend(wedges, weathersit_data.index, title="Weather Condition", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

for text in texts:
    text.set_fontsize(12)  
for autotext in autotexts:
    autotext.set_color("black")  
    autotext.set_fontsize(10)  

st.pyplot(fig)

# Bar Chart untuk casual dan registered user berdasarkan weathersit
st.subheader("Number of Customers by Weather Condition")

casual_user_data = main_df.groupby('weathersit')['casual'].sum()
registered_user_data = main_df.groupby('weathersit')['registered'].sum()

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots(figsize=(25, 15))  
    
    sns.barplot(
        y=casual_user_data.index, 
        x=casual_user_data.values,
        palette=['#ff9999'],
        ax=ax
    )
    ax.set_title("Total Casual Users by Weather Condition", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel("Number of Casual Users", fontsize=25)  
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    for i, value in enumerate(casual_user_data.values):
        percentage = (value / casual_user_data.sum()) * 100  
        ax.text(
            value + 10, i, f"{value}", 
            va='center', fontsize=20, color='black'  
        )
        
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots(figsize=(25, 15))  
    
    sns.barplot(
        y=registered_user_data.index, 
        x=registered_user_data.values,
        palette=['#66b3ff'],
        ax=ax
    )
    ax.set_title("Total Registered Users by Weather Condition", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel("Number of Registered Users", fontsize=25)  
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)

    for i, value in enumerate(registered_user_data.values):
        ax.text(
            value + 10, i, f"{value}", 
            va='center', fontsize=20, color='black'  
        )

    st.pyplot(fig)

# Scatter plot pengaruh suhu terhadap jumlah penyewaan sepeda
st.subheader("Effects of Temperature on Bike Rentals")

# Metrik pada suhu
col1, col2, col3 = st.columns(3)

with col1:
    avg_temp = main_df['temperature'].mean()
    st.metric("Average Temperature", value=f"{avg_temp:.2f} °C")

with col2:
    min_temp = main_df['temperature'].min()
    st.metric("Minimum Temperature", value=f"{min_temp:.2f} °C")

with col3:
    max_temp = main_df['temperature'].max()
    st.metric("Maximum Temperature", value=f"{max_temp:.2f} °C")

# Menyiapkan data untuk scatter plot
scatter_fig, scatter_ax = plt.subplots(figsize=(10, 5))

scatter_ax.scatter(main_df['temperature'], main_df['total'], 
                   c=main_df['weathersit'].map(color_mapping),  
                   alpha=0.6, edgecolors='w', s=100)  

scatter_ax.set_title("Temperature vs Total Rentals", fontsize=25)
scatter_ax.set_xlabel("Temperature", fontsize=20)
scatter_ax.set_ylabel("Total Rentals", fontsize=20)

st.pyplot(scatter_fig)

# Footer
st.caption('Copyright (c) Dicoding 2023')
