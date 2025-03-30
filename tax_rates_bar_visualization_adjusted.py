import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Create the data for 10-year intervals
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

# Original data
data_original = {
    'Year': years,
    'Lowest Quintile': [5, 6, 7, 7, 5, 4, 3, 3],
    'Second Quintile': [8, 9, 10, 9, 7, 6.5, 5, 5],
    'Middle Quintile': [10, 11, 12, 11, 9, 8.5, 8, 8],
    'Fourth Quintile': [12, 13, 14, 13, 11, 10.5, 10, 10],
    'Highest Quintile': [20, 21, 22, 21, 19, 18.5, 18, 18],
    'Top 1%': [42, 38, 35, 34, 32, 30, 28, 26],
    'Top 0.1%': [50, 45, 40, 37, 35, 33, 31, 30]
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

# Define colors for each group
colors = {
    'Top 0.1%': '#000000',      # Black
    'Top 1%': '#8c564b',        # Brown
    'Highest Quintile (80-99th percentile)': '#9467bd',  # Purple
    'Fourth Quintile': '#d62728',   # Red
    'Middle Quintile': '#ff7f0e',   # Orange
    'Second Quintile': '#2ca02c',   # Green
    'Lowest Quintile': '#1f77b4'    # Blue
}

# Create the figure
fig = go.Figure()

# Order the columns by tax rate (descending)
first_year_rates = df.iloc[0].drop('Year')
ordered_columns = ['Year'] + list(first_year_rates.sort_values(ascending=False).index)
df = df[ordered_columns]

# Add bars for each group
for column in df.columns[1:]:  # Skip 'Year' column
    # Add bars
    fig.add_trace(go.Bar(
        name=column,
        x=df['Year'],
        y=df[column],
        marker_color=colors[column],
        opacity=0.7,  # Make bars slightly transparent
        hovertemplate="Year: %{x}<br>" +
                     "Group: " + column + "<br>" +
                     "Tax Rate: %{y:.1f}%<br>" +
                     "<extra></extra>"
    ))
    
    # Add trend lines
    fig.add_trace(go.Scatter(
        name=column + " (trend)",
        x=df['Year'],
        y=df[column],
        mode='lines',
        line=dict(color=colors[column], width=3),
        showlegend=False,  # Don't show separate legend entry for trend lines
        hoverinfo='skip'  # Don't show hover info for trend lines
    ))

# Update layout
fig.update_layout(
    title={
        'text': "Effective Federal Tax Rates by Income Group with Trends (1950-2020)<br><sub>Highest Quintile adjusted to exclude Top 1%</sub>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title="Year",
    yaxis_title="Effective Federal Tax Rate (%)",
    barmode='group',  # Grouped bar chart
    bargap=0.15,      # Gap between bars
    bargroupgap=0.1,  # Gap between bar groups
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
        range=[0, 55],  # Adjusted to show full range
        tickformat='.0f',
        gridcolor='lightgrey',
        gridwidth=1
    ),
    xaxis=dict(
        tickmode='array',
        ticktext=df['Year'].astype(str),
        tickvals=df['Year'],
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
        y=50,
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
        y=45,
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
fig.write_html("tax_rates_bar_visualization_adjusted.html")

print("Adjusted bar chart visualization has been created and saved as 'tax_rates_bar_visualization_adjusted.html'") 