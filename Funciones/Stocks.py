import yfinance as yf
import matplotlib.pyplot as plt

# Definir los símbolos de las acciones
symbols = ['F', 'GM']  # Delta Air Lines y American Airlines

# Definir el período de tiempo (últimos 10 años)
start_date = '2014-02-23'

# Descargar los datos históricos
stocks = yf.download(symbols, start=start_date)['Close']

# Graficar los precios de cierre
plt.figure(figsize=(14, 7))
plt.plot(stocks, label=['Ford (F)', 'General Motors (GM)'])
plt.title('Precio de Cierre de F y GM (Últimos 10 años)')
plt.xlabel('Fecha')
plt.ylabel('Precio de Cierre (USD)')
plt.legend()
plt.grid(True)
plt.show()