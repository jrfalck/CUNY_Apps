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
# df1 = pd.read_csv('data/poverty3.csv')
# df2 = pd.read_csv('data/poverty2.csv')
# , external_stylesheets=external_stylesheets

# Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#5a5a5a dark gray
#7FDBFF pale blue
#d4d4d4 light gray

colors = {
    'background': '#111111',
    'text': '#7fdbff'
}

tabs_styles = {
    'height': '44px',
    'backgroundColor': 'black',
    'border-top-left-radius' : '15px',
    'border-top-right-radius' : '15px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#3d3d3d',
    'color' : colors['text'],
    'border-top-left-radius' : '15px',
    'border-top-right-radius' : '15px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'border-top-left-radius': '15px',
    'border-top-right-radius': '15px'

}

# Define layout
app.layout = html.Div(children=[

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
        ],style={
            'textAlign': 'left',
            'color': colors['text'], 'backgroundColor' : colors['background']
        })], style=tab_style, selected_style=tab_selected_style),

        # Define first tab
        dcc.Tab(label='World Map', value='tab-1', children=[
            html.Div([html.H1('Poverty in the World by Metric through the Years')],
                     style={'textAlign': 'center','color': colors['text']}),
            # Define dropdown and slider for user input
                html.Div([
                    dcc.Dropdown(
                        id='metric-dropdown',
                        options=[{'label': name, 'value': metric} for name, metric in
                                 zip(df['Indicator Name'].unique(),df['Indicator Code'].unique())],
                        value=df['Indicator Code'].iloc[0]
                    )], style={'display': 'inline-block', 'width': '30%'}),

                html.Div([
                    dcc.Slider(
                        id='year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        # marks={str(year): str(year)[-2:] for year in df['year'].unique()},
                        marks={str(df['year'].min()): str(df['year'].min()),
                               "1995": "1995",
                               str(df['year'].max()): str(df['year'].max())},
                        value=1995,
                        included=False,
                        step=1
                    )
                ], style={'display': 'inline-block', 'width': '60%'}),

                # Define world map that updates based on user selections
                html.Div([
                    dcc.Graph(id='world-map')
                ])
        ],style=tab_style, selected_style=tab_selected_style),

        # Define second tab
        dcc.Tab(label='Line Plot 1', value='tab-2', children=[
            # Define dropdown for selecting metrics
            html.Div([
                html.Div([
                    html.H1('Poverty Metrics by Country'),
                ],style={'color': colors['text']}),
                html.Div([
                    dcc.Dropdown(
                        id='country-dropdown',
                        options=[{'label': name, 'value': code} for name,
                        code in zip(df['Country Name'].unique(), df['Country Code'].unique())],
                        value=df['Country Code'].iloc[0]
                    ),
                ], style={'display': 'inline-block', 'width': '25%'}),
                html.Br(),
                html.Div([
                    dcc.Dropdown(
                        id='metric-dropdown2',
                        options=[{'label': name, 'value': code} for name,
                        code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                        value=[],
                        multi=True
                    ),
                ], style={'display': 'inline-block', 'width': '50%'}),
                html.Div(id='output')
            ])
        ],style=tab_style, selected_style=tab_selected_style),

    # Define third tab
        dcc.Tab(label='Bar Chart', value='tab-3', children=[
            # Define dropdown for selecting metrics
            html.Div([
                html.Div([
                    html.H1('Metric Comparison of ALL Countries'),
                ],style={'color': colors['text']}),
                html.Div([
                    dcc.Dropdown(
                        id='metric2-dropdown',
                        options=[{'label': name, 'value': code} for name, code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                        value= None
                    ),
                ], style={'display': 'inline-block', 'width': '30%'}),

                html.Div([
                    dcc.Slider(
                        id='year-slider2',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=1995,
                        marks={str(df['year'].min()): str(df['year'].min()),
                               "1995": "1995",
                               str(df['year'].max()): str(df['year'].max())},
                        step=1
                    ),
                ], style={'display': 'inline-block', 'width': '60%'}),

                dcc.Graph(id='bar-chart',style={'height': '1000px'})
            ],style={'overflowY': 'scroll', 'height': 1000})
        ],style=tab_style, selected_style=tab_selected_style),

    # Define fourth tab
        dcc.Tab(label='Line Plot 2', value='tab-4', children=[
            # Define dropdown for selecting metrics
            html.Div([
                html.Div([
                    html.H1('Poverty Comparison of Countries'),
                ],style={'color': colors['text']}),
                html.Div([
                    dcc.Dropdown(
                        id='metric-dropdown4',
                        options=[{'label': name, 'value': code} for name,
                        code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                        value=df['Indicator Code'].iloc[0]
                    ),
                ], style={'display': 'inline-block', 'width': '40%'}),

                html.Br(),
                html.Div([
                    dcc.Dropdown(
                        id='country-dropdown4',
                        options=[{'label': name, 'value': code} for name,
                        code in zip(df['Country Name'].unique(), df['Country Code'].unique())],
                        value=[],
                        multi=True
                    ),
                ], style={'display': 'inline-block', 'width': '40%'}),

                html.Div(id='output4')
            ])
        ],style=tab_style, selected_style=tab_selected_style),
    ], style=tabs_styles)
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

    # Colors added by JUAN
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
    )

    fig.update_layout(
         autosize=True,
    #    margin=dict(
    #        l=0,
    #        r=0,
    #        b=0,
    #        t=0,
    #        pad=4,
    #        autoexpand=True
    #    ),
        #width=800,
        height=600,
    )
    return fig

# Define Callback for Line Plot 1
@app.callback(
    dash.dependencies.Output('output', 'children'),
    [dash.dependencies.Input('country-dropdown', 'value'),
     dash.dependencies.Input('metric-dropdown2', 'value')]
)
def update_lineplot1(country_code, metric_codes):
    if country_code is None or len(metric_codes) == 0:
        return ''
    else:
        # Filter the data by country and selected metrics
        filtered_df = df[(df['Country Code'] == country_code) & (df['Indicator Code'].isin(metric_codes))]

        # Create line plots for each selected metric
        fig = px.line(filtered_df, x='year', y='value', color='Indicator Code', hover_name='Indicator Name')

        # Colors added by JUAN
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )

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
    sorted_df = filtered_df.sort_values('value', ascending=True)

    # Create the bar chart
    fig = px.bar(sorted_df, x='value', y='Country Name', orientation='h',
                 title=f'{metric} Values for {year}', text_auto=True)
    fig.update_layout(xaxis=dict(title='value',
                                 showline=False,
                                 showgrid=False),
                      yaxis=dict(title='Country',
                                 showline=False,
                                 showgrid=False),
                      plot_bgcolor=colors['background'],
                      font_color=colors['text'],
                      paper_bgcolor=colors['background'])

    return fig

@app.callback(
    dash.dependencies.Output('output4', 'children'),
    [dash.dependencies.Input('country-dropdown4', 'value'),
     dash.dependencies.Input('metric-dropdown4', 'value')]
)
def update_lineplot2(country_codes, metric_code):
    if metric_code is None or len(country_codes) == 0:
        return ''
    else:
        # Filter the data by country and selected metrics
        filtered_df = df[(df['Indicator Code'] == metric_code) & (df['Country Code'].isin(country_codes))]

        # Create line plots for each selected metric
        fig = px.line(filtered_df, x='year', y='value', color='Country Code', hover_name='Country Name')

        # Colors added by JUAN
        fig.update_layout(
            plot_bgcolor=colors['background'],
            paper_bgcolor=colors['background'],
            font_color=colors['text'],
        )

        # Return the line plot
        return dcc.Graph(figure=fig)


# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
