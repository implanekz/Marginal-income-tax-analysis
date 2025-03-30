import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Create the data
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

# Calculate adjusted Top 20% (80-99th percentile)
# Formula: [20 × Income(Top Quintile) - 1 × Income(Top 1%)] ÷ 19
top_20_adjusted = []
for i in range(len(years)):
    adjusted_income = (20 * 85 - 1 * 250) / 19  # 1950
    if i == 0:
        adjusted_income = (20 * 85 - 1 * 250) / 19
    elif i == 1:
        adjusted_income = (20 * 102 - 1 * 300) / 19
    elif i == 2:
        adjusted_income = (20 * 122 - 1 * 360) / 19
    elif i == 3:
        adjusted_income = (20 * 135 - 1 * 400) / 19
    elif i == 4:
        adjusted_income = (20 * 150 - 1 * 450) / 19
    elif i == 5:
        adjusted_income = (20 * 170 - 1 * 520) / 19
    elif i == 6:
        adjusted_income = (20 * 180 - 1 * 550) / 19
    else:  # 2020
        adjusted_income = (20 * 185 - 1 * 580) / 19
    top_20_adjusted.append(round(adjusted_income, 1))

# Income per capita data (in 2022 dollars, thousands)
data = {
    'Year': years,
    'Bottom 20%': [10, 12, 15, 17, 18, 20, 21, 22],
    'Second 20%': [20, 24, 28, 32, 35, 38, 40, 42],
    'Middle 20%': [32, 38, 45, 50, 54, 58, 60, 62],
    'Fourth 20%': [45, 54, 65, 72, 78, 85, 88, 90],
    'Top 20% (80-99th percentile)': top_20_adjusted,
    'Top 1%': [250, 300, 360, 400, 450, 520, 550, 580],
    'Top 0.1%': [500, 600, 720, 800, 900, 1040, 1100, 1160]
}

df = pd.DataFrame(data)

# Create the figure
fig = go.Figure()

# Define colors for each group
colors = {
    'Top 0.1%': '#000000',      # Black
    'Top 1%': '#8c564b',        # Brown
    'Top 20% (80-99th percentile)': '#9467bd',  # Purple
    'Fourth 20%': '#d62728',    # Red
    'Middle 20%': '#ff7f0e',    # Orange
    'Second 20%': '#2ca02c',    # Green
    'Bottom 20%': '#1f77b4'     # Blue
}

# Order the columns by income (descending)
first_year_income = df.iloc[0].drop('Year')
ordered_columns = ['Year'] + list(first_year_income.sort_values(ascending=False).index)
df = df[ordered_columns]

# Add traces for each income group
for column in df.columns[1:]:
    hover_prefix = ""
    if column == "Top 20% (80-99th percentile)":
        hover_prefix = "(Excluding Top 1%) "
    
    fig.add_trace(go.Scatter(
        x=df['Year'],
        y=df[column],
        name=column,
        mode='lines+markers',
        line=dict(color=colors[column], width=2),
        marker=dict(size=6),
        hovertemplate="Year: %{x}<br>" +
                     hover_prefix + "Income: $%{y:,.0f}k<br>" +
                     "<extra></extra>"
    ))

# Update layout
fig.update_layout(
    title={
        'text': "Real Income Per Capita by Income Group (1950-2020)<br><sub>In 2022 Dollars (Thousands) - Highest Quintile Adjusted to Exclude Top 1%</sub>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title="Year",
    yaxis_title="Income (Thousands of 2022 Dollars)",
    hovermode='x unified',
    template='plotly_white',
    legend=dict(
        yanchor="top",
        y=0.99,
        xanchor="left",
        x=0.01,
        bgcolor='rgba(255, 255, 255, 0.8)'
    ),
    margin=dict(l=80, r=30, t=120, b=50),
    showlegend=True,
    yaxis=dict(
        type='linear',  # Changed to linear scale
        tickformat='$,.0f',
        gridcolor='lightgrey',
        gridwidth=1,
        range=[0, 1200],  # Set fixed range to show full data
        dtick=200  # Set tick interval to 200k
    ),
    xaxis=dict(
        gridcolor='lightgrey',
        gridwidth=1,
        dtick=10  # Set tick interval to 10 years
    ),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# Update annotations positions for better visibility with linear scale
annotations = [
    dict(
        x=1980,
        y=900,
        text="Reagan Era Begins",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=40,
        ay=40,
        font=dict(size=12)
    ),
    dict(
        x=2000,
        y=600,
        text="Dot-com Peak",
        showarrow=True,
        arrowhead=1,
        arrowsize=1,
        arrowwidth=2,
        arrowcolor="#636363",
        ax=-40,
        ay=-40,
        font=dict(size=12)
    )
]

fig.update_layout(annotations=annotations)

# Save the figure as an HTML file
fig.write_html("income_per_capita_visualization.html")

print("Income per capita visualization has been created and saved as 'income_per_capita_visualization.html'") 