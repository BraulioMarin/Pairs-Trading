import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest_strategy(signals, initial_capital=1_000_000, com=0.00125, n_shares=35, margin_call_threshold=0.5):
    capital = initial_capital
    margin_call_level = initial_capital * margin_call_threshold  # Nivel de margin call (50% del capital inicial)
    positions = []
    portfolio_value = [capital]
    dates = signals.index  # Extraer las fechas del DataFrame de señales

    for i in range(len(signals)):
        price1 = signals["stock1_price"].iloc[i]
        price2 = signals["stock2_price"].iloc[i]
        ratio = signals["hedge_ratio"].iloc[i]

        n_shares2 = int(n_shares * ratio)

        # 🟢 Apertura de posiciones
        if signals["long_stock1"].iloc[i] and signals["short_stock2"].iloc[i]:
            cost1 = n_shares * price1 * (1 + com)
            if capital >= cost1:
                capital -= cost1  # Compra de stock1
                positions.append((price1, price2, n_shares, -n_shares2))

        elif signals["short_stock1"].iloc[i] and signals["long_stock2"].iloc[i]:
            cost2 = n_shares2 * price2 * (1 + com)
            if capital >= cost2:
                capital -= cost2  # Compra de stock2
                positions.append((price1, price2, -n_shares, n_shares2))

        # 🔴 Cierre de posiciones por señal de cierre
        if signals["close"].iloc[i] and positions:
            closed_positions = []

            for pos in positions:
                pos_price1, pos_price2, shares1, shares2 = pos
                current_price1 = price1
                current_price2 = price2

                if shares1 > 0:  # Cierre de posición larga en stock1
                    total_sale1 = current_price1 * shares1 * (1 - com)
                    capital += total_sale1  # Agregamos la venta total al capital
                else:  # Cierre de posición corta en stock1
                    profit1 = (pos_price1 - current_price1) * abs(shares1) * (1 - com)
                    capital += profit1

                if shares2 < 0:  # Cierre de posición corta en stock2
                    profit2 = (pos_price2 - current_price2) * abs(shares2) * (1 - com)
                    capital += profit2
                else:  # Cierre de posición larga en stock2
                    total_sale2 = current_price2 * shares2 * (1 - com)
                    capital += total_sale2  # Agregamos la venta total al capital

                closed_positions.append(pos)

            positions = []  # Asegurar que todas las posiciones abiertas se cierren correctamente

        # ⚠️ MARGIN CALL: Cierra todas las posiciones solo si es estrictamente necesario
        if capital < margin_call_level and positions:
            print(f"⚠️ MARGIN CALL ACTIVADO EN EL DÍA {i} | Capital: ${capital:,.2f}")
            for pos in positions:
                pos_price1, pos_price2, shares1, shares2 = pos
                current_price1 = price1
                current_price2 = price2

                if shares1 > 0:  # Cierre de posición larga en stock1
                    total_sale1 = current_price1 * shares1 * (1 - com)
                    capital += total_sale1  # Agregamos la venta total al capital
                else:  # Cierre de posición corta en stock1
                    profit1 = (pos_price1 - current_price1) * abs(shares1) * (1 - com)
                    capital += profit1

                if shares2 < 0:  # Cierre de posición corta en stock2
                    profit2 = (pos_price2 - current_price2) * abs(shares2) * (1 - com)
                    capital += profit2
                else:  # Cierre de posición larga en stock2
                    total_sale2 = current_price2 * shares2 * (1 - com)
                    capital += total_sale2  # Agregamos la venta total al capital

            positions = []  # Se liquidan todas las posiciones

        portfolio_value.append(capital)

    final_value = portfolio_value[-1]
    print(f"\U0001F4B0 Valor final del portafolio: ${final_value:,.2f}")

    # 📈 Gráfica con fechas reales en el eje X
    plt.figure(figsize=(12, 6))
    plt.plot(dates, portfolio_value[1:], label="Valor del Portafolio", color="blue")
    plt.title("Evolución del Portafolio con Margin Call")
    plt.xlabel("Año")
    plt.ylabel("Capital ($)")
    plt.xticks(dates[::int(len(dates)/10)].strftime('%Y'), rotation=45)  # Mostrar solo algunos años
    plt.legend()
    plt.grid(True)
    plt.show()

    return portfolio_value
