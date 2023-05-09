import pandas as pd
import plotly.express as px
#import plotly.graph_objs as go
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load data

df = pd.read_csv('http://www.my-cunymsds.com/data608/poverty3.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.DARKLY]

# Load the two CSV files
#df1 = pd.read_csv('data/poverty3.csv')
#df2 = pd.read_csv('data/poverty2.csv')

# Create app
app = dash.Dash(__name__ , external_stylesheets=external_stylesheets)
server = app.server
# Define layout
app.layout = html.Div([

    # Define tabs
    dcc.Tabs(id='tabs', value='tab-1', children=[

        # Define tab 0
        dcc.Tab(label='CSV Selector', value='tab-0', children=[
        html.Div([
            html.H2('Select a CSV File to load and use'),
            dcc.RadioItems(
                id='csv-selection',
                options=[
                    {'label': 'CSV 1 High Count Metrics ', 'value': 'http://www.my-cunymsds.com/data608/poverty3.csv'},
                    {'label': 'CSV 2 all (many low count metrics)', 'value': 'http://www.my-cunymsds.com/data608/poverty2.csv'}
                ],
                value='http://www.my-cunymsds.com/data608/poverty3.csv'
            ),
            html.Br(),
            html.Div([
                html.P('Instructions:'),
                html.P(
                    'Here you can change which data frame is used for visualizations.  There are two options.  One where I filtered all instances where a given metric has very few datapoints available. The other CSV has all data points included, even if there was only a single data point found.'),
                html.P(
                    'You can switch back and forth as needed. Just remember that if you use the full dataset, you may see a few hits in your plots, maybe even just one datapoint. If you use the filtered dataset, some datapoints were ommitted'),
            ]),
            html.Div(id='output-data'),
        ])]),

        # Define first tab
        dcc.Tab(label='World Map', value='tab-1', children=[

            # Define dropdown and slider for user input
            html.Div([
                html.H1('Poverty in the World by Metric through the Years'),
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[{'label': name, 'value': metric} for name, metric in
                             zip(df['Indicator Name'].unique(),df['Indicator Code'].unique())],
                    value=df['Indicator Code'].iloc[0]
                ),
                html.Br(),
                dcc.Slider(
                    id='year-slider',
                    min=df['year'].min(),
                    max=df['year'].max(),
                    marks={str(year): str(year)[-2:] for year in df['year'].unique()},
                    value=df['year'].iloc[0],
                    step=1
                )
            ]),

            # Define world map that updates based on user selections
            html.Div([
                dcc.Graph(id='world-map')
            ])
        ]),

        # Define second tab
        dcc.Tab(label='Line Plot 1', value='tab-2', children=[
            # Define dropdown for selecting metrics
            html.Div([
                html.H1('Poverty Metrics by Country'),
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': name, 'value': code} for name,
                    code in zip(df['Country Name'].unique(), df['Country Code'].unique())],
                    value=df['Country Code'].iloc[0]
                ),
                html.Br(),
                dcc.Dropdown(
                    id='metric-dropdown2',
                    options=[{'label': name, 'value': code} for name,
                    code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                    value=[],
                    multi=True
                ),
                html.Div(id='output')
            ])
        ]),

    # Define third tab
        dcc.Tab(label='Bar Chart', value='tab-3', children=[
            # Define dropdown for selecting metrics
            html.Div([
                html.H1('Metric Comparison of ALL Countries'),
                dcc.Dropdown(
                    id='metric2-dropdown',
                    options=[{'label': name, 'value': code} for name, code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                    value= None
                ),
                html.Br(),
                dcc.Slider(
                    id='year-slider2',
                    min=df['year'].min(),
                    max=df['year'].max(),
                    value=df['year'].min(),
                    marks={str(year): str(year)[-2:] for year in df['year'].unique()},
                    step=1
                ),
                dcc.Graph(id='bar-chart',style={'height': '1000px'})
            ],style={'overflowY': 'scroll', 'height': 1000})
        ]),

    # Define fourth tab
        dcc.Tab(label='Line Plot 2', value='tab-4', children=[
            # Define dropdown for selecting metrics
            html.Div([
                html.H1('Poverty Comparison of Countries'),
                dcc.Dropdown(
                    id='metric-dropdown4',
                    options=[{'label': name, 'value': code} for name,
                    code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                    value=df['Indicator Code'].iloc[0]
                ),
                html.Br(),
                dcc.Dropdown(
                    id='country-dropdown4',
                    options=[{'label': name, 'value': code} for name,
                    code in zip(df['Country Name'].unique(), df['Country Code'].unique())],
                    value=[],
                    multi=True
                ),
                html.Div(id='output4')
            ])
        ]),
    ])
])


# Define callbacks

# Define callback to load selected CSV into df
@app.callback(Output('output-data', 'children'),
              [Input('csv-selection', 'value')])

def update_df(csv_filename):
    global df
    df = pd.read_csv(csv_filename)
    return ''

@app.callback(
    Output('world-map', 'figure'),
    Input('metric-dropdown', 'value'),
    Input('year-slider', 'value'),
)
def update_world_map(metric, year):
    filtered_df = df[(df['Indicator Code'] == metric) & (df['year'] == year)]
    fig = px.choropleth(filtered_df, locations='Country Code', hover_name='Country Name',
                        color='value', range_color=[filtered_df['value'].min(), filtered_df['value'].max()],
                        title='{} ({})'.format(metric, year))
    return fig

@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('metric-dropdown2', 'value')]
)
def update_output(country_code, metric_codes):
    if country_code is None or len(metric_codes) == 0:
        return ''
    else:
        # Filter the data by country and selected metrics
        filtered_df = df[(df['Country Code'] == country_code) & (df['Indicator Code'].isin(metric_codes))]

        # Create line plots for each selected metric
        fig = px.line(filtered_df, x='year', y='value', color='Indicator Code', hover_name='Indicator Name')

        # Return the line plot
        return dcc.Graph(figure=fig)


# Define the callback function for the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('metric2-dropdown', 'value'),
     Input('year-slider2', 'value')]
)
def update_bar_chart(metric, year):
    # Filter the data based on the selected metric and year
    filtered_df = df[(df['Indicator Code'] == metric) & (df['year'] == year)]

    # Sort the data by value in descending order
    sorted_df = filtered_df.sort_values('value', ascending=False)

    # Create the bar chart
    fig = {
        'data': [{
            'x': sorted_df['value'],
            'y': sorted_df['Country Name'],
            'type': 'bar',
            'orientation': 'h',

        }],
        'layout': {
            'title': f'{metric} Values for {year}',
            'xaxis': {'title': 'Value'},
            'yaxis': {'title': 'Country'}
        }
    }

    return fig

@app.callback(
    dash.dependencies.Output('output4', 'children'),
    [dash.dependencies.Input('country-dropdown4', 'value'),
     dash.dependencies.Input('metric-dropdown4', 'value')]
)
def update_output2(country_codes, metric_code):
    if metric_code is None or len(country_codes) == 0:
        return ''
    else:
        # Filter the data by country and selected metrics
        filtered_df = df[(df['Indicator Code'] == metric_code) & (df['Country Code'].isin(country_codes))]

        # Create line plots for each selected metric
        fig = px.line(filtered_df, x='year', y='value', color='Country Code', hover_name='Country Name')

        # Return the line plot
        return dcc.Graph(figure=fig)


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
