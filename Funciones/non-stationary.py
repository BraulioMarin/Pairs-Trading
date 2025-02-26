import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from statsmodels.tsa.stattools import adfuller

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