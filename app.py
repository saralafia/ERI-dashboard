import os
import json
import pandas as pd
import numpy as np
import colorcet as cc
import plotly.express as px
import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
from dash.dependencies import Input, Output

coarse = pd.read_csv('data-tsne-9.csv', index_col=0)
fine = pd.read_csv('data-tsne-36.csv', index_col=0)
coarse_umap = pd.read_csv('data-umap-9.csv', index_col=0)
fine_umap = pd.read_csv('data-umap-36.csv', index_col=0)

all_options = {'coarse (t-SNE)': coarse, 'coarse (UMAP)': coarse_umap, 'fine (t-SNE)': fine, 'fine (UMAP)': fine_umap}

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.title = 'ERI Research Maps'

server = app.server

list_of_pis = coarse['Name'].unique().tolist()
list_of_pis.sort()

list_of_depts = coarse['PI_primary_dept'].unique().tolist()
list_of_depts.sort()

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div(children=[
        html.Div(
            className="row",
            children=[
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.Img(className="logo", src=app.get_asset_url("ERI_logo_WEB_72dpi_1.png")),
                        html.H4(className='what-is', children='Earth Research Institute Maps'),
                        html.Div(id='control-tabs', className='control-tabs', children=[
                                dcc.Tabs(id='tabs', value='what-is', children=[
                                    dcc.Tab(
                                        label='About',
                                        value='what-is',
                                        children=html.Div(className='control-tab', children=[
                                            html.Div(
                                                className="text-padding",
                                                children=[],
                                                ),
                                            html.P('These maps show neighborhoods of topically similar research documents from the Earth Research Institute (ERI) at UC Santa Barbara. The 3,770 research documents (publications and projects) are associated with ERI researchers from 2001 - 2019. Each point in the map is a document color-coded by its main topic. Each document is assigned a mixture of topics from a non-negative matrix factorization (NMF) topic model and is embedded using t-distributed stochastic neighbor embedding (t-SNE) or uniform manifold approximation and projection (UMAP).'),
                                            html.P('Change the level of detail and embedding method for documents with the radio buttons on top of the map. Filter documents in the map by date range with the slider at the bottom of the map. Isolate a topic by double-clicking it in the map legend. In the "Search" tab, highlight documents in the map by affiliated researcher or academic department.'),
                                            dcc.Markdown("""Dashboard data and code are available on [Github](https://github.com/saralafia/ERI-dashboard).""")
                                        ])
                                    ),
                                    dcc.Tab(
                                        label='Search',
                                        value='search',
                                        children=html.Div(className='control-tab', children=[
                                            html.Div(className="div-for-dropdown",
                                                children=[
                                                    dcc.Dropdown(id="pi-selector",
                                                        placeholder="ERI researcher", 
                                                        options=[{"label": i, "value": i} for i in list_of_pis],
                                                        multi=False,
                                                        className='pi-selector')
                                                ]
                                            ), 
                                            html.Div(className='div-for-dropdown',
                                                children=[
                                                    dcc.Dropdown(id="dept-selector",
                                                        placeholder="Academic department", 
                                                        options=[{"label": i, "value": i} for i in list_of_depts],
                                                        multi=False,
                                                        className='dept-selector')
                                                ]
                                            ),
                                            html.Pre(id='click-data', 
                                                style=styles['pre']),
                                        ])
                                    )
                                ])
                            ]),
                    ]),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        html.Div(
                            className="text-padding",
                            children=[
                                "Change the map (by topical granularity and document embedding method)"
                            ],
                        ),
                        dcc.RadioItems(
                            id='granularity-options',
                            options=[{'label': i, 'value': i} for i in all_options.keys()],
                            value='coarse (t-SNE)',
                            labelStyle={'display': 'inline-block', 'verticalAlign': 'top', 'width': '20%'}
                            ),
                        dcc.Graph(
                            id='graphs', 
                            config={'displayModeBar': True}, 
                            responsive=True,
                            #style={"height" : '80vh', "width" : "100%"},
                            style={"height" : "80%", "width" : "100%"},
                            ),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Change the map (by document start and end year)"
                            ],
                        ),
                        html.Div(
                            className="div-for-slider", 
                            children=[
                                dcc.RangeSlider(
                                    id='year--slider',
                                    min=coarse['year'].min(),
                                    max=coarse['year'].max(),
                                    value=[2009, 2019],
                                    allowCross=False,marks={str(year): str(year) for year in coarse['year'].unique()}, 
                                    step=None, 
                                    className='year--slider',
                                    ),
                                ]
                            ),

                    ]
                )]
        )
    ])

@app.callback(
    Output('graphs','figure'),
    [Input('pi-selector', 'value'), Input('dept-selector', 'value'), Input('year--slider', 'value'), Input('granularity-options', 'value')])

def update_graph(selected_pi, selected_dept, year_value, granularity_value):
    
    selected = all_options[granularity_value]
    dff = selected[(selected['year']>year_value[0])&(selected['year']<year_value[1])]
    #dff = df[(df['year']>year_value[0])&(df['year']<year_value[1])]
    
    fig = px.scatter(dff, 
        x='x', 
        y='y',
        color='main_label',
        #color='main_keys',
        hover_name='title', 
        hover_data={
            'x':False,
            'y':False,
            #'main_keys':True,
            'main_label':True,
            'authors':True,
            'year':True,
            'type':True,
            'doi':True, 
            'main_keys':True,
            },
        #color_discrete_sequence=px.colors.qualitative.D3, 
        color_discrete_sequence= cc.glasbey,
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
        'showlegend': True,
        'legend': {'title':'Main Topic','itemsizing': 'constant'}, 
        'legend_font': {'family':"sans-serif", 'size':14, 'color':'white'}, 
        'clickmode': 'event+select',
        'hovermode': 'closest',
        }
        )

    if selected_pi:
        fig.update_traces(hovertemplate=None,hoverinfo='skip')

        filtered_df = dff[dff.Name == selected_pi]
    
        fig.add_trace(go.Scatter(
            x=filtered_df['x'], 
            y=filtered_df['y'], 
            text=filtered_df['title'],
            mode='markers', 
            marker=dict(
                color='whitesmoke',
                opacity=0.9,
                line=dict(
                    color='White',
                    width=2)
                ),
            hoverinfo='text', 
            hovertemplate= 
            "<b>Title: %{text}</b><br><br>" +
            "<extra></extra>",
            showlegend=False))
    
        return fig

    elif selected_dept:
        fig.update_traces(hovertemplate=None,hoverinfo='skip')

        filtered_df = dff[dff.PI_primary_dept == selected_dept]
    
        fig.add_trace(go.Scatter(
            x=filtered_df['x'], 
            y=filtered_df['y'], 
            text=filtered_df['title'],
            mode='markers', 
            marker=dict(
                color='whitesmoke',
                opacity=0.9,
                line=dict(
                    color='White',
                    width=2)
                ),
            hoverinfo='text', 
            hovertemplate= 
            "<b>Title: %{text}</b><br><br>" +
            "<extra></extra>",
            showlegend=False))
    
        return fig

    else:  
        fig = px.scatter(dff, 
            x='x', 
            y='y',
            color='main_label',
            #color='main_keys',
            hover_name='title',
            hover_data={
            'x':False,
            'y':False,
            #'main_keys':True,
            'main_label':True,
            'authors':True,
            'year':True,
            'type':True,
            'doi':True, 
            'main_keys':True,
            },
            #color_discrete_sequence=px.colors.qualitative.D3, 
            color_discrete_sequence= cc.glasbey,
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
            'showlegend': True,
            'legend': {'title':'Main Topic','itemsizing': 'constant'}, 
            'legend_font': {'family':"sans-serif", 'size':14, 'color':'white'}, 
            'clickmode': 'event+select',
            'hovermode': 'closest',
            }
            )

        return fig

    return graphs

@app.callback(
    Output('click-data', 'children'),
    [Input('graphs', 'clickData')])
def display_click_data(clickData):
    if clickData:
        return json.dumps(clickData, indent=4, sort_keys=True, separators=(',', ': '))   
    else:
        return html.P('Click on a document in the map to view its information.')

if __name__ == '__main__':
    app.run_server(debug=True)
