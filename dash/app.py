import dash
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output
from dash import dcc
from dash import html, ctx
import dash_bootstrap_components as dbc
from dash.development.base_component import Component
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
from dash import dash_table
from pymongo import MongoClient

import dash_bootstrap_components as dbc

app = dash.Dash(__name__ , external_stylesheets=[dbc.themes.GRID,dbc.themes.BOOTSTRAP])
server = app.server

host = "my_mongo"
port = 27017
user = 'admin'
password = 'pass'


def find_flight_states(icao24):
    client = MongoClient(host=host, port=port, username=user, password=password)
    database = client['aircraft']
    position_collection = database["positions"]

    data = position_collection.find({"icao24": icao24}, {"icao24": 1, "long": 1, "lat": 1}).sort("time_position", -1)
    return list(data)


def get_all_flights_last_state():
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


states = pd.DataFrame(get_all_flights_last_state())
CountryOriginDropdown = [
    html.Div([
        dcc.Dropdown(
            id='country_origin_dropdown',
            placeholder="Select Origin Country",
            options=[
                {'label': i, 'value': i} for i in states.origin_country.unique()
            ],
            multi=True
        ),
    ],
        style={"width": "80%", 'margin-left': 0, },
    ),
]

ClearSelectionButton =   [html.Div([dbc.Button("Clear selection", color="primary", n_clicks=1, id="clear_selection_button")])]



app.layout = dbc.Container([
     dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Suivi du traffic aérien'),
                ], style={'textAlign': 'center', "color": "white"})

            ], className="border-0 bg-transparent"),
        ], width=12),],style={'margin-bottom': 20 , 'backgroundColor': '#1C4E80'}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([

                    dbc.Row(
                    [dbc.Col(
                        html.Div([
                                    dcc.Markdown("""
                                        Origin Country:
                                    """),                                   
                                ],style={'margin-left': "20%",'textAlign': 'center'}), md=3 ),
                    dbc.Col(CountryOriginDropdown, md=6),
                    
                    dbc.Col(ClearSelectionButton, md=3)
                     ])
                ],)

            ], style={'margin-bottom': 20, "backgroundColor": "#F1F1F1"}, #className="border-0 bg-transparent"
            ),
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id="map"),
                ])],style={ "backgroundColor": "#F1F1F1"} )

        ], width=7),

        dbc.Col([

                dbc.Card([
                dbc.CardBody([

                    dbc.Row([
                            html.Div([
                                    dcc.Markdown("""
                                        Flight information:
                                    """),                                   
                            ]),
                    ]),
                    dbc.Row([
                        dash_table.DataTable(
                                id = 'table',
                                style_cell={'textAlign': 'left'},
                                style_header = {'display': 'none'},
                        ),
                    ])
                ], style={'textAlign': 'center'})

            ], style={'margin-bottom': 30, "backgroundColor": "#F1F1F1"}, #className="border-0 bg-transparent" ,style={ "backgroundColor": "#F1F1F1"}
            ),
            ], width=5),

    ]),

    dcc.Interval(
                        id='interval-component',
                        interval=1000 * 45,  # in milliseconds
                        n_intervals=0
                    ) 
], style={'backgroundColor':'white'},fluid=True)

      

@app.callback(
    dash.dependencies.Output('table', 'data'),
    [dash.dependencies.Input('map', 'clickData'),
     dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('clear_selection_button', 'n_clicks')])
def updateTable(clic_data, interval, nb_clicks):
    states = pd.DataFrame(get_all_flights_last_state())

    dt_temp1 = states.loc[states['icao24'] == clic_data["points"][0]["text"]]
    dt_temp1 = dt_temp1.drop('_id', axis=1).drop_duplicates()
    dt_temp1 = dt_temp1.T.reset_index().T.reset_index(drop=True)

    if ctx.triggered_id == "clear_selection_button":
        return

    return dt_temp1.T.to_dict('records')


@app.callback(
    dash.dependencies.Output('map', 'figure'),
    [dash.dependencies.Input('country_origin_dropdown', 'value'),
     dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('map', 'clickData'),
     dash.dependencies.Input('clear_selection_button', 'n_clicks')
     ])
def display_map(country, interval, click_data, clear_button_data):
    trigger_id = ctx.triggered_id
    display_mode = 'markers'

    if trigger_id == 'map' and click_data is not None:
        icao24 = click_data["points"][0]["text"]
        data = find_flight_states(icao24)
        df_states = pd.DataFrame(data)
        display_mode = 'lines'
       
    elif trigger_id == 'country_origin_dropdown':
        df_states = pd.DataFrame(get_all_flights_last_state())
        df_states = df_states[df_states.origin_country.isin(country)]

    else:
        df_states = pd.DataFrame(get_all_flights_last_state())
       
    fig = go.Figure(data=go.Scattermapbox(
        lon=df_states['long'],
        lat=df_states['lat'],
        text=df_states['icao24'],
        mode=display_mode,
        line=dict(width=4),
    
    ), )
    
    fig.update_layout(
        height=600,
        margin=dict(l=0, r=0, t=0, b=0),
        #clickmode='event+select',
        #paper_bgcolor="#DCDCDC",
         mapbox = {
            'style': "stamen-terrain",
            "zoom" : 1
         }
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8050)




