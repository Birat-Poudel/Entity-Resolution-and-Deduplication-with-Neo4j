import pandas as pd

def fetch_csv_data():
    url = 'https://docs.google.com/spreadsheets/d/1d2aXpsKcTIarqS9LpHv8IXBus1BfgpFZG8J5p7_iMMk/pub?gid=1543451169&single=true&output=csv'
    df = pd.read_csv(url)
    return df.to_dict(orient='records')