import pandas as pd
import os
# Define the directory where your CSV files are located
dir_path = os.path.dirname(os.path.realpath(__file__))

# Define the name of the specific CSV file you're looking for
csv_file_name = 'combinedfiles.csv'

# Create the full path to the CSV file
csv_file_path = os.path.join(dir_path, csv_file_name)

# Check if the file exists
if os.path.exists(csv_file_path):
    # Load the CSV file into a pandas DataFrame
    turnstile_data = pd.read_csv(csv_file_path)




import streamlit as st


st.title('MTA Turnstile Data Visualizations 🎈')


st.write('The plot below looks at the busiest 15 subway stations in NYC. The 42nd Street - Port Authority Station is the busiest in the city!')


import matplotlib.pyplot as plt
# turnstile_data = pd.read_csv('/home/cyrus/Documents/combinedfiles.csv')
turnstile_data.columns = turnstile_data.columns.str.strip()
turnstile_data = turnstile_data[turnstile_data['DATE'] != 'DATE']
turnstile_data['ENTRIES'] = turnstile_data['ENTRIES'].astype(int)
turnstile_data['EXITS'] = turnstile_data['EXITS'].astype(int)
turnstile_data['DATE'] = pd.to_datetime(turnstile_data['DATE'], errors='coerce')
turnstile_data['HOUR'] = turnstile_data['DATE'].dt.hour
st.set_option('deprecation.showPyplotGlobalUse', False)




# Calculate total footfall for each station
turnstile_data['FOOTFALL'] = turnstile_data['ENTRIES'] + turnstile_data['EXITS']
footfall_by_station = turnstile_data.groupby('STATION')['FOOTFALL'].sum().sort_values(ascending=False).reset_index()

# Plot the 15 stations with the highest footfall
st.write('Busiest 15 NYC Subway Stations')
st.bar_chart(footfall_by_station.set_index('STATION').head(15))



st.write('The plot below looks at the busiest days of the week in terms of foot-traffic, and Thursday is found to be the busiest day of the week')


# Copy the original DataFrame
turnstile_data_copy = turnstile_data.copy()

turnstile_data_copy['DATE'] = pd.to_datetime(turnstile_data_copy['DATE'], errors='coerce')

# Sort the dataframe and calculate daily entries and exits
sorted_data = turnstile_data_copy.sort_values(['C/A', 'UNIT', 'SCP', 'STATION', 'DATE'])
sorted_data['DAILY_ENTRIES'] = sorted_data.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['ENTRIES'].diff()
sorted_data['DAILY_EXITS'] = sorted_data.groupby(['C/A', 'UNIT', 'SCP', 'STATION'])['EXITS'].diff()

# Drop NA rows
sorted_data.dropna(subset=['DAILY_ENTRIES', 'DAILY_EXITS'], inplace=True)

# Outlier handling
filtered_data = sorted_data[(sorted_data['DAILY_ENTRIES'] >= 0) & (sorted_data['DAILY_ENTRIES'] <= 50000)]
filtered_data = filtered_data[(filtered_data['DAILY_EXITS'] >= 0) & (filtered_data['DAILY_EXITS'] <= 50000)]

# Compute total traffic and the day of the week
filtered_data['TOTAL_DAILY_TRAFFIC'] = filtered_data['DAILY_ENTRIES'] + filtered_data['DAILY_EXITS']
filtered_data['DAY_OF_WEEK'] = filtered_data['DATE'].dt.day_name()

# Now, compute total traffic for each day of the week
grouped_tdata = filtered_data.groupby('DAY_OF_WEEK')['TOTAL_DAILY_TRAFFIC'].sum().reset_index()

# Order the days of the week
ordered_days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
grouped_tdata['DAY_OF_WEEK'] = pd.Categorical(grouped_tdata['DAY_OF_WEEK'], categories=ordered_days, ordered=True)

# Sort by the ordered day of the week
grouped_tdata.sort_values('DAY_OF_WEEK', inplace=True)

plt.figure(figsize=[10,10])
plt.bar(grouped_tdata['DAY_OF_WEEK'], grouped_tdata['TOTAL_DAILY_TRAFFIC'])
plt.xlabel('Day of the Week')
plt.ylabel('Total Traffic')
plt.title('Daily Total Traffic')
st.pyplot()




st.write('The plot below allows you to look at entries and exits of specific turnstiles (or all) - just search or click the option you wish and it will automatically populate!')


def stations_plotting(stations):
    for station in stations:
        # Filter and aggregate data for the current station
        station_entries = turnstile_data[turnstile_data['STATION'] == station].groupby('DATE')['ENTRIES'].sum().reset_index()
        station_exits = turnstile_data[turnstile_data['STATION'] == station].groupby('DATE')['EXITS'].sum().reset_index()
        
        # Write a title for the line chart
        st.write(f"Station daily entries over time: {station}")
        
        # Create a line chart for the current station
        st.line_chart(station_entries.set_index('DATE'), use_container_width=True)

        # Write a title for the second line chart
        st.write(f"Station daily exits over time: {station}")

        # Create a second line chart for the current station
        st.line_chart(station_exits.set_index('DATE'), use_container_width=True)



# List of all stations
all_stations = turnstile_data['STATION'].unique().tolist()

# Add 'Select All' to the list
all_stations.insert(0, 'Select All')

# Multiselect box with 'Select All' option
selected_stations = st.multiselect('Select stations to plot daily entries and exits over time', all_stations)

# If 'Select All' is chosen, use all station names. Otherwise, use the selected stations
if 'Select All' in selected_stations:
    selected_stations = turnstile_data['STATION'].unique().tolist()

# Call the function with the selected stations
stations_plotting(selected_stations)