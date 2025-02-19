# imports
import streamlit as st
import pandas as pd
import os
from io import BytesIO

# page 
st.set_page_config(page_title="Data Convertor", layout="wide")

# title
st.title("Data Sweep")

# heading
st.write("## transform your files between CSV and Excel formats with built-in data cleaning and visualization")

# upload file
uploaded_files = st.file_uploader("Upload your files here (CSV or Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

# check if files are uploaded
if uploaded_files:
    for file in uploaded_files:
        ext = os.path.splitext(file.name)[-1].lower()
        if ext == ".csv":
            df = pd.read_csv(file)
        elif ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("Unsupported file type: {ext}")
            continue

         # display files info and preview
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {(file.size/1024).__float__()}")

        # display preview
        st.write(df.head())

        # options for data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed successfully")

            with col2:
                if st.button(f"Remove Missing Values from {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values removed successfully")

            with col3:
                if st.button(f"Standardize Column Names for {file.name}"):
                    df.columns = df.columns.str.lower()
                    df.columns = df.columns.str.replace(" ", "_")
                    st.success("Column names standardized successfully")

            
            
    
        st.subheader("Convert Columns")
        columns = st.multiselect(f"Select columns to convert", df.columns, default=df.columns.to_list())
        df = df[columns]

        # data visualization

        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # convert to excel
        st.subheader("Convert Options")
        convertion_type = st.radio("Convert your file to", ("Excel", "CSV"), key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if convertion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(ext, ".csv")
                mime_type = "text/csv"

            elif convertion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(label=f"Download {file_name}", data=buffer, file_name=file_name, mime=mime_type)
        
            


