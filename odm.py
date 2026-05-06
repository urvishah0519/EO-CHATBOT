import pandas as pd
import pyodbc

def load_data():
    print("Connecting...")

    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 18 for SQL Server};"
        "SERVER=vik-sql-prd-03.corp.hpicloud.net;"
        "DATABASE=PS_Viking_EO;"
        "UID=EO_analytics_svc;"
        "PWD=4y*yVK9Z%5Qe;"
        "Encrypt=no;"                 # important for now
        "TrustServerCertificate=yes;",
        timeout=5
    )

    print("Connected!")

    query = """
SELECT TOP 1000
    [ODM],
    [ODMPartNumber],
    [ODMDescription],
    [Program Name],
    TRY_CAST([Disc Date] AS DATETIME) AS [Disc Date],
    [Supp_Manufacturer],
    [SA],
    TRY_CAST([RDP/Week] AS DATETIME) AS [RDP/Week],
    [Qty on Hand],
    [Qty on Order],
    [NetExcessQuantity],
    [NetExcessValue],
    [TotalLiabilityAfterMitigation],
    [AV_BOM],
    [Sub-Category],
    [Source],
    [Family_Adj],
    [L6 Flag],
    CASE 
        WHEN [Code Name Allocated] = 'NANTUCKET 1.0' THEN 'NANTUCKET17'
        WHEN [Code Name Allocated] = 'CANNONBALL 2.0' THEN 'CANNONBALL2'
        WHEN [Code Name Allocated] = 'ELDORADO' THEN 'ELDORADOWKS'
        ELSE [Code Name Allocated]
    END AS [Code Name Allocated],
    [Product Group],
    [Data_Type],
    [Process Flag]
FROM PS_Viking_EO.tab.EO_Validated_Files
WHERE
    [Product Group] IS NOT NULL
    AND [Product Group] NOT IN ('Accessories', 'Displays')
    AND [RDP/Week] >= '2024-11-01'
    AND [Data_Type] IN ('E&O', 'OOW')
    AND [Source] = 'Automated'
    AND [Process Flag] NOT IN ('Duplicate Entry')
"""

    print("Running query...")
    df = pd.read_sql(query, conn)
    print("Done!")

    return df
