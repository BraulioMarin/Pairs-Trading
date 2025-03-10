import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_strategy(signals, initial_capital=1_000_000, com=0.00125, n_shares=100):
    capital = initial_capital
    positions = []
    portfolio_value = [capital]

    for i in range(len(signals)):
        price1 = signals["stock1_price"].iloc[i]
        price2 = signals["stock2_price"].iloc[i]
        ratio = signals["hedge_ratio"].iloc[i]

        n_shares2 = int(n_shares * ratio)

        if signals["long_stock1"].iloc[i] and signals["short_stock2"].iloc[i]:
            cost1 = n_shares * price1 * (1 + com)
            if capital >= cost1:
                capital -= cost1  # Restamos la compra total de stock1
                positions.append((price1, price2, n_shares, -n_shares2))

        elif signals["short_stock1"].iloc[i] and signals["long_stock2"].iloc[i]:
            cost2 = n_shares2 * price2 * (1 + com)
            if capital >= cost2:
                capital -= cost2  # Restamos la compra total de stock2
                positions.append((price1, price2, -n_shares, n_shares2))

        elif signals["close"].iloc[i] and positions:
            total_profit = 0
            closed_positions = []

            for pos in positions:
                pos_price1, pos_price2, shares1, shares2 = pos
                current_price1 = price1
                current_price2 = price2

                if shares1 > 0:  # Cierre de posición larga en stock1
                    total_sale1 = current_price1 * shares1 * (1 - com)
                    profit1 = total_sale1

                else:  # Cierre de posición corta en stock1
                    profit1 = (pos_price1 - current_price1) * abs(shares1) * (1 - com)

                if shares2 < 0:  # Cierre de posición corta en stock2
                    profit2 = (pos_price2 - current_price2) * abs(shares2) * (1 - com)

                else:  # Cierre de posición larga en stock2
                    total_sale2 = current_price2 * shares2 * (1 - com)
                    profit2 = total_sale2

                total_profit += profit1 + profit2
                closed_positions.append(pos)

            capital += total_profit  
            positions = []

        portfolio_value.append(capital)

    final_value = portfolio_value[-1]
    print(f"\U0001F4B0 Valor final del portafolio: ${final_value:,.2f}")

    plt.figure(figsize=(12, 6))
    plt.plot(portfolio_value, label="Valor del Portafolio", color="blue")
    plt.title("Evolución del Portafolio")
    plt.xlabel("Días")
    plt.ylabel("Capital ($)")
    plt.legend()
    plt.grid(True)
    plt.show()

    return portfolio_value
