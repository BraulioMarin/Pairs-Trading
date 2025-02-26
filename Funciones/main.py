from Stocks import download_data, graficar_precios, grafica_comparar

tickers=["MSFT","BRK-B"]
def main():
    tickers=["MSFT","BRK-B"]
    data = download_data(tickers)
    graficar_precios(data)
    grafica_comparar(data,tickers)

if __name__ == '__main__':
    main()