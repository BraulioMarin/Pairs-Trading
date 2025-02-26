import yfinance as yf
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import pandas as pd
from main import tickers


start_date = '2014-02-23'
stocks = yf.download(tickers, start=start_date)['Close']

X = sm.add_constant(stocks[tickers[0]])
model = sm.OLS(stocks[tickers[1]], X)
results = model.fit()

residuals = results.resid

# Graficar los residuos
plt.figure(figsize=(14, 7))
plt.plot(residuals, label='Residuos de la regresión')
plt.axhline(0, color='red', linestyle='--', label='Línea de referencia (0)')
plt.title('Residuos de la regresión entre F y GM')
plt.xlabel('Fecha')
plt.ylabel('Residuos')
plt.legend()
plt.grid(True)
plt.show()

def test_stationarity(timeseries):
    print('Resultados de la prueba de Dickey-Fuller:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Estadístico de prueba', 'p-value', '#Lags Usados', 'Número de observaciones usadas'])
    for key, value in dftest[4].items():
        dfoutput['Valor crítico (%s)' % key] = value
    print(dfoutput)

print("Prueba de Dickey-Fuller en los residuos:")
test_stationarity(residuals.dropna())