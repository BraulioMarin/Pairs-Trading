import pandas as pd
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
            revenue2 = n_shares2 * price2 * (1 - com)  
            
            
            margin_requirement = revenue2 * 0.5 
            
            net_cost = cost1 - revenue2  
            if capital >= net_cost + margin_requirement:
                capital -= net_cost
                capital -= margin_requirement  
                positions.append((price1, price2, n_shares, -n_shares2, margin_requirement))
                
        elif signals["short_stock1"].iloc[i] and signals["long_stock2"].iloc[i]:  
            revenue1 = n_shares * price1 * (1 - com) 
            cost2 = n_shares2 * price2 * (1 + com)

            
            margin_requirement = revenue1 * 0.5  

            net_cost = cost2 - revenue1  
            if capital >= net_cost + margin_requirement:
                capital -= net_cost
                capital -= margin_requirement  
                positions.append((price1, price2, -n_shares, n_shares2, margin_requirement))

        
        elif signals["close"].iloc[i] and positions:
            total_profit = 0
            for pos in positions:
                pos_price1, pos_price2, shares1, shares2, margin = pos

                
                if shares1 > 0:  
                    profit1 = (price1 - pos_price1) * shares1 * (1 - com)
                else:  
                    profit1 = (pos_price1 - price1) * abs(shares1) * (1 - com)

                if shares2 < 0:  
                    profit2 = (pos_price2 - price2) * abs(shares2) * (1 - com)
                else: 
                    profit2 = (price2 - pos_price2) * shares2 * (1 - com)

                
                total_profit += profit1 + profit2
                capital += margin  

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