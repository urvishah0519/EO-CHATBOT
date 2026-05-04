import streamlit as st
from odm import load_data
from buy_sell import load_buy_sell
from EO_dollar import load_eo_combined
from First_customer_shipment import load_pso_data
from RDP import load_rdp_data
from feedback import load_feedback   # 👈 NEW

st.title("📊 Power BI Chatbot Prototype")
st.write("Ask questions about E&O Data, Buy/Sell, E&O$, First Customer Shipments, RDP, and Feedback")

# -------------------------------
# LOAD DATA
# -------------------------------
try:
    eo_df = load_data()
    buy_sell_df = load_buy_sell()
    eo_dollar_df = load_eo_combined()
    shipment_df = load_pso_data()
    rdp_df = load_rdp_data()
    feedback_df = load_feedback()   # 👈 NEW

    data_loaded = True
    st.success("All data loaded successfully!")

except Exception as e:
    st.error(f"Error loading data: {e}")
    data_loaded = False

# -------------------------------
# USER INPUT
# -------------------------------
query = st.text_input("Ask a question...")

# -------------------------------
# CHATBOT LOGIC
# -------------------------------
def handle_query(q):
    q = q.lower()

    try:
        # ---------------- E&O ----------------
        if "total eo" in q or "total excess" in q:
            return f"Total E&O Excess: {eo_df['NetExcessValue'].sum():,.2f}"

        elif "top eo product" in q:
            return (
                eo_df.groupby("Product Group")["NetExcessValue"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

        # ---------------- BUY/SELL ----------------
        elif "total buy" in q or "total buy sell" in q:
            return f"Total Buy/Sell Value: {buy_sell_df['Total $_w/o ODM'].sum():,.2f}"

        elif "platform" in q:
            return (
                buy_sell_df.groupby("Platforms")["Total $_w/o ODM"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
            )

        # ---------------- E&O$ ----------------
        elif "eo$" in q or "liability" in q:
            return f"Total E&O$ Liability: {eo_dollar_df['OBS Total Liability After Mitigation'].sum():,.2f}"

        elif "forecast" in q or "actual" in q:
            actual = eo_dollar_df['Actual Shipments'].fillna(0).sum()
            forecast = eo_dollar_df['Forecast Shipments'].fillna(0).sum()
            return f"Actual: {actual:,.2f} vs Forecast: {forecast:,.2f}"

        # ---------------- CUSTOMER SHIPMENT ----------------
        elif "shipment" in q or "customer shipment" in q:
            return shipment_df.head()

        elif "total shipment" in q:
            return f"Total Rows in Shipment Data: {len(shipment_df):,}"

        elif "top family" in q:
            return shipment_df['FAMILY'].value_counts().head(10)

        # ---------------- RDP ----------------
        elif "rdp" in q:
            return rdp_df.head()

        elif "total rdp" in q:
            return f"Total RDP records: {len(rdp_df):,}"

        # ---------------- FEEDBACK ----------------
        elif "feedback" in q:
            return feedback_df.head()

        elif "total feedback" in q:
            return f"Total feedback records: {len(feedback_df):,}"

        # ---------------- COMPARISON ----------------
        elif "compare" in q:
            eo_total = eo_df['NetExcessValue'].sum()
            bs_total = buy_sell_df['Total $_w/o ODM'].sum()
            return f"E&O: {eo_total:,.2f} vs Buy/Sell: {bs_total:,.2f}"

        # ---------------- DEBUG ----------------
        elif "show eo" in q:
            return eo_df.head()

        elif "show buy" in q:
            return buy_sell_df.head()

        elif "show eo$" in q:
            return eo_dollar_df.head()

        elif "show shipment" in q:
            return shipment_df.head()

        elif "show rdp" in q:
            return rdp_df.head()

        elif "show feedback" in q:
            return feedback_df.head()

        elif "why" in q:
            return "Excess value is mainly driven by demand-supply mismatch and inventory imbalance."

        # ---------------- DEFAULT ----------------
        else:
            return """Try asking:

📊 E&O (Excess & Obsolete)
- total eo (total excess value across all products)
- top eo product (product groups with highest excess value)

💰 Buy/Sell Analysis
- total buy sell (total financial impact without ODM)
- top buy sell platform (platforms contributing highest buy/sell value)

⚖️ Comparison
- compare eo vs buy sell (compare excess value vs buy/sell value)

📈 E&O$ (Liability & Forecast)
- eo$ liability (total liability after mitigation)
- forecast vs actual (compare forecasted vs actual shipments)

🚚 Customer Shipments (FCS)
- show shipment (preview first customer shipment data)
- total shipment (total shipment records)
- top family (product families with highest shipments)

📅 RDP (Planning Data)
- show rdp (preview planning dataset)
- total rdp (total planning records)

📝 Feedback Analysis
- show feedback (preview feedback dataset)
- total feedback (total feedback entries)
"""
    except Exception as e:
        return f"Error: {str(e)}"

# -------------------------------
# RESPONSE
# -------------------------------
if data_loaded and query:
    result = handle_query(query)

    if isinstance(result, str):
        st.write(result)
    else:
        st.dataframe(result)