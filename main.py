import streamlit as st
import pandas as pd
import time
from googlesearch import search

def get_linkedin_url(query):
    try:
        for url in search(query, num=1, stop=1):
            if 'linkedin.com' in url:
                return url
        time.sleep(1)  # Lowered delay for demonstration
    except Exception as e:
        st.error(f"Error searching for {query}: {e}")
    return None

def get_website_url(query):
    try:
        for url in search(query, num=1, stop=1):
            return url
        time.sleep(1)  # Lowered delay for demonstration
    except Exception as e:
        st.error(f"Error searching for {query}: {e}")
    return None

def enrich_csv(data):
    for i, row in data.iterrows():
        person_query = f"{row.get('First Name', '')} {row.get('Last Name', '')} LinkedIn"
        company_query = f"{row.get('Company', '')} LinkedIn"
        website_query = f"{row.get('Company', '')} official website"
        data.at[i, 'LinkedIn URL'] = get_linkedin_url(person_query)
        data.at[i, 'Company LinkedIn URL'] = get_linkedin_url(company_query)
        data.at[i, 'Company Website'] = get_website_url(website_query)
    return data

st.title("Guided CSV Enrichment")

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    if st.button("Enrich CSV"):
        with st.spinner('Enriching...'):
            enriched_data = enrich_csv(data)
            st.success("Enrichment Complete")
            st.dataframe(enriched_data)
            csv = enriched_data.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "file.csv", "text/csv", key='download-csv')

