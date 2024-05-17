# %%
import streamlit as st
from elasticsearch import Elasticsearch
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()

hostname = os.getenv("DEMO_SEARCH_HOSTNAME")
auth_user = os.getenv("DEMO_SEARCH_AUTH_USER")
auth_pass = os.getenv("DEMO_SEARCH_AUTH_PASS")
cloud_id = os.getenv("DEMO_SEARCH_CLOUD_ID")
login_password = os.getenv("LOGIN_PASSWORD")



# Initialize Elasticsearch client
es = Elasticsearch(
    cloud_id=cloud_id,
    basic_auth=(auth_user, auth_pass),
)

# Function to perform search on Elasticsearch
def search_companies(query):
    body = {
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["name", "capital_iq_description"]
            }
        }
    }
    response = es.search(index="your_index_name", body=body)  # Update with your index name
    return response

# Streamlit app with password protection
def main():
    st.title("Company Search App")

    # Input field for search query
    search_query = st.text_input("Enter company name or description")

    if search_query:
        # Perform search
        results = search_companies(search_query)
        
        # Extract and display results
        hits = results['hits']['hits']
        if hits:
            data = []
            for hit in hits:
                source = hit['_source']
                data.append({
                    'capiq_id': source['alpha_id'],
                    'name': source['name'],
                    'description': source.get('capital_iq_description', 'N/A'),
                    'address': source.get('address', 'N/A'),
                    'homepage_url': source.get('homepage_url', 'N/A'),
                    'city': source.get('city', 'N/A'),
                    'country_code': source.get('country_code', 'N/A'),
                    'founded_year': source.get('founded_year', 'N/A'),
                    'employee_count_range': source.get('capital_iq_employee_count_range', 'N/A'),
                    'specialties': source.get('specialties', 'N/A'),
                })
            
            df = pd.DataFrame(data)
            st.write(df)
        else:
            st.write("No results found")

# Password check
def password_check():
    st.title("Authentication")
    password = st.text_input("Enter password", type="password")
    if password == login_password:  # Replace 'your_password' with your actual password
        st.success("Password correct")
        return True
    elif password:
        st.error("Password incorrect")
        return False
    return None

if __name__ == "__main__":
    if password_check():
        main()

# %%
