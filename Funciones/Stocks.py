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
    plt.figure(figsize=(14, 7))

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # Primer eje (izquierda) para la primera acción
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel(tickers[0], color='blue')
    ax1.plot(data.index, data[tickers[0]], label=tickers[0], color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')

    # Segundo eje (derecha) para la segunda acción
    ax2 = ax1.twinx()
    ax2.set_ylabel(tickers[1], color='orange')
    ax2.plot(data.index, data[tickers[1]], label=tickers[1], color='orange')
    ax2.tick_params(axis='y', labelcolor='orange')

    # Título y formato
    plt.title(f'Comparación de Precios de {tickers[0]} y {tickers[1]}')
    fig.tight_layout()
    plt.grid(True)
    plt.show()