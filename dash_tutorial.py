import pandas as pd
import numpy as np
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
#import requests

import dash  # (version 1.12.0) pip install dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

gapminder = px.data.gapminder()

bgcolors = {
    'background': '#13263a',
    'text': '#FFFFFF'
}

#------------------------------

# external JavaScript files
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

# ------------------------------------------------------------------------------

# Import and clean data (importing csv into pandas)
df = pd.read_csv('bigmac.csv')
df.head(20)

df1 = df[['date','name','local_price','dollar_ex','dollar_price']]
df1.dtypes

date_unique = df1.date.nunique()
date_min = df1.date.min()
date_max = df1.date.max()
name_unique = df1.name.nunique()
dollar_price_min = df1.dollar_price.min()
dollar_price_max = df1.dollar_price.max()
print(f"date_unique: ", date_unique)
print(f"date_min: ", date_min)
print(f"date_max: ", date_max)
print(f"name_unique: ", name_unique)
print(f"dollar_price_min: ", dollar_price_min)
print(f"dollar_price_max ", dollar_price_max)

#create a list of countries where number of price
name = df1['name'].value_counts().reset_index()
name = name[name['name'] > 20][['index','name']]

#rename columns
name.columns = ['countries','count']

#create list out of countries
countries = list(name['countries'])

name.countries.nunique()

countries
colors = ['#0000ff', '#3300cc', '#660099', '#990066', '#cc0033', '#ff0000']

#that was way more difficult than it should have been
#just wanted to make sure there was the same number of countries in the list of countries that
#had more than 20 prices/dates that are in the dataframe
#there are
df2 = df1[df1['name'].isin(countries)]
df2.name.unique()
name_unique = df2.name.nunique()
countries_unique = name.countries.nunique()
print(f"name_unique: ", name_unique)
print(f"countries_unique: ", countries_unique)

#create an average price column
df2['average_price'] = df2[['dollar_price']].mean(axis=1)
print(df2.average_price.nunique())
print(df2.head())

#created a dataframe with just the averages of each column per country
df3 = df2.groupby('name').mean().reset_index()
print(df3.head())

print(df3.dtypes)
df3.columns = ['country','local_price','dollar_ex','dollar_price','average_price']
print(df3.head())

df4 = df3[['dollar_price','country']]
print(df4.head())

prices = list(df1.groupby('name').dollar_price.unique())
print(prices)

def get_df():
    return df3

#------------

#create plotly figures
#scatter plot
plot1 = px.scatter(df2,
        x="name",
        y="dollar_price",
        animation_frame="date", #this is right
        #animation_group="City", #this is right
        color="name",
        size="dollar_price",
        hover_data=['name'],
        #log_x=True,
        size_max=35,
        #range_x=[1,58]
        range_y=[0,10]
)

scatter1 = go.Scatter(x=list(df2.name)
                     ,y=list(df2.dollar_price)
                     ,name="Scatter"
                     ,showlegend=True
                     ,visible=True
                     ,mode='markers'
                     ,marker=dict(
                        size=16,
                        color=np.random.randn(500), #set color equal to a variable
                        colorscale='Viridis', # one of plotly colorscales
                        showscale=True
                      )                     #,size_max=35
                     #,size=df2.average_price
                     #,color=df2.name
                     #,line=dict(color="#f44242")
                     )

#line plot
title = "BigMac Price per Country per Year"
plot2 = px.line(
        df2,
        title=title,
        x="date",
        y="dollar_price",
        color="name",
        hover_name="name",
        line_shape="spline",
        render_mode="svg"
)
layout = dict(
        legend=dict(
            traceorder="normal",
            font=dict(
                family="sans-serif",
                size=12,
                color="black"
            ),
            bgcolor="LightSteelBlue",
            bordercolor="Black",
            borderwidth=1
        )
)

fig1 = go.Scatter(x=list(df3.country)
                 ,y=list(df3.dollar_price)
                 ,mode='markers'
                 ,name='countries'
                 )
                 #,name="df3_dollar_price")
#data = [fig1, fig2]
#return {"data": data,"layout": layout}

#----------------------
#build html banner


#-----------------------
#app layout div

app.layout = html.Div([
    html.Div([
        html.H1(children="This is a Dash Dashboard with Plotly Plots!"),
        #html.Img(src="/assets/stock-icon.png")
        ], className="sample-header",
           style = {
                'font-family': 'cursive',
                'font-size': '26px',
                'text-align': 'center'
            }),

    html.Br(),

    html.Div(['Simple Dash App']),

    html.Br(),
    html.Br(),

    html.H1("Pandas DataFrame inserted into a Dash DataTable"),

    #datatable div
    html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df3.columns],
            data=df3.to_dict('records'),
            style_cell={'fontSize':16, 'font-family':'sans-serif','colors':'black','backgroundColor':'darkgrey'}
        ),
    ], style={"height": "300px","width":"90%", "overflowY": "scroll", 'padding': 0,
              'backgroundColor':'black','fontWeight':'bold'}),

    html.Br(),
    html.Br(),

    # html.Div([
    #     generate_html_table()
    # ], className="3 columns", style={'padding': 50}),

    #input div
    html.H3("Filters:"),
    html.Div([
        dcc.Input(
            id="country-input",
            placeholder="Enter a Country",
            type="text",
            value=''
        ),
        html.Button(id="submit-button", n_clicks=0, children="Submit")
    ]),

    html.Br(),

    #dropdown div
    html.Div(
        dcc.Dropdown(
            options=[
                {'label': 'Candlestick', 'value': 'Candlestick'},
                {'label': 'Line', 'value': 'Line'},
                {'label': 'Bar', 'value': 'Bar'}
            ]
        ), style={"width": "35%"}
    ),

    html.Br(),
    html.Br(),

    html.H1("Two plots next to each other (two columns)?"),

    #add two graphs side by side
    html.Div([
        html.Div([
        html.H2("First Column"),
        dcc.Graph(
            id='fig0',
            figure={
                'data': [
                    dict(
                        x=df3[df3['country'] == i]['dollar_price'],
                        y=df3[df3['country'] == i]['average_price'],
                        text=df3[df3['country'] == i]['country'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 35,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df3.country.unique()
                ],
                'layout': dict(
                    xaxis={'type': 'log', 'title': 'BigMac Price per Country'},
                    yaxis={'title': 'Dollar Price'},
                    margin={'l': 0, 'b': 40, 't': 10, 'r': 0},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            },
            style={"width": "100%",
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto"
            },
        )
        ], className='six columns'),#, className="10 columns", style={'padding-left': '5%', 'padding-right': '1%', "width": "600px", 'plot_bgcolor': 'rgb(10,10,10)'}),

        # html.Br(),
        # html.Br(),
        # html.Br(),

        #style={"height": "300px", "overflowY": "scroll"},
        #style={"height": "100%"},
        html.Div([
        html.H2("Second Column"),
        dcc.Graph(
            id='fig2',
            figure={
                'data': [
                    dict(
                        x=df3[df3['country'] == i]['average_price'],
                        y=df3[df3['country'] == i]['dollar_price'],
                        text=df3[df3['country'] == i]['country'],
                        mode='markers',
                        opacity=0.7,
                        marker={
                            'size': 35,
                            'line': {'width': 0.5, 'color': 'white'}
                        },
                        name=i
                    ) for i in df3.country.unique()
                ],
                'layout': dict(
                    xaxis={'type': 'log', 'title': 'BigMac Price per Country'},
                    yaxis={'title': 'Average Price'},
                    margin={'l': 0, 'b': 40, 't': 10, 'r': 0},
                    legend={'x': 0, 'y': 1},
                    hovermode='closest'
                )
            },
            style={"width": "100%",
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto"
            }
        )
        ], className="six columns"),#, className="10 columns", style={'padding-left': '5%', 'padding-right': '1%', "width": "600px", 'plot_bgcolor': 'rgb(10,10,10)'}),
    # ] #, fig.update_layout(width=450, height=450, plot_bgcolor='rgb(10,10,10)')
    ], className="row", style={"width": "90%"}),

    html.Br(),

    #px plot
    html.Div([
        html.H1("Scatter Plot (Animated)"),
        dcc.Graph(
            id="animated1",
            style={"width": "100%",
            "display": "block",
            "margin-left": "auto",
            "margin-right": "auto"
            },
            figure = plot1
        )
    ], className="3 columns", style={"width": "80%", 'padding-right':'0%','padding': 10}),

    html.Br(),

    html.Div([
        html.Div([
            html.H1("line graph"),
            dcc.Graph(
                id="graph1",
                style={
                "width": "500px",
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto"
                },
                # style={"width": "100%", "display": "block"},
                figure = plot2
            )
        ]),# className="3 columns", style={'padding': 50}),

        html.Br(),

        html.Div([
            html.H1("weird scatter plot"),
            dcc.Graph(
                id="plotly_figure_1",
                style={
                "width": "500px",
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto"
                },
                figure={
                    "data":[scatter1],
                    "layout": {
                        "title": "plot 1 title"
                    }
                }
            )
        ]),# className="3 columns", style={'padding': 50}), #copy to each dcc.graph

        html.Br(),

        html.Div([
            html.H1("scatter-ish"),
            dcc.Graph(
                id="fig1",
                style={
                "width": "500px",
                "display": "block",
                "margin-left": "auto",
                "margin-right": "auto"
                },
                figure={
                    "data":[fig1],
                    "layout":{
                        "title": "plot 2 title"
                    }
                }
            )
        ]),# className="3 columns", style={'padding': 100})
    ], className="3 columns", style = {'columnCount': 3,"width":"80%"})

    #className="row"),

], style={
    #'backgroundColor': bgcolors['background'],
    #'background': 'black',
    'color': bgcolors['text'],
    #'height':'100vh',
    'width':'100%',
    'height':'100%',
    'top':'0px',
    'left':'0px',
    'padding': 50}
)#, style={'columnCount': 2})#, "height": "900px", "overflowY": "scroll"})


# app.css.append_css({
#     "external_url":"https://codepen.io/chriddyp/pen/bWLwgP.css"
# })

#-------------------------
#callback

# @app.callback(dash.dependencies.Output("fig0", "figure"),
#             (dash.dependencies.Input())
#               [dash.dependencies.Input("country-input", "value")]
#               )
@app.callback(Output('fig0','figure'),
             [Input("submit-button", "n_clicks")],
             [State("country-input", "value")]
             )

#have to have a function for the callback
def update_fig(n_clicks, input_value):
    df = pd.read_csv('bigmac.csv')

    df1 = df[['date','name','local_price','dollar_ex','dollar_price']]

    date_unique = df1.date.nunique()
    date_min = df1.date.min()
    date_max = df1.date.max()
    name_unique = df1.name.nunique()
    dollar_price_min = df1.dollar_price.min()
    dollar_price_max = df1.dollar_price.max()

    name = df1['name'].value_counts().reset_index()
    name = name[name['name'] > 20][['index','name']]

    name.columns = ['countries','count']

    countries = list(name['countries'])

    colors = ['#0000ff', '#3300cc', '#660099', '#990066', '#cc0033', '#ff0000']

    df2 = df1[df1['name'].isin(countries)]
    name_unique = df2.name.nunique()
    countries_unique = name.countries.nunique()

    df2['average_price'] = df2[['dollar_price']].mean(axis=1)

    df3 = df2.groupby('name').mean().reset_index()

    df3.columns = ['country','local_price','dollar_ex','dollar_price','average_price']

    df4 = df3[['dollar_price','country']]

    prices = list(df1.groupby('name').dollar_price.unique())

    data = []

    fig1 = go.Scatter(x=list(df3.country)
                     ,y=list(df3.dollar_price)
                     ,name="df3_dollar_price")
    data.append(fig1)

    layout = {"title": "Callback Graph"}

    return {
        "data": data,
        "layout": layout
    }

#-------------------------------------
#run it

if __name__ == '__main__':
    app.run_server(debug=True)
