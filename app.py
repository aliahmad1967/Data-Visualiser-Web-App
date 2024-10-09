import streamlit as st
import sys
import subprocess
import importlib

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

required_packages = ['pandas', 'matplotlib', 'seaborn']
missing_packages = []

for package in required_packages:
    if importlib.util.find_spec(package) is None:
        missing_packages.append(package)

if missing_packages:
    st.error(f"The following required packages are missing: {', '.join(missing_packages)}")
    st.info("Please install the missing packages using the following command in your terminal or command prompt:")
    st.code(f"pip install {' '.join(missing_packages)}")
    st.stop()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set the page config
st.set_page_config(page_title='Data Visualizer',
                   layout='centered',
                   page_icon='📊')

# Title
st.title('📊 Data Visualizer')

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    col1, col2 = st.columns(2)
    columns = df.columns.tolist()
    
    with col1:
        st.write("")
        st.write(df.head())
    
    with col2:
        # Allow the user to select columns for plotting
        x_axis = st.selectbox('Select the X-axis', options=columns+["None"])
        y_axis = st.selectbox('Select the Y-axis', options=columns+["None"])
        plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
        # Allow the user to select the type of plot
        plot_type = st.selectbox('Select the type of plot', options=plot_list)
    
    # Generate the plot based on user selection
    if st.button('Generate Plot'):
        fig, ax = plt.subplots(figsize=(6, 4))
        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
            y_axis='Density'
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
            y_axis = 'Count'
        
        # Adjust label sizes
        ax.tick_params(axis='x', labelsize=10)  # Adjust x-axis label size
        ax.tick_params(axis='y', labelsize=10)  # Adjust y-axis label size
        
        # Adjust title and axis labels with a smaller font size
        plt.title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        plt.xlabel(x_axis, fontsize=10)
        plt.ylabel(y_axis, fontsize=10)
        
        # Show the results
        st.pyplot(fig)
else:
    st.info("Please upload a CSV file to begin.")