import pandas as pd
import pyodbc

def load_eo_combined():
    print("Connecting to EO Combined...")

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=vm-vik-sql-03.corp.hpicloud.net;"
        "DATABASE=PS_Viking_EO;"
        "UID=user_name;"
        "PWD=pswd;"
        "Encrypt=no;"
        "TrustServerCertificate=yes;",
        timeout=5
    )

    print("Connected EO Combined!")

    query = """
    SELECT TOP 1000
        [Family],
        [Family_Adj],
        [Business Unit],
        [Disc Date],
        [ODM],
        CAST([RDP/Week] AS DATETIME) AS [RDP/Week],
        [OBS Source],
        [OBS Total Liability After Mitigation],
        [Actual Shipments],
        [Forecast Shipments],
        CASE 
            WHEN [Code Name Allocated] = 'NANTUCKET 1.0' THEN 'NANTUCKET17'
            WHEN [Code Name Allocated] = 'CANNONBALL 2.0' THEN 'CANNONBALL2'
            ELSE [Code Name Allocated]
        END AS [Code Name Allocated],
        [Product Group Allocated],
        [Product Group],
        [Data_Type]
    FROM PS_Viking_EO.tab.EO_Combined
    WHERE
        [RDP/Week] >= '2024-11-01'
        AND [Data_Type] IN ('E&O', 'OOW')
        AND [OBS Source] = 'Automated'
        AND [Product Group] NOT IN ('Accessories', 'Displays')
        AND [Product Group Allocated] IS NOT NULL
        AND [Family] NOT LIKE '%,%'
        AND [Family] NOT LIKE '%;%'
    """

    print("Running EO Combined query...")
    df = pd.read_sql(query, conn)

    print("EO Combined Done!")

    return df
