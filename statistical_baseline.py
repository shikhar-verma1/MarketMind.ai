import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

class statisticalbaseline:
    def __init__(self,data_path):
        self.data_path = data_path 

    def calculate_parameters(self):
        df = pd.read_csv(self.data_path,index_col = "Date",parse_dates=True)
        returns = df["Close"].pct_change().dropna()
        mu = returns.mean()
        si = returns.std()
        so = df["Close"].iloc[-1]
        return mu,si,so
    
    def simulate_gbm(self,so,mu,si,days =30,simulations=300):
        print(f"running the simulation")
        dt = 1
        paths = np.zeros((days,simulations))
        paths[0] = so

        for t in range(1,days):
            z = np.random.standard_normal(simulations)
            paths[t] = paths[t-1] * np.exp((mu - 0.5*si**2)*dt + si*np.sqrt(dt)+z)

        return paths

    def plot_simulate(self,paths,ticker):
        plt.figure(figsize=(10,6))
        plt.plot(paths,alpha=0.3,color="blue",linewidth=1,label="expected mean path")
        plt.title(f"Makemind engine {ticker}  - 30 days probability Matrix")
        plt.xlabel("Trading days into the future")
        plt.ylabel("simulated price")
        plt.legend()

if __name__ == "__main__":
    ticker = "NVDA"
    file_path = f"./data/{ticker}_historical.csv"
    
    if not os.path.exists(file_path):
        print(f"CRITICAL: Could not find data at {file_path}. Run data_harvester.py first.")
    else:
        # Initialize the engine
        baseline = statisticalbaseline(file_path)
        
        # Calculate the math
        mu, sigma, S0 = baseline.calculate_parameters()
        print(f"Statistical Baselines locked - Drift (mu): {mu:.6f}, Volatility (sigma): {sigma:.6f}, Current Price: ${S0:.2f}")
        
        # Run 100 simulations for the next 30 days
        simulated_paths = baseline.simulate_gbm(S0, mu, sigma, days=30, simulations=100)
        
        # Visualize the probability matrix
        baseline.plot_simulate(simulated_paths, ticker)