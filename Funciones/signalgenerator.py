import pandas as pd
import numpy as np
from kalman_filter import KalmanFilterHedgeRatio

def generate_trading_signals(stock1, stock2, window=50, initial_hedge_ratio=1.0):
   
  
   
    kf = KalmanFilterHedgeRatio()
    kf.x[1] = initial_hedge_ratio  
    hedge_ratios = []
    spreads = []

    for i in range(len(stock1)):
        if pd.notna(stock1.iloc[i]) and pd.notna(stock2.iloc[i]): 
            kf.predict()
            kf.update(stock1.iloc[i], stock2.iloc[i])

        hedge_ratio = kf.get_hedge_ratio()
        hedge_ratios.append(hedge_ratio)
        spread = stock2.iloc[i] - hedge_ratio * stock1.iloc[i]  
        spreads.append(spread)

    
    hedge_ratios_series = pd.Series(hedge_ratios, index=stock1.index)
    spreads_series = pd.Series(spreads, index=stock1.index)

    
    spread_mean = spreads_series.rolling(window=window, min_periods=1).mean()
    spread_std = spreads_series.rolling(window=window, min_periods=1).std()
    spread_std[spread_std < 1e-5] = 1e-5 
    z_score_series = (spreads_series - spread_mean) / spread_std

   
    signals = pd.DataFrame(index=stock1.index)
    signals["long_stock1"] = z_score_series < -1.5  
    signals["short_stock2"] = z_score_series < -1.5 
    signals["short_stock1"] = z_score_series > 1.5  
    signals["long_stock2"] = z_score_series > 1.5   
    signals["close"] = abs(z_score_series) < 0.5    

    
    signals["long_stock1"] = signals["long_stock1"] & ~signals["short_stock1"]
    signals["short_stock2"] = signals["short_stock2"] & ~signals["long_stock2"]
    signals["short_stock1"] = signals["short_stock1"] & ~signals["long_stock1"]
    signals["long_stock2"] = signals["long_stock2"] & ~signals["short_stock2"]

   
    signals["hedge_ratio"] = hedge_ratios_series
    signals["spread"] = spreads_series
    signals["z_score"] = z_score_series
    signals["stock1_price"] = stock1
    signals["stock2_price"] = stock2

    return signals