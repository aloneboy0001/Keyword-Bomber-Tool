# Import necessary libraries
import streamlit as st
import bomber
import asyncio
import pandas as pd

# Function to run asyncio code
def run_asyncio_code(keyword, country):
    # The API key is no longer required, so this function doesn't need it
    # This function calls the 'get_keyword_data' function from the 'bomber' module
    return asyncio.run(bomber.get_keyword_data(keyword, country))

# Function to display Keyword Data
def display_keyword_data(keyword_data):
    # Display keyword data in a nicely formatted manner
    st.markdown("## Keyword Data")
    for category, keywords in keyword_data.items():
        st.markdown(f"### {category}")
        # Convert the data to a pandas DataFrame for display
        df = pd.DataFrame.from_dict(keywords, orient='index').transpose()
        st.dataframe(df)

# Commenting out this function as AI report display is no longer needed
# def display_ai_report(ai_report):
#     # Display AI report analysis (now removed)
#     st.markdown("## AI Analysis Report")
#     st.markdown(ai_report)

# Streamlit UI layout setup
st.title("Keyword Bomber")  # App title
st.write("Enter the details below to fetch keyword data.")  # Instructions

# Text input fields for keyword and country
input_keyword = st.text_input("Enter the keyword", "Marketing Automation")  # Default keyword
input_country = st.text_input("Enter the country code", "US")  # Default country

# Commenting out the API key input as it’s no longer required
# API_KEY = st.text_input("Enter your OpenAI API Key", "sk-XXX")

# Button to trigger data fetching
if st.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        # Fetch data by calling the function (no API key passed anymore)
        result = run_asyncio_code(input_keyword, input_country)
        if result.get('success'):
            # Display the keyword data
            display_keyword_data(result['result']['keyword_data'])
            # Commenting out AI report display as it's removed
            # display_ai_report(result['result']['ai_report'])
        else:
            # Display error if fetching fails
            st.error("Failed to fetch data")
