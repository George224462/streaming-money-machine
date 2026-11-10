# ============================================================
# PROJECT: The Streaming Money Machine
# FILE: python/monte_carlo_simulation.py
# PURPOSE: Simulate 10,000 artist career trajectories over 1 year
# ============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set random seed for reproducible results
np.random.seed(42)

# --- 1. SIMULATION PARAMETERS ---
NUM_SIMULATIONS = 10000    # Simulate 10,000 independent artists
MONTHS = 12                # 1-year timeline
STREAM_PAYOUT = 0.004      # $0.004 per stream
PLATFORM_CUT = 0.15        # 15% distributor cut
ANNUAL_RENT = 18000        # $1,500/month * 12

# Starting monthly streams for an emerging artist (Mean: 20,000, Std Dev: 10,000)
INITIAL_STREAMS_MEAN = 20000
INITIAL_STREAMS_STD = 10000

# Monthly growth rate parameters (Average 5% monthly growth, 25% volatility)
MONTHLY_GROWTH_MEAN = 0.05
MONTHLY_GROWTH_STD = 0.25

# Cost parameters per artist
PROD_COST_PER_TRACK = 500
TRACKS_PER_YEAR = 4
MARKETING_COST = 1000
DISTRIBUTION_COST = 50
TOTAL_EXPENSES = (PROD_COST_PER_TRACK * TRACKS_PER_YEAR) + MARKETING_COST + DISTRIBUTION_COST

# --- 2. RUN MONTE CARLO SIMULATION ---
print(f"🚀 Running {NUM_SIMULATIONS:,} Monte Carlo Simulations...")

annual_net_profits = []
total_annual_streams = []

for i in range(NUM_SIMULATIONS):
    # Sample starting streams for this artist (cannot be negative)
    current_streams = max(1000, np.random.normal(INITIAL_STREAMS_MEAN, INITIAL_STREAMS_STD))
    year_streams = 0
    
    for month in range(MONTHS):
        # Apply random monthly growth rate with volatility
        growth_rate = np.random.normal(MONTHLY_GROWTH_MEAN, MONTHLY_GROWTH_STD)
        
        # 5% chance of a "Viral Spike" (3x to 5x streams in a month)
        if np.random.random() < 0.05:
            growth_rate += np.random.uniform(2.0, 5.0)
            
        current_streams = max(500, current_streams * (1 + growth_rate))
        year_streams += current_streams
        
    # Calculate financials for this simulated year
    gross_revenue = year_streams * STREAM_PAYOUT
    net_revenue = gross_revenue * (1 - PLATFORM_CUT)
    net_profit = net_revenue - TOTAL_EXPENSES
    
    annual_net_profits.append(net_profit)
    total_annual_streams.append(year_streams)

profits = np.array(annual_net_profits)

# --- 3. STATISTICAL SUMMARY ---
prob_profitable = (profits > 0).mean() * 100
prob_pays_rent = (profits >= ANNUAL_RENT).mean() * 100
median_profit = np.median(profits)
top_5_percent_profit = np.percentile(profits, 95)

print("\n" + "="*50)
print("📊 MONTE CARLO SIMULATION RESULTS (10,000 ARTISTS)")
print("="*50)
print(f"Probability of Making ANY Profit (> $0):    {prob_profitable:.2f}%")
print(f"Probability of Paying Full Rent (>= $18K):  {prob_pays_rent:.2f}%")
print(f"Median Annual Net Income:                   ${median_profit:,.2f}")
print(f"Top 5% Breakout Artist Net Income:          ${top_5_percent_profit:,.2f}")
print("="*50)

# --- 4. VISUALIZATION ---
plt.figure(figsize=(12, 6))
sns.set_theme(style="darkgrid")

# Histogram plot
ax = sns.histplot(profits, bins=100, kde=True, color="#1DB954", edgecolor="none") # Spotify Green

# Highlight Rent Threshold
plt.axvline(ANNUAL_RENT, color="red", linestyle="--", linewidth=2, label=f"Annual Rent Target (${ANNUAL_RENT:,})")
plt.axvline(0, color="orange", linestyle=":", linewidth=2, label="Break-Even ($0)")

plt.title("Monte Carlo Simulation: 10,000 Emerging Artists 1-Year Net Profit Distribution", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Annual Net Income ($ USD)", fontsize=12)
plt.ylabel("Number of Simulated Artists", fontsize=12)
plt.xlim(-5000, 50000) # Zoom into relevant range

plt.legend(fontsize=11)

# Annotate Probability
plt.text(20000, ax.get_ylim()[1] * 0.7, 
         f"🎯 Probability of Paying Rent:\n   {prob_pays_rent:.2f}%\n\n📈 Probability of Profit:\n   {prob_profitable:.2f}%", 
         bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="grey"),
         fontsize=11, fontweight="bold")

plt.tight_layout()

# Save plot to images folder
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, "..", "images")
os.makedirs(images_dir, exist_ok=True)
output_path = os.path.join(images_dir, "monte_carlo_results.png")

plt.savefig(output_path, dpi=300)
print(f"\n✅ Chart saved to: {output_path}")

plt.show()