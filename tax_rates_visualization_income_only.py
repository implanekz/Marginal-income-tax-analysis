import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Create the data
years = [1950, 1975, 2000, 2022]
data = {
    'Year': years,
    'Lowest Quintile': [0, 0, -6, -10],
    'Second Quintile': [1, 1, -3, -4],
    'Middle Quintile': [3, 3, 2, 1],
    'Top 1%': [16.9, 20, 25, 26.1],
    'Top 0.1%': [20, 23, 27, 27.5]
}

df = pd.DataFrame(data)

# Reorder columns based on the first year's tax rates (descending order)
first_year_rates = df.iloc[0].drop('Year')
ordered_columns = ['Year'] + list(first_year_rates.sort_values(ascending=False).index)
df = df[ordered_columns]

# Create the figure
fig = go.Figure()

# Add traces for each income group
colors = {
    'Top 0.1%': '#000000',  # Black
    'Top 1%': '#8c564b',    # Brown
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
                     "Tax Rate: %{y:.1f}%<br>" +
                     "<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title={
        'text': "Effective Federal Income Tax Rates in the U.S. (1950-2022)",
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
    margin=dict(l=80, r=30, t=100, b=50),
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
fig.write_html("tax_rates_visualization_income_only.html")

print("Visualization has been created and saved as 'tax_rates_visualization_income_only.html'") 