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

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.title = 'ERI Research Map'

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
                            """Filter documents in the map by researcher or by years."""
                        ),
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        dcc.Dropdown(id="pi-selector",
                                            placeholder="Select an ERI researcher", 
                                            options=[{"label": i, "value": i} for i in list_of_pis],
                                            multi=False,
                                            #value="Adrian Stier",
                                            className='pi-selector')
                                    ], 
                                    style={'color': '#1E1E1E'}
                                ),  
                            ],
                        ),
                        dcc.Markdown(
                            children=[
                                "**About:** This t-SNE map was created from a NMF topic model of 3,770 ERI research publications and active projects from 2001 - 2019. Dashboard data and code are available on [Github](https://github.com/saralafia/ERI-dashboard)."
                            ]
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id='graphs', 
                            config={'displayModeBar': True}, 
                            #responsive=True,
                            #animate=True,
                            ),
                        dcc.RangeSlider(
                            id='year--slider',
                            min=df['year'].min(),
                            max=df['year'].max(),
                            value=[2009, 2019],
                            #value=df['year'].max(),
                            allowCross=False,
                            marks={str(year): str(year) for year in df['year'].unique()}, 
                            step=None, 
                            ),
                    ]
                )
            ]
        )
    ])

@app.callback(
    Output('graphs','figure'),
    [Input('pi-selector', 'value'), Input('year--slider', 'value')])

def update_graph(selected_pi, year_value):
    #dff = df[df['year'] == year_value]
    dff = df[(df['year']>year_value[0])&(df['year']<year_value[1])]
    if not selected_pi:
        fig = px.scatter(dff, 
                    x='x', 
                    y='y',
                    color='main_label',
                    hover_name='title', 
                    hover_data=['authors','doi','year','type','main_keys'], 
                    color_discrete_sequence=px.colors.qualitative.D3, 
                    opacity=0.6,
                    )

        fig.update_layout(
                       {'autosize': True, 
                       'plot_bgcolor': 'rgba(0, 0, 0, 0)',
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
                        )

        return fig
    
    else:
        fig = px.scatter(dff, 
                    x='x', 
                    y='y',
                    color='main_label',
                    hover_name='title', 
                    hover_data=['authors','doi','year','type','main_keys'], 
                    color_discrete_sequence=px.colors.qualitative.D3, 
                    opacity=0.2, 
                    )

        fig.update_layout(
                       {'autosize': True,
                       'plot_bgcolor': 'rgba(0, 0, 0, 0)',
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
                        )

        filtered_df = dff[dff.Name == selected_pi]
        
        fig.add_trace(go.Scatter(
                    x=filtered_df['x'], 
                    y=filtered_df['y'], 
                    #name='title',
                    text=filtered_df['title'],
                    mode='markers', 
                    #marker_symbol='x',
                    marker=dict(
                        color='whitesmoke',
                        #size=11,
                        opacity=0.9,
                        line=dict(
                            color='White',
                            width=2)
                        ),
                    hoverinfo='none', 
                    hovertemplate= 
                    "<b>Title: %{text}</b><br><br>" +
                    "<extra></extra>",
                    showlegend=False))
        
        return fig

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)
