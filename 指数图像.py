
import numpy as np
import matplotlib.pyplot as plt

def generate_exponential_plot(base):
    x = np.linspace(-10, 10, 500)
    y = base ** x
    y = np.clip(y, -1e10, 1e10)

    plt.figure(figsize=(8, 6))
    plt.plot(x, y, label=f'{base}^x')
    plt.title(f'Exponential Function: {base}^x')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.8, linestyle='--')
    plt.axvline(0, color='black', linewidth=0.8, linestyle='--')
    plt.legend()
    plt.show()

base = float(input("Enter the base of the exponent: "))
generate_exponential_plot(base)
