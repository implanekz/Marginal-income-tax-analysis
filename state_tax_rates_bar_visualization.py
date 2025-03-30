import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Create the data for 10-year intervals
years = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020]

# Original data (approximate state tax rates across income groups)
data_original = {
    'Year': years,
    'Lowest Quintile': [2, 3, 3.5, 4, 4.5, 4.8, 5, 5],
    'Second Quintile': [3, 3.5, 4, 4.5, 5, 5.2, 5.5, 5.5],
    'Middle Quintile': [3.5, 4, 4.5, 5, 5.5, 5.8, 6, 6],
    'Fourth Quintile': [4, 4.5, 5, 5.5, 6, 6.2, 6.5, 6.5],
    'Highest Quintile': [4.5, 5, 5.5, 6, 6.5, 6.8, 7, 7],
    'Top 1%': [5, 5.5, 6, 6.5, 7, 7.2, 7.5, 6.5],  # Note the recent decline due to tax competition
    'Top 0.1%': [5.2, 5.8, 6.2, 6.8, 7.2, 7.5, 7.8, 6.8]
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
    hover_prefix = ""
    if column == "Highest Quintile (80-99th percentile)":
        hover_prefix = "(Excluding Top 1%) "
        
    fig.add_trace(go.Bar(
        name=column,
        x=df['Year'],
        y=df[column],
        marker_color=colors[column],
        opacity=0.7,  # Make bars slightly transparent
        hovertemplate="Year: %{x}<br>" +
                     hover_prefix + "Tax Rate: %{y:.1f}%<br>" +
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
        'text': "State Effective Tax Rates by Income Group with Trends (1950-2020)<br><sub>Highest Quintile adjusted to exclude Top 1%</sub>",
        'y':0.95,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(size=24)
    },
    xaxis_title="Year",
    yaxis_title="Effective State Tax Rate (%)",
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
    margin=dict(l=80, r=30, t=120, b=50),
    showlegend=True,
    yaxis=dict(
        range=[0, 10],  # Adjusted range for state tax rates
        tickformat='.1f',
        gridcolor='lightgrey',
        gridwidth=1,
        dtick=1  # Set tick interval to 1%
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

# Add annotations for key state tax events
annotations = [
    dict(
        x=1978,
        y=8,
        text="Prop 13 in California",
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
        x=2010,
        y=7,
        text="State Tax Competition Era",
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
fig.write_html("state_tax_rates_bar_visualization.html")

print("State tax rates bar chart visualization has been created and saved as 'state_tax_rates_bar_visualization.html'") 