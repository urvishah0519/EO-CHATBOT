import pandas as pd
import pyodbc

def load_pso_data():
    print("Connecting to PSOInventory...")

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=VCSMASCOTSQLP.vcs.rd.hpicorp.net;" 
        "DATABASE=PSOInventory;"                   #  NEW DB
        "Trusted_Connection=yes;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;",
        timeout=5
    )

    print("Connected PSO!")

    query = """
SELECT TOP 200
    [FAMILY],
    [Program Name],
    [Family 1],
    [FCS DATE]
FROM PSOInventory.dbo.FCS
"""

    print("Running PSO query...")
    df = pd.read_sql(query, conn)

    print("PSO Done!")

    return df