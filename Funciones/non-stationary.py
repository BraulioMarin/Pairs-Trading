import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller

symbols = ['F', 'GM']

start_date = '2014-02-23'

stocks = yf.download(symbols, start=start_date)['Close']

fig, ax1 = plt.subplots(figsize=(14, 7))

color = 'tab:blue'
ax1.set_xlabel('Fecha')
ax1.set_ylabel('Ford (F)', color=color)
ax1.plot(stocks.index, stocks['F'], color=color, label='Ford (F)')
ax1.tick_params(axis='y', labelcolor=color)
ax1.grid(True)

ax2 = ax1.twinx()
color = 'tab:orange'
ax2.set_ylabel('General Motors (GM)', color=color)
ax2.plot(stocks.index, stocks['GM'], color=color, label='General Motors (GM)')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Comparación de Precios de F y GM (Últimos 10 años)')
plt.show()

def test_stationarity(timeseries):
    print('Resultados de la prueba de Dickey-Fuller:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Estadístico de prueba', 'p-value', '#Lags Usados', 'Número de observaciones usadas'])
    for key, value in dftest[4].items():
        dfoutput['Valor crítico (%s)' % key] = value
    print(dfoutput)

print("Prueba de Dickey-Fuller para Ford (F):")
test_stationarity(stocks['F'].dropna())

print("\nPrueba de Dickey-Fuller para General Motors (GM):")
test_stationarity(stocks['GM'].dropna())