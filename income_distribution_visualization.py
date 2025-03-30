import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Create the data
years = np.arange(1950, 2026, 5)
data = {
    'Year': years,
    'Lowest Quintile': [15000, 18000, 22000, 25000, 28000, 30000, 32000, 35000, 38000, 40000, 42000, 45000, 48000, 50000, 52000, 55000],
    'Second Quintile': [25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000],
    'Middle Quintile': [35000, 42000, 50000, 58000, 65000, 72000, 80000, 88000, 95000, 100000, 105000, 110000, 115000, 120000, 125000, 130000],
    'Fourth Quintile': [45000, 55000, 65000, 75000, 85000, 95000, 105000, 115000, 125000, 135000, 145000, 155000, 165000, 175000, 185000, 195000],
    'Highest Quintile': [65000, 80000, 95000, 110000, 125000, 140000, 155000, 170000, 185000, 200000, 215000, 230000, 245000, 260000, 275000, 290000],
    'Top 1%': [150000, 200000, 250000, 300000, 350000, 400000, 450000, 500000, 550000, 600000, 650000, 700000, 750000, 800000, 850000, 900000],
    'Top 0.1%': [500000, 700000, 900000, 1100000, 1300000, 1500000, 1700000, 1900000, 2100000, 2300000, 2500000, 2700000, 2900000, 3100000, 3300000, 3500000]
}

df = pd.DataFrame(data)

# Reorder columns based on the first year's income (descending order)
first_year_income = df.iloc[0].drop('Year')
ordered_columns = ['Year'] + list(first_year_income.sort_values(ascending=False).index)
df = df[ordered_columns]

# Create the figure
fig = go.Figure()

# Add traces for each income group
colors = {
    'Top 0.1%': '#000000',  # Black
    'Top 1%': '#8c564b',    # Brown
    'Highest Quintile': '#9467bd',  # Purple
    'Fourth Quintile': '#d62728',  # Red
    'Middle Quintile': '#ff7f0e',  # Orange
    'Second Quintile': '#2ca02c',  # Green
    'Lowest Quintile': '#1f77b4'   # Blue
}

for column in df.columns[1:]:
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df[column],
        name=column,
        mode='lines+markers',
        line=dict(color=colors[column], width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{x}<br>" +
                     "Income: $%{y:,.0f}<br>" +
                     "<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title={
        'text': "Median Per Capita Income by Income Group (1950-2025)",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title="Year",
    yaxis_title="Median Per Capita Income ($)",
    hovermode='x unified',
    template='plotly_white',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(l=80, r=30, t=100, b=50),
    showlegend=True,
    yaxis=dict(
        tickformat='$,.0f',
        gridcolor='lightgrey',
        gridwidth=1
    ),
    xaxis=dict(
        gridcolor='lightgrey',
        gridwidth=1
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Add annotations for key events
annotations = [
    dict(
        x=1986,
        y=500000,
        text="Tax Reform Act of 1986",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=40,
        ay=-40,
        font=dict(size=12)
    ),
    dict(
        x=2017,
        y=400000,
        text="Tax Cuts and Jobs Act",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=-40,
        ay=40,
        font=dict(size=12)
    )
]

fig.update_layout(annotations=annotations)

# Save the figure as an HTML file
fig.write_html("income_distribution_visualization.html")

print("Visualization has been created and saved as 'income_distribution_visualization.html'") 