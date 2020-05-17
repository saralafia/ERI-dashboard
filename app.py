import os
import pandas as pd
import numpy as np
import plotly.express as px
import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
from dash.dependencies import Input, Output

df = pd.read_csv('data.csv', index_col=0)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

list_of_pis = df['Name'].unique().tolist()
list_of_pis.sort()

app.layout = html.Div(children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(className="logo", src=app.get_asset_url("ERI_logo_WEB_72dpi_1.png")),
                        html.H2("ERI Research Map"),
                        html.P(
                            """Filter documents in the map by researcher or year. See the topic mixture of a document in the bar chart."""
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Dropdown(id="pi-selector",
                                            placeholder="Select a PI", 
                                            options=[{"label": i, "value": i} for i in list_of_pis],
                                            multi=False,
                                            #value=[df['Name'].sort_values()[0]],
                                            #style={'backgroundColor': '#1E1E1E'},
                                            className='pi-selector')
                                    ], 
                                    style={'color': '#1E1E1E'}
                                ),  
                            ],
                        ),
                        dcc.Markdown(
                            children=[
                                "**About:** This t-SNE map was created from a NMF topic model of 3,770 ERI research publications and funded projects from 2009 - 2019. Dashboard data and code are available on [Github](https://github.com/saralafia/ERI-dashboard)."
                            ]
                        ),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(id="map-graph", 
                            #config={'displayModeBar': True}, 
                            #animate=True,
                            figure = px.scatter(df, 
                                x='x', 
                                y='y',
                                color='main_label',
                                hover_name='title', 
                                hover_data=['authors','doi','year','type','main_keys'], 
                                color_discrete_sequence=px.colors.qualitative.D3, 
                                opacity=0.6, 
                                template='plotly_white').update_layout(
                                   {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)', 
                                    'xaxis_showgrid': False, 
                                    'yaxis_showgrid': False, 
                                    'xaxis_zeroline': False, 
                                    'yaxis_zeroline': False, 
                                    'yaxis_visible': False, 
                                    'xaxis_visible': False, 
                                    'font':{'family':"sans-serif", 'size':14, 'color':'white'},
                                    'legend': {'title':'Main Topic','itemsizing': 'constant'}, 
                                    'legend_font': {'family':"sans-serif", 'size':14, 'color':'white'},
                                    }
                                    )),
                    html.Div(
                        className="text-padding"),
                    dcc.RangeSlider(id='year-slider',
                        min=df['year'].min(),
                        max=df['year'].max(),
                        value=[2014, 2019],
                        marks={str(year): str(year) for year in df['year'].unique()}, 
                        step=None
                        ),
                    ]
                )
            ]
        )
    ])

# @app.callback(
#     Output('map-graph', 'figure'),
#     [Input('pi-selector', 'value')])

# def update_figure(selected_pi):
#     filtered_df = df[df.Name == selected_pi]
#     traces = []
#     for i in filtered_df.main_label.unique():
#         df_by_topic = filtered_df[filtered_df['main_label'] == i]
#         traces.append(dict(
#             x=df_by_topic['x'],
#             y=df_by_topic['y'],
#             text=df_by_topic['title'],
#             color=df_by_topic['main_label'], 
#             # hover_name='title', 
#             # hover_data=['authors','doi','year','type','main_keys'], 
#             color_discrete_sequence=px.colors.qualitative.D3,
#             mode='markers',
#             opacity=0.7,
#             marker={
#                 'size': 10,
#                 'line': {'width': 0, 'color': 'white'}
#             },
#             name=i
#         ))

#     return {
#         'data': traces,
#         'layout': dict(
#             xaxis={'range':[-150, 150],'showgrid': False,'zeroline': False,'visible': False,},
#             yaxis={'range': [-150, 150],'showgrid': False,'zeroline': False,'visible': False,},
#             # margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
#             # xaxis_showgrid=False, 
#             # yaxis_showgrid=False, 
#             # xaxis_zeroline=False, 
#             # yaxis_zeroline=False, 
#             # yaxis_visible=False, 
#             # xaxis_visible=False,
#             # legend={'x': 0, 'y': 1},
#             hovermode='closest',
#             transition = {'duration': 500},
#         )
#     }

if __name__ == '__main__':
    app.run_server(debug=True)
