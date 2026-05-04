# EO-CHATBOT-
AI-powered chatbot prototype for the Platform E&amp;O Review dashboard, integrating multiple data sources including PS_Viking, PSOInventory, and SharePoint. Built using Python and Streamlit, it enables users to query business data through predefined analytical prompts . Designed to be extended with Azure OpenAI for natural language query understanding.


# AI-Powered Chatbot for Platform E&O Review

## Overview
This project is a chatbot-based analytics prototype built for the Platform E&O Review dashboard. It enables users to interact with business data through a conversational interface instead of navigating multiple dashboard views.

## Key Features
- Multi-source data integration:
  - PS_Viking (E&O, Buy/Sell, E&O$)
  - PSOInventory (FCS, RDP)
  - SharePoint (Feedback)
- Streamlit-based interactive UI
- Rule-based query handling (totals, comparisons, top contributors)
- Cross-dataset analytical insights

## Tech Stack
- Python
- Streamlit
- Pandas
- PyODBC / SQL Server
- SharePoint (via OneDrive sync)

## Example Queries
- total eo
- total buy sell
- compare eo vs buy sell
- top buy sell platform
- total shipment
- show feedback

## How to Run
```bash
pip install -r requirements.txt
streamlit run app.py
