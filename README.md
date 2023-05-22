# Streamlit exploration

This is a basic visual exploration of MTA Turnstile data using Python + Streamlit, please keep in mind the main focus of this is to show basic visualizations of streamlit to anyone curious about Python's interactive web-app abilities

To be able to run this, please have the following installed:

1. pandas
2. matplotlib
3. seaborn
4. streamlit (of course)

First run the first two cells in the "MTA-links.ipynb" file. This will allow you to get the data that you need from the specified range. You can edit the date range by changing the start_date and end_date variables. It will grab the relevant files from the specified range, and concat them together. Be sure to adjust the filepath though, as the current filepath is for my local machine.

To run streamlit, please ensure that the combinedfiles.csv file and the streamlit_app.py script are in the same folder, or if they aren't/if there is an issue, please manually point to the folder where the combinedfiles.csv file is. The set-up to run is the following on my system (you may need to adjust on another OS):
1. Start VSCode/IDE of your choice/terminal
2. cd into the specific folder that the streamlit_app.py and combined files are in
3. Enter the following:
    * streamlit run streamlit_app.py

If you change the name of the streamlit file, be sure to update the name when running the script as well

The other cells in the MTA-links.ipynb were the beginning of my attempt to add an interactive map to the display as well, but I ended up not adding it - however, anyone who wishes to add it would have the geographic information already set up. I included the file with the geographic information as well. The code should standardize the names of stations as they have different formats since they came from different sources. 

Enjoy!
