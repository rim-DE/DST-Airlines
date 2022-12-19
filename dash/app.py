import pprint

import dash
from dash import html
import pandas as pd
from dash import dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from pymongo import MongoClient
import fontawesome as fa


app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.SKETCHY],
)

server = app.server

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H6('DST Tracker'),
                    html.Div(id='none', children=[], style={'display': 'none'})
                ], style={'textAlign': 'center'})

            ]),
        ], width=12),

        dbc.Col([
            dbc.Card([
                dcc.Graph(id="ploting", figure={}),

            ]),
        ], width=10),
        dbc.Col([

        ], width=1),

    ], className='mb-2'),

    dcc.Interval(
        id='interval-component',
        interval=1000 * 45,  # in milliseconds
        n_intervals=0
    )

], fluid=True)


# ------------------

@app.callback(
    Output('ploting', 'figure'),
    [Input('interval-component', 'n_intervals', )]
)
def plot_map(noned):
    states = pd.DataFrame(get_data_from_database())
    if states.size == 0:
        return

    fig = px.scatter_mapbox(states, lat="lat", lon="long", hover_name="origin_country", zoom=2, height=1000)
    fig.update_layout(mapbox_style="open-street-map", margin={"r": 0, "t": 0, "l": 0, "b": 0})

    # fig.update_traces(marker=dict(symbol=fa.icons['arrow-up'], size=1000, color='red', opacity=0.5))

    return fig


def get_data_from_database():
    host = "my_mongo"
    port = 27017
    user = 'admin'
    password = 'pass'

    client = MongoClient(host=host, port=port, username=user, password=password)

    database = client['aircraft']
    position_collection = database["positions"]

    last_extraction = position_collection.find().sort("extract_date", -1).limit(1)
    last_extraction = list(last_extraction)
    if len(last_extraction) == 0:
        return last_extraction
    else:
        data = list(position_collection.find({
            "extract_date": last_extraction[0]["extract_date"],
            "on_ground (T/F)": False
        }))

    return data


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
