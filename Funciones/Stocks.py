import yfinance as yf
import matplotlib.pyplot as plt

def download_data(tickers):
    # Descargar datos de Yahoo Finance
    data = yf.download(tickers, start="2015-01-01", end="2025-01-20")["Close"]
    data = data[tickers]
    return data

# Graficar los precios de cierre
def graficar_precios(data):
    plt.figure(figsize=(14, 7))
    plt.plot(data, label=['Ford (F)', 'General Motors (GM)'])
    plt.title('Precio de Cierre de F y GM (Últimos 10 años)')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de Cierre (USD)')
    plt.legend()
    plt.grid(True)
    plt.show()


def grafica_comparar(data, tickers):
    fig, ax1 = plt.subplots(figsize=(14, 7))

    color = 'tab:blue'
    ax1.set_xlabel('Fecha')
    ax1.set_ylabel(tickers[0], color=color)
    ax1.plot(data.index, data[tickers[0]], color=color, label=tickers[0])
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.grid(True)

    ax2 = ax1.twinx()
    color = 'tab:orange'
    ax2.set_ylabel(tickers[1], color=color)
    ax2.plot(data.index, data[tickers[1]], color=color, label=tickers[1])
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Comparación de Precios de {tickers[0]} y {tickers[1]}')

    plt.show()