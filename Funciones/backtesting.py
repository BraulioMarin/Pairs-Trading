import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_strategy(signals, initial_capital=1_000_000, com=0.00125, n_shares=35, margin_call_threshold=0.5):
    capital = initial_capital
    margin_call_level = initial_capital * margin_call_threshold  
    positions = []
    portfolio_value = [capital]
    dates = signals.index  

    for i in range(len(signals)):
        price1 = signals["stock1_price"].iloc[i]
        price2 = signals["stock2_price"].iloc[i]
        ratio = signals["hedge_ratio"].iloc[i]

        n_shares2 = int(n_shares * ratio)

        
        if signals["long_stock1"].iloc[i] and signals["short_stock2"].iloc[i]:
            cost1 = n_shares * price1 * (1 + com)
            if capital >= cost1:
                capital -= cost1  
                positions.append((price1, price2, n_shares, -n_shares2))

        elif signals["short_stock1"].iloc[i] and signals["long_stock2"].iloc[i]:
            cost2 = n_shares2 * price2 * (1 + com)
            if capital >= cost2:
                capital -= cost2  
                positions.append((price1, price2, -n_shares, n_shares2))

       
        if signals["close"].iloc[i] and positions:
            closed_positions = []

            for pos in positions:
                pos_price1, pos_price2, shares1, shares2 = pos
                current_price1 = price1
                current_price2 = price2

                if shares1 > 0:  
                    total_sale1 = current_price1 * shares1 * (1 - com)
                    capital += total_sale1  
                else:  
                    profit1 = (pos_price1 - current_price1) * abs(shares1) * (1 - com)
                    capital += profit1

                if shares2 < 0:  
                    profit2 = (pos_price2 - current_price2) * abs(shares2) * (1 - com)
                    capital += profit2
                else:  
                    total_sale2 = current_price2 * shares2 * (1 - com)
                    capital += total_sale2  

                closed_positions.append(pos)

            positions = []  

        
        if capital < margin_call_level and positions:
            print(f"⚠️ MARGIN CALL ACTIVADO EN EL DÍA {i} | Capital: ${capital:,.2f}")
            for pos in positions:
                pos_price1, pos_price2, shares1, shares2 = pos
                current_price1 = price1
                current_price2 = price2

                if shares1 > 0:  
                    total_sale1 = current_price1 * shares1 * (1 - com)
                    capital += total_sale1  
                else:  
                    profit1 = (pos_price1 - current_price1) * abs(shares1) * (1 - com)
                    capital += profit1

                if shares2 < 0:  
                    profit2 = (pos_price2 - current_price2) * abs(shares2) * (1 - com)
                    capital += profit2
                else:  
                    total_sale2 = current_price2 * shares2 * (1 - com)
                    capital += total_sale2  

            positions = []  

        portfolio_value.append(capital)

    final_value = portfolio_value[-1]
    print(f"\U0001F4B0 Valor final del portafolio: ${final_value:,.2f}")

    
    plt.figure(figsize=(12, 6))
    plt.plot(dates, portfolio_value[1:], label="Valor del Portafolio", color="blue")
    plt.title("Evolución del Portafolio con Margin Call")
    plt.xlabel("Año")
    plt.ylabel("Capital ($)")
    plt.xticks(dates[::int(len(dates)/10)].strftime('%Y'), rotation=45)  
    plt.legend()
    plt.grid(True)
    plt.show()

    return portfolio_value
