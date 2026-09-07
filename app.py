# lab_eda_gui.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Page Configuration

st.set_page_config(
    page_title="EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("Exploratory Data Analysis Interface")


# 2. Sidebar: Dataset Ingestion

#set header for sidebar
st.sidebar.header("Dataset Ingestion")

#create a file uploader in the sidebar for CSV files
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV file",
    type=["csv"]
)

if uploaded_file is not None:
    # Read dataset
    try:
        df = pd.read_csv(uploaded_file)

        # Validate that the dataset is not empty
        if df.empty:
            st.error("The uploaded CSV file is empty.")
            st.stop()

    except Exception as e:
        st.error(f"Invalid CSV file. Please upload a valid CSV dataset.\n\nError: {e}")
        st.stop()

        
    # 3. Dataset Overview
    
    #set subheader for dataset overview
    st.subheader("Dataset Overview")

    st.write("**First 5 Rows:**")
    #display the first 5 rows of the dataset
    st.dataframe(df.head(5), use_container_width=True)

    #display the shape of the dataset
    st.write(f"**Dataset Shape:** {df.shape[0]} rows × {df.shape[1]} columns")

    st.write("**Column Data Types:**")
    #display the data types of each column in the dataset
    st.dataframe(
        df.dtypes.astype(str).to_frame("Data Type"),
        use_container_width=True
    )

    # Missing value summary
    st.write("**Missing Values per Column:**")
    #display the count and percentage of missing values for each column in the dataset

    missing_values = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Missing Percentage": (
            df.isnull().sum() / len(df) * 100
        ).round(2)
    })

    st.dataframe(
        missing_values,
        use_container_width=True
    )
    

    # Basic statistics for numerical columns
    st.write("**Basic Numerical Statistics:**")
    #display the basic statistics

    numerical_columns = df.select_dtypes(
        include="number"
    ).columns

    if len(numerical_columns) > 0:

        numerical_stats = pd.DataFrame({
            "Mean": df[numerical_columns].mean(),
            "Median": df[numerical_columns].median(),
            "Minimum": df[numerical_columns].min(),
            "Maximum": df[numerical_columns].max()
        })

        st.dataframe(
            numerical_stats,
            use_container_width=True
        )

    else:
        st.info("No numerical columns found.")

    
    # 4. Attribute Selection
    
    #set header for attribute selection in the sidebar
    st.sidebar.header("Attribute Selection")

    #create a selectbox in the sidebar to choose an attribute for visualization
    selected_column = st.sidebar.selectbox(
        "Select an attribute:",
        df.columns
    )


    # Detect column type

    if pd.api.types.is_numeric_dtype(df[selected_column]):
        column_type = "Numerical"
    else:
        column_type = "Categorical"

    st.write(f"**Selected Attribute:** {selected_column}")
    st.write(f"**Attribute Type:** {column_type}")


    
    # 5. Visualization Rendering
    
    st.subheader("Visualization")

    if column_type == "Numerical":
        # Histogram with seaborn

        fig, ax = plt.subplots()

        sns.histplot(
            data=df,
            x=selected_column,
            kde=True,
            ax=ax
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        ax.set_title(
            f"Distribution of {selected_column}"
        )

        st.pyplot(fig)

    else:
        # Bar chart for categorical

        value_counts = df[selected_column].fillna(
            "Missing"
        ).value_counts()

        fig, ax = plt.subplots()

        sns.barplot(
            x=value_counts.index,
            y=value_counts.values,
            ax=ax
        )

        ax.set_xlabel(selected_column)
        ax.set_ylabel("Frequency")
        ax.set_title(
            f"Frequency Distribution of {selected_column}"
        )

        plt.xticks(rotation=45)

        st.pyplot(fig)    

else:
    st.info("Please upload a CSV file to start EDA.")