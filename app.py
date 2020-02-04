# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 17:43:39 2019

@author: Stephen Day
"""

import os
import flask
import pathlib
import statistics
from collections import OrderedDict
from statistics import mean

import pathlib as pl
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output, State

from src.dashboard import Dashboard

dashboard = Dashboard()
product_names = list(dashboard.product_names())

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(
    children=[
        html.Div(
            className="pkcalc-banner",
            children=[
                html.H2("Product Prediction"),
                html.A(
                    id="gh-link",
                    children=["View on GitHub"],
                    href="https://github.com/Kludex/display_product_ls",
                    style={"color": "white", "border": "solid 1px white"},
                ),
                html.Img(src=app.get_asset_url("GitHub-Mark-Light-64px.png")),
            ],
        ),
        html.Div(
            className="container",
            children=[
                html.Div(
                    html.Div(
                        className="row",
                        style={},
                        children=[
                            html.Div(
                                className="four columns pkcalc-settings",
                                children=[
                                    html.Label(
                                        [
                                            html.H4(["Options"])
                                        ]
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                [
                                                    html.Div(["Product"]),
                                                    dcc.Dropdown(
                                                        id='product',
                                                        options=[{
                                                            'label': name,
                                                            'value': name
                                                        } for name in product_names],
                                                        value=product_names[0]
                                                    ),
                                                ],
                                            ),
                                            html.Label(
                                                [
                                                    html.Div(["Scenario"]),
                                                    dcc.Dropdown(
                                                        id='scenario',
                                                        value=dashboard.scenarios_from(product_names[0])[0]
                                                    ),
                                                ]
                                            ),
                                            html.Label(
                                                [
                                                    html.Div(["Outliers"]),
                                                    dcc.Input(
                                                        id="outlier",
                                                        placeholder="Enter a value...",
                                                        type="number",
                                                        value=0,
                                                        min=0,
                                                        max=5,
                                                    ),
                                                ]
                                            ),
                                            html.Label(
                                                [
                                                    html.A(
                                                        html.Button('Download Excel', id='download-button'),
                                                        id='download-link',
                                                    ),
                                                ]
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                className="eight columns",
                                children=[
                                    html.Div(id='average-growth'),
                                    html.Div(
                                        children=[
                                            dcc.Graph(id="results-graph"),
                                        ],
                                    ),
                                ]
                            ),
                        ]
                    )
                )
            ]
        ),
    ],
)

@app.callback(
    [
        Output("results-graph", "figure"),
        Output("average-growth", "children"),
    ],
    [
        Input("product", "value"),
        Input("scenario", "value"),
        Input("outlier", "value"),
    ]
)
def update_output(product, scenario, outlier):
    data = dashboard.data_from(product, outlier)
    annual_growth = Dashboard.annual_growth_for(data[scenario])
    figure = {
        'data': [{
            'x': data.date,
            'y': data[scenario],
            'line': {'width': 3},
            'text': ['Annual growth:' + '{0:.0%}'.format(growth) for growth in annual_growth],
        }],
        'layout': {
            'margin': {'l': 50, 'r': 30, 'b': 30, 't': 30}
        }
    }
    children = html.H3('Average growth: ' + '{0:.0%}'.format(mean(annual_growth[:-12])))
    return figure, children

@app.callback(
    Output("scenario", "options"),
    [Input("product", "value")]
)
def update_scenarios(product):
    product_scenarios = dashboard.scenarios_from(product)
    return [{'label': scenario, 'value': scenario} for scenario in product_scenarios]

@app.callback(
    Output('download-link', 'href'),
    [
        Input('download-button', 'n_clicks'),
    ],
    [
        State('results-graph', 'figure'),
    ]
)
def update_download(n_clicks, figure):
    if n_clicks:
        dataframe = pd.DataFrame(
            {
                'date': figure['data'][0]['x'],
                'scenario': figure['data'][0]['y'],
            })
        root_dir = os.getcwd()
        absolute_filename = os.path.join(root_dir, 'download.xlsx')
        writer = pd.ExcelWriter(absolute_filename)
        dataframe.to_excel(writer, 'Scenario')
        writer.save()
    return '/download.xlsx'

@app.server.route('/download.xlsx')
def serve_static():
    root_dir = os.getcwd()
    return flask.send_from_directory(
        root_dir, 'download.xlsx'
    )

if __name__ == "__main__":
    app.run_server(debug=True)
