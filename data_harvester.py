import os
import yfinance as yf
import numpy as np

class Dataharvester():
    def __init__(self,data_dir = "./data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def fetch_historical_data(self,ticker_symbol,start_date,end_date):
        print(f"fetching data for {ticker_symbol}...")
        ticker = yf.Ticker(ticker_symbol) 
        df = ticker.history(start= start_date,end=end_date)
    
        file_path = f"{self.data_dir}/{ticker_symbol}_historical.csv"
        df.to_csv(file_path)
        print("Data saved to {file_path}")
        return df

if __name__ == "__main__":
    harvester = Dataharvester(data_dir="./data")
    df = harvester.fetch_historical_data("NVDA","2023-01-01", "2024-01-01")
    print(df.head())

