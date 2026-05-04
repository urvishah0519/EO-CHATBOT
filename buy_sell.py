import pandas as pd
import pyodbc

def load_buy_sell():
    print("Connecting to Buy/Sell...")

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=vm-vik-sql-03.corp.hpicloud.net;"
        "DATABASE=PS_Viking_EO;"
        "UID=EO_analytics_svc;"
        "PWD=4y*yVK9Z%5Qe;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;",
        timeout=5
    )

    print("Connected Buy/Sell!")

    query = """
    SELECT TOP 1000
        CAST([RDP Reference Date] AS DATETIME) AS [RDP Reference Date],
        CAST([Disc Date] AS DATETIME) AS [Disc Date],
        [Feature Type],
        [Feature Value],
        CASE 
            WHEN [Platforms] = 'NANTUCKET 1.0' THEN 'NANTUCKET17'
            WHEN [Platforms] = 'CANNONBALL 2.0' THEN 'CANNONBALL2'
            WHEN [Platforms] = 'ELDORADO' THEN 'ELDORADOWKS'
            ELSE [Platforms]
        END AS [Platforms],
        [Net_Excess Qty_w/o ODM],
        [Total $_w/o ODM],
        [Product Group],
        [ODM]
    FROM PS_Viking_EO.tab.VI_Buy_Sell_Accrual
    WHERE 
        [Product Group] IS NOT NULL
        AND [Product Group] NOT IN ('Accessories', 'Displays')
        AND [RDP Reference Date] >= '2024-11-01'
        AND [Source] = 'Validated'
    """

    print("Running Buy/Sell query...")
    df = pd.read_sql(query, conn)
    print("Buy/Sell Done!")

    return df