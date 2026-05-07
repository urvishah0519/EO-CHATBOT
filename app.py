import streamlit as st
from dotenv import load_dotenv
import os
import re
import pyodbc
import pandas as pd
from openai import AzureOpenAI

# -------------------------------
# LOAD ENV
# -------------------------------
load_dotenv()

# -------------------------------
# OPENAI SETUP
# -------------------------------
api_key = os.getenv("AZURE_OPENAI_API_KEY") or st.secrets["AZURE_OPENAI_API_KEY"]
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT") or st.secrets["AZURE_OPENAI_ENDPOINT"]

client = AzureOpenAI(
    api_key=api_key,
    api_version="2023-07-01-preview",
    azure_endpoint=endpoint
)

# -------------------------------
# UI
# -------------------------------
st.title("📊 Power BI Chatbot Prototype")
st.write("Ask questions about E&O, Buy/Sell, inventory, etc.")

# -------------------------------
# USER INPUT
# -------------------------------
query = st.text_input("Ask a question...")

# -------------------------------
# SQL GENERATION FUNCTION
# -------------------------------
def generate_sql(query):
    prompt = f"""
You are a SQL expert for Microsoft SQL Server.

Database: PS_Viking_EO
Schema: tab
Table: tab.EO_Validated_Files

Columns:
- NetExcessValue
- Product Group
- Platforms
- RDP/Week
- Data_Type

Rules:
- Only SELECT queries
- No DELETE, UPDATE, INSERT
- Return ONLY SQL (no markdown, no explanation)

User question:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return ONLY raw SQL. No markdown."},
            {"role": "user", "content": prompt}
        ]
    )

    raw_sql = response.choices[0].message.content

    # SIMPLE CLEANING
    sql_query = raw_sql

    # extract only SQL from SELECT onwards
    upper_sql = sql_query.upper()
    if "SELECT" in upper_sql:
        index = upper_sql.index("SELECT")
        sql_query = sql_query[index:]

    sql_query = sql_query.replace(
    "TAB.EO_VALIDATED_FILES",
    "tab.EO_Validated_Files"
)

    sql_query = sql_query.replace(
    "tab.eo_validated_files",
    "tab.EO_Validated_Files"
)
    if "GROUP BY [Product Group]" in sql_query:
        sql_query = sql_query.replace(
        "GROUP BY [Product Group]",
        "WHERE [Product Group] IS NOT NULL GROUP BY [Product Group]"
    )

    return sql_query.strip()

# -------------------------------
# RUN SQL FUNCTION
# -------------------------------
def run_query(sql_query):
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=vik-sql-prd-03.corp.hpicloud.net;"
        "DATABASE=PS_Viking_EO;"
        "UID=EO_analytics_svc;"
        f"PWD={os.getenv('DB_PASSWORD')};"
        "Encrypt=no;"
        "TrustServerCertificate=yes;"
    )

    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df

# -------------------------------
# RESPONSE
# -------------------------------
if query:
    try:
        # Step 1: Generate SQL
        sql_query = generate_sql(query)

        #  Show CLEAN SQL (no formatting issues)
        #st.write("### Generated SQL")
        #st.text(sql_query)

        # Step 2: Execute
        df = run_query(sql_query)

        # Step 3: Show data
        st.write("### Result")
        st.dataframe(df)

        # Step 4: AI Insights
        try:
            explanation = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Explain insights clearly in business terms."},
                    {
                        "role": "user",
                        "content": f"Question: {query}\n\nData:\n{df.head(10).to_string()}"
                    }
                ]
            )

            st.write("### 📊 Insights")
            st.write(explanation.choices[0].message.content)

        except:
            st.warning("Could not generate insights.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
