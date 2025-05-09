import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend suitable for server environments

import matplotlib.pyplot as plt
import numpy as np
import os

def generate_trend_plot(city):
    months = np.arange(1, 13)
    trend = np.random.normal(loc=300, scale=50, size=12)

    plt.figure(figsize=(8, 4))
    plt.plot(months, trend, marker='o')
    plt.title(f'Energy Bill Trend in {city}')
    plt.xlabel('Month')
    plt.ylabel('Estimated Bill (INR)')
    plt.xticks(months)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('static/chart.png')
    plt.close()
