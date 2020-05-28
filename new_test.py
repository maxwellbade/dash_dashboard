import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

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

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    #html.H1("Web Application Dashboards with Dash", style={'text-align': 'center'}),

    # dcc.Dropdown(id="slct_year",
    #              options=[
    #                  {"label": "2015", "value": 2015},
    #                  {"label": "2016", "value": 2016},
    #                  {"label": "2017", "value": 2017},
    #                  {"label": "2018", "value": 2018}],
    #              multi=False,
    #              value=2015,
    #              style={'width': "40%"}
    #              ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    #dcc.Graph(id='my_bee_map', figure={}),
    #dcc.Graph(id='my_bee_map', figure={}),

    html.Div([
        html.Div([
            dcc.Graph(id="bigmac1",figure='fig1')
        ], className="six columns"),
    html.Div([
        html.Div([
            dcc.Graph(id="bigmac2",figure='fig2')
        ], className="six columns")

        # html.Div([
        #     html.H3("Market News"),
        #     #generate_html_table()
        # ], className="six columns"),

    ],className="row")
    ])
])

# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='bigmac1', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
#def update_graph(self):
    # print(option_slctd)
    # print(type(option_slctd))

#container = "The year chosen by user was: {}".format(option_slctd)

    # dff = df.copy()
    # dff = dff[dff["Year"] == option_slctd]
    # dff = dff[dff["Affected by"] == "Varroa_mites"]
    #
    # # Plotly Express
    # fig = px.choropleth(
    #     data_frame=dff,
    #     locationmode='USA-states',
    #     locations='state_code',
    #     scope="usa",
    #     color='Pct of Colonies Impacted',
    #     hover_data=['State', 'Pct of Colonies Impacted'],
    #     color_continuous_scale=px.colors.sequential.YlOrRd,
    #     labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
    #     template='plotly_dark'
    # )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

#scatter plot
fig1 = px.scatter(df2,
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

#line plot
title = "BigMac Price per Country per Year"
fig2 = px.line(
        df2,
        title=title,
        x="date",
        y="dollar_price",
        color="name",
        hover_name="name",
        line_shape="spline",
        render_mode="svg"
)
fig2.update_layout(
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

#return container, fig1, fig2

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
