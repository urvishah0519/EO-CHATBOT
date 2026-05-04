import pandas as pd

def load_feedback():
    print("Loading Feedback file...")

    file_path = r"C:\Users\ShUr837\HP Inc\PS Inventory Planning Data and Analytics Team - On Order Cancellation\Feedback_Sheet_Final.xlsx"
    df = pd.read_excel(file_path)

    print("Feedback loaded!")

    return df