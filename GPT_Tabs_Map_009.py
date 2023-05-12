import pandas as pd
import plotly.express as px
#import plotly.graph_objs as go
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load data

df = pd.read_csv('http://www.my-cunymsds.com/data608/poverty2.csv')
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.DARKLY]
external_stylesheets = [dbc.themes.BOOTSTRAP]


# Create app
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Falck Data608'
app.title = 'Falck Data608'
#5a5a5a dark gray
#7FDBFF pale blue
#7ec8e6
#d4d4d4 light gray
#111111 very darl almost black
#119DFF  Blue
#fafafa light light gray

sizedrop = 70

colors = {
    'background': '#000000',
    'text': '#7ec8e6'
}

tabs_styles = {
    'height': '44px',
    #'backgroundColor': 'black',
    'border-top-left-radius' : '15px',
    'border-top-right-radius' : '15px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#1d1d1d',
    'color' : colors['text'],
    'border-top-left-radius' : '15px',
    'border-top-right-radius' : '15px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#7FDBFF',
    'color': 'white',
    'padding': '6px',
    'border-top-left-radius': '15px',
    'border-top-right-radius': '15px'

}

tab0_content = html.Div([
                    html.H2('Select a CSV File to load and use'),
                    dcc.RadioItems(
                        id='csv-selection',
                        options=[
                            {'label': 'CSV 1 High Count Metrics ', 'value': 'http://www.my-cunymsds.com/data608/poverty3.csv'},
                            {'label': 'CSV 2 all (many low count metrics)', 'value': 'http://www.my-cunymsds.com/data608/poverty2.csv'}
                        ],
                        value='http://www.my-cunymsds.com/data608/poverty2.csv'
                    ),
                    html.Br(),
                    html.P('Instructions:'),
                    html.P('Here you can change which data frame is used for visualizations.  There are two options.  One where I filtered all instances where a given metric has very few datapoints available. The other CSV has all data points included, even if there was only a single data point found.'),
                    html.P('You can switch back and forth as needed. Just remember that if you use the full dataset, you may see a few hits in your plots, maybe even just one datapoint. If you use the filtered dataset, some datapoints were ommitted'),
                    html.Div(id='output-data')
], style={'textAlign': 'left','color': colors['text'], 'backgroundColor' : colors['background']})

controls_tab1 = dbc.Card(
    [
        dbc.Label("Select Poverty Metric"),
        html.Div(
            dcc.Dropdown(
                id='metric-dropdown1',
                options=[{'label': name[0:sizedrop], 'value': metric} for name, metric in
                         zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                value=df['Indicator Code'].iloc[0]
            ), style={'font-size':'12px'}
        ),
        html.Br(),
        dbc.Label("Select Year"),
        html.Div(
            dcc.Slider(
                id='year-slider1',
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
        )
    ],
    body=True,
)

tab1_content = dbc.Container(
    [
        dbc.Row(html.Div([html.H1('Poverty in the World by Metric through the Years')],
                        style={'textAlign': 'center', 'color': colors['text']})),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_tab1, md=3,style={"border-right-style":"solid","border-right-color":" dark gray" }),
                dbc.Col(dcc.Graph(id='world-map'), md=9),
            ]
            #align="center",
        )
    ],
    fluid=True
)

controls_tab2 = dbc.Card(
    [
        dbc.Label("Select Country"),
        html.Div(
            dcc.Dropdown(
                id='country-dropdown2',
                options=[{'label': name[0:sizedrop], 'value': code} for name,
                code in zip(df['Country Name'].unique(), df['Country Code'].unique())],
                value=df['Country Code'].iloc[0]
            ), style={'font-size':'12px'}
        ),
        html.Br(),
        dbc.Label("Select Poverty Metric"),
        html.Div(
            dcc.Dropdown(
                id='metric-dropdown2',
                options=[{'label': name[0:sizedrop], 'value': code} for name,
                code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                value=[],
                multi=True
            ), style={'font-size':'12px'}
        )
    ],
    body=True,
)

tab2_content = dbc.Container(
    [
        dbc.Row(html.Div([html.H1('Poverty Metrics by Country')],
                        style={'textAlign': 'center', 'color': colors['text']})),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_tab2, md=3,style={"border-right-style":"solid","border-right-color":" dark gray" }),
                dbc.Col(dcc.Graph(id='lineplot1'), md=9),
            ]
            #align="center",
        )
    ],
    fluid=True
)

controls_tab3 = dbc.Card(
    [
        dbc.Label("Select Poverty Metric"),
        html.Div(
            dcc.Dropdown(
                id='metric-dropdown3',
                options=[{'label': name[0:sizedrop], 'value': metric} for name, metric in
                         zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                value=df['Indicator Code'].iloc[0]
            ), style={'font-size':'12px'}
        ),
        html.Br(),
        dbc.Label("Select Year"),
        html.Div(
            dcc.Slider(
                id='year-slider3',
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
        )
    ],
    body=True,
)

tab3_content = dbc.Container(
    [
        dbc.Row(html.Div([html.H1('Poverty Metric Comparison - All Countires')],
                        style={'textAlign': 'center', 'color': colors['text']})),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_tab3, md=3,style={"border-right-style":"solid","border-right-color":" dark gray" }),
                dbc.Col(dcc.Graph(id='bar-chart',style={'height': '800px'}), md=9,style={"maxHeight": "400px", "overflow": "scroll"}),
            ]
            #align="center",
        )
    ],
    fluid=True
)

controls_tab4 = dbc.Card(
    [
        dbc.Label("Select Poverty Metric"),
        html.Div(
            dcc.Dropdown(
                id='metric-dropdown4',
                options=[{'label': name[0:sizedrop], 'value': code} for name,
                code in zip(df['Indicator Name'].unique(), df['Indicator Code'].unique())],
                value=df['Indicator Code'].iloc[0]
            ), style={'font-size':'12px'}
        ),
        html.Br(),
        dbc.Label("Select Countries"),
        html.Div(
            dcc.Dropdown(
                id='country-dropdown4',
                options=[{'label': name[0:sizedrop], 'value': code} for name,
                code in zip(df['Country Name'].unique(), df['Country Code'].unique())],
                value=[],
                multi=True
            ), style={'font-size':'12px'}
        )
    ],
    body=True,
)

tab4_content = dbc.Container(
    [
        dbc.Row(html.Div([html.H1('Country Comparison by Metric')],
                        style={'textAlign': 'center', 'color': colors['text']})),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls_tab4, md=3,style={"border-right-style":"solid","border-right-color":" dark gray" }),
                dbc.Col(dcc.Graph(id='lineplot2'), md=9),
            ]
            #align="center",
        )
    ],
    fluid=True
)


# Define layout
app.layout = html.Div([

    # Define tabs
    dcc.Tabs(id='tabs', value='tab-1',children=[

        # Define tab 0
        dcc.Tab(tab0_content, label='CSV Selector', value='tab-0',style=tab_style, selected_style=tab_selected_style),

        # Define first tab
        dcc.Tab(tab1_content, label='World Map', value='tab-1',style=tab_style, selected_style=tab_selected_style),

        # Define second tab
        dcc.Tab(tab2_content, label='Line Plot 1', value='tab-2',style=tab_style, selected_style=tab_selected_style),

        # Define third tab
        dcc.Tab(tab3_content, label='Bar Chart', value='tab-3',style=tab_style, selected_style=tab_selected_style),

        # Define fourth tab
        dcc.Tab(tab4_content, label='Line Plot 2', value='tab-4',style=tab_style, selected_style=tab_selected_style),

    ], style=tabs_styles)
    
],style={'padding': '20px 20px 20px 20px'})


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
    Input('metric-dropdown1', 'value'),
    Input('year-slider1', 'value'),
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
        #width=800,
        height=600,
    )
    return fig

# Define Callback for Line Plot 1
@app.callback(
    Output('lineplot1', 'figure'),
    [Input('country-dropdown2', 'value'),
    Input('metric-dropdown2', 'value')]
)
def update_lineplot1(country_code, metric_codes):
    # Filter the data by country and selected metrics
    filtered_df = df[(df['Country Code'] == country_code) & (df['Indicator Code'].isin(metric_codes))]

    # Create line plots for each selected metric
    fig = px.line(filtered_df, x='year', y='value', color='Indicator Code', hover_name='Indicator Name')

    # Colors added by JUAN
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False,showline=True),
    )
    # Return the line plot
    return fig


# Define the callback function for the bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('metric-dropdown3', 'value'),
     Input('year-slider3', 'value')]
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
    Output('lineplot2', 'figure'),
    [Input('metric-dropdown4', 'value'),
     Input('country-dropdown4', 'value')]
)
def update_lineplot2(metric_code,country_codes):
    # Filter the data by country and selected metrics
    filtered_df = df[(df['Indicator Code'] == metric_code) & (df['Country Code'].isin(country_codes))]

    # Create line plots for each selected metric
    fig = px.line(filtered_df, x='year', y='value', color='Country Code', hover_name='Country Name')

    # Colors added by JUAN
    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False, showline=True)
    )

    # Return the line plot
    return fig


# Run app
if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
