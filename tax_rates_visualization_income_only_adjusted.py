import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Create the data
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

# Original data
data_original = {
    'Year': years,
    'Lowest Quintile': [0, -2, -4, -6, -8, -10, -10, -10],
    'Second Quintile': [1, 0, -1, -2, -3, -4, -4, -4],
    'Middle Quintile': [3, 3, 2, 2, 1, 1, 1, 1],
    'Fourth Quintile': [6, 6, 5, 5, 4, 4, 4, 4],
    'Highest Quintile': [18, 19, 19, 20, 20, 19, 19, 19],
    'Top 1%': [16.9, 18, 19, 22, 24, 25, 26, 26.1],
    'Top 0.1%': [20, 21, 22, 24, 26, 27, 27.5, 27.5]
}

# Calculate adjusted Highest Quintile (80-99th percentile)
# Formula: [20 × Rate(Top Quintile) - 1 × Rate(Top 1%)] ÷ 19
highest_quintile_adjusted = []
for i in range(len(years)):
    adjusted_rate = (20 * data_original['Highest Quintile'][i] - 1 * data_original['Top 1%'][i]) / 19
    highest_quintile_adjusted.append(round(adjusted_rate, 1))

# Create new data dictionary with adjusted highest quintile
data = data_original.copy()
data['Highest Quintile (80-99th percentile)'] = highest_quintile_adjusted
del data['Highest Quintile']  # Remove the original highest quintile

df = pd.DataFrame(data)

# Create the figure
fig = go.Figure()

# Add traces for each income group
colors = {
    'Top 0.1%': '#000000',      # Black
    'Top 1%': '#8c564b',        # Brown
    'Highest Quintile (80-99th percentile)': '#9467bd',  # Purple
    'Fourth Quintile': '#d62728',   # Red
    'Middle Quintile': '#ff7f0e',   # Orange
    'Second Quintile': '#2ca02c',   # Green
    'Lowest Quintile': '#1f77b4'    # Blue
}

# Order the columns by tax rate (descending)
first_year_rates = df.iloc[0].drop('Year')
ordered_columns = ['Year'] + list(first_year_rates.sort_values(ascending=False).index)
df = df[ordered_columns]

for column in df.columns[1:]:
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df[column],
        name=column,
        mode='lines+markers',
        line=dict(color=colors[column], width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{x}<br>" +
                     "Tax Rate: %{y:.1f}%<br>" +
                     "<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title={
        'text': "Effective Federal Income Tax Rates (AGI) Excluding Payroll and Corporate Taxes (1950-2022)<br><sub>Highest Quintile adjusted to exclude Top 1%</sub>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title="Year",
    yaxis_title="Effective Federal Income Tax Rate (%)",
    hovermode='x unified',
    template='plotly_white',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(l=80, r=30, t=120, b=50),  # Increased top margin for subtitle
    showlegend=True,
    yaxis=dict(
        range=[-15, 30],  # Adjusted range to show negative rates
        tickformat='.0f',
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
        y=20,
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
        y=15,
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
fig.write_html("tax_rates_visualization_income_only_adjusted.html")

print("Adjusted income-tax-only visualization has been created and saved as 'tax_rates_visualization_income_only_adjusted.html'") 