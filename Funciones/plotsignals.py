import matplotlib.pyplot as plt
import pandas as pd

def plot_trading_signals(stock1, stock2, signals, threshold=1.5):
    
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 10), sharex=True)

    
    axes[0].plot(stock1.index, stock1, label="Stock 1", color="blue", linewidth=1.5)
    axes[0].plot(stock2.index, stock2, label="Stock 2", color="orange", linewidth=1.5)

    
    axes[0].scatter(
        stock1.index[signals["long_stock1"]], 
        stock1[signals["long_stock1"]], 
        marker="^", color="green", label="Compra Stock1", alpha=0.8, s=80
    )
    axes[0].scatter(
        stock1.index[signals["short_stock1"]], 
        stock1[signals["short_stock1"]], 
        marker="v", color="red", label="Venta en corto Stock1", alpha=0.8, s=80
    )

    axes[0].scatter(
        stock2.index[signals["long_stock2"]], 
        stock2[signals["long_stock2"]], 
        marker="^", color="green", label="Compra Stock2", alpha=0.8, s=80
    )
    axes[0].scatter(
        stock2.index[signals["short_stock2"]], 
        stock2[signals["short_stock2"]], 
        marker="v", color="red", label="Venta en corto Stock2", alpha=0.8, s=80
    )

    axes[0].set_title("Precios de las Acciones con Señales de Trading")
    axes[0].set_ylabel("Precio")
    axes[0].legend()
    axes[0].grid(True)

    
    z_score = signals["z_score"]
    axes[1].plot(z_score.index, z_score, label="Spread Normalizado", color="blue", linewidth=1.5)

   
    axes[1].axhline(y=threshold, color="orange", linestyle="--", label=f"±{threshold} sigma", linewidth=1.2)
    axes[1].axhline(y=-threshold, color="orange", linestyle="--", linewidth=1.2)
    axes[1].axhline(y=0, color="gray", linestyle="-", linewidth=1)

    axes[1].set_title("Spread Normalizado y Señales de Trading")
    axes[1].set_xlabel("Fecha")
    axes[1].set_ylabel("Z-score")
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()