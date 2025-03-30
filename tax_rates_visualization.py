import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Create the data
years = np.arange(1950, 2026, 5)
data = {
    'Year': years,
    'Lowest Quintile': [5, 6, 6, 7, 7.5, 7, 6, 5, 4, 3.5, 3, 3, 3, 3, 3, 3],
    'Second Quintile': [8, 8.5, 9, 10, 9.5, 9, 8, 7, 6.5, 6, 5, 5, 5, 5, 5, 5],
    'Middle Quintile': [10, 10.5, 11, 12, 11.5, 11, 10, 9, 8.5, 8, 8, 8, 8, 8, 8, 8],
    'Fourth Quintile': [12, 12.5, 13, 14, 13.5, 13, 12, 11, 10.5, 10, 10, 10, 10, 10, 10, 10],
    'Highest Quintile': [20, 20.5, 21, 22, 21.5, 21, 20, 19, 18.5, 18, 18, 18, 18, 18, 18, 18],
    'Top 1%': [42, 40, 38, 35, 35, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 26],
    'Top 0.1%': [50, 48, 45, 40, 40, 38, 37, 36, 35, 34, 33, 32, 31, 30, 30, 30]
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
                     "Tax Rate: %{y:.1f}%<br>" +
                     "<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title={
        'text': "Effective Federal Tax Rates in the U.S. (1950-2025)",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title="Year",
    yaxis_title="Effective Federal Tax Rate (%)",
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
        range=[0, 60],
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
        y=35,
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
        y=25,
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
fig.write_html("tax_rates_visualization.html")

print("Visualization has been created and saved as 'tax_rates_visualization.html'") 