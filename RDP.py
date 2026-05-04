import pandas as pd
import pyodbc

def load_rdp_data():
    print("Connecting to PSOInventory (RDP)...")

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=VCSMASCOTSQLP.vcs.rd.hpicorp.net;"
        "DATABASE=PSOInventory;"
        "Trusted_Connection=yes;"          # 👈 use this (same as FCS)
        "Encrypt=no;"
        "TrustServerCertificate=yes;",
        timeout=5
    )

    print("Connected!")

    query = """
    SELECT TOP 1000 *
    FROM PSOInventory.dbo.RDP
    """

    print("Running RDP query...")
    df = pd.read_sql(query, conn)

    print("RDP Done!")

    return df