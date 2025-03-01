import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import os

DATA_FOLDER = "data"
DATA_FILE = os.path.join(DATA_FOLDER, "stocks.csv")

def download_data(tickers, folder=DATA_FOLDER, force_download=False):
    if not os.path.exists(folder):
        os.makedirs(folder)

    if os.path.exists(DATA_FILE) and not force_download:
        return load_data(folder)

    data = yf.download(tickers, start="2015-01-01", end="2025-01-20")["Close"]
    data.to_csv(DATA_FILE)
    return data

def load_data(folder=DATA_FOLDER):
    file_path = os.path.join(folder, "stocks.csv")
    df = pd.read_csv(file_path, index_col=0, parse_dates=True)
    return df

def plot_prices(data):
    plt.figure(figsize=(14, 7))
    for column in data.columns:
        plt.plot(data.index, data[column], label=column)
    
    plt.title('Precio de Cierre de los Activos (Últimos 10 años)')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de Cierre (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_normalized(data, tickers):
    normalized_data = data / data.iloc[0] * 100

    plt.figure(figsize=(14, 7))
    plt.plot(normalized_data.index, normalized_data[tickers[0]], label=tickers[0], color='blue')
    plt.plot(normalized_data.index, normalized_data[tickers[1]], label=tickers[1], color='orange')
    
    plt.title(f'Comparación de Precios Normalizados de {tickers[0]} y {tickers[1]}')
    plt.xlabel('Fecha')
    plt.ylabel('Índice Base 100')
    plt.legend()
    plt.grid(True)
    plt.show()