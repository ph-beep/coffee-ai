import streamlit as st
import pandas as pd
from PIL import Image
import os
from time import sleep
# import plotly.express as px
# import matplotlib.pyplot as plt

page_element="""
<style>
[data-testid="stAppViewContainer"]{
    background-image: url("https://wallpapercave.com/wp/wp1923703.jpg");
    background-size: cover;
}
h1 {
    color: #FFD700; /* Gold/Yellow for visibility */
    text-shadow: 2px 2px 4px #000000;
    }
h2 {
    color: #FFD700; /* Gold/Yellow for visibility */
    text-shadow: 2px 2px 4px #000000;
    }
p {
    color: #FFFF8F; /* Gold/Yellow for visibility */
    text-shadow: 2px 2px 4px #000000;
    }
</style>
"""

st.markdown(page_element, unsafe_allow_html=True)

# Get to ensure the favicon is in the same directory as the project
try:
    img = Image.open("./assets/favicon.ico")
except FileNotFoundError:
    img = None

# Get started with web page configuration
st.set_page_config(
    page_title="CoffeeAI - Enhanced Data Viewer",
    page_icon=img if img else"=",
    layout="centered"
)

st.title("Simple Data Viewer")
uploaded_file = st.file_uploader("Choose file to upload", type="xlsx")

if uploaded_file is not None:
    # Use a spinner to enhance the UX experience giving them a time to wait
    # while the file is being read
    with st.spinner("Loading data..."):
        sleep(1)
        df = pd.read_excel(uploaded_file)
        st.success("File loaded sucessfully!!")
        st.subheader("Data Preview")
        st.write(df.head())
    # Details
    st.subheader("Data Summary")
    st.write(df.describe())

    # Filter data
    columns = df.columns.tolist()
    st.subheader("Filter Data")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            selected_column = st.selectbox("Select column to filter by", columns, key="filter_col")
        
        # Ensure the selected column has unique values to show
        if selected_column in df.columns:
            unique_values = df[selected_column].unique()
            with col2:
                selected_values = st.selectbox("Select value", unique_values, key="filter_val")
            
            filtered_df = df[df[selected_column] == selected_values]
            st.markdown(f"**Filtered Results ({len(filtered_df)} Rows):**")
            st.dataframe(filtered_df)
    # Plot data
    with st.container(border=True):
        st.header("Visualize Data")
        plot_type = st.radio(
            "Choose your chart type:",
            ("Line Chart", "Bar Chart"),
            horizontal=True
    )
        
    col3, col4 = st.columns(2)
    with col3:
        x_column = st.selectbox("Select X-Axis Column (Categories/Time)", columns, key="x_col")
    with col4:
        y_column = st.selectbox("Select Y-Axis Column (Numeric Values)", columns, key="y_col")

    if st.button("Generate Plot", type="primary"):
        # Basic check to ensure the Y-axis column is numeric
        if pd.api.types.is_numeric_dtype(filtered_df[y_column]):
            try:
                # Use a spinner while generating the plot
                with st.spinner(f'Generating {plot_type}...'):
                    sleep(0.5) 
                    
                    # Set the X-axis column as the index for plotting
                    plot_data = filtered_df.set_index(x_column)[y_column]

                    if plot_type == 'Line Chart':
                        st.line_chart(plot_data)
                    elif plot_type == 'Bar Chart':
                        st.bar_chart(plot_data)
                        
                st.success('Plot generated! 🎨')
                
            except Exception as e:
                st.error(f"An error occurred while plotting: {e}")
                st.warning("Ensure the X-axis column does not contain duplicate values or check the data types.")
        else:
            # Error message if the Y-axis is not numerical
            st.error(f"The column **'{y_column}'** is not a numerical type. Please select a column with numbers for the Y-axis.")
