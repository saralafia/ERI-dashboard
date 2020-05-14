import os
import pandas as pd
import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('data.csv', index_col=0)
mytitle='ERI projects & publications (2009 - 2019) clustered by topic'
githublink='https://github.com/saralafia/ERI-dashboard'

fig = px.scatter(df, 
                 x=df.x, 
                 y=df.y,
                 color=df.main_label, 
                 hover_data={'x':False,
                             'y':False, 
                             'title':df.title,
                             'authors':df.authors,
                             'identifier':df.identifier,
                             'year':df.year, 
                             'type':df.type, 
                             'topic_keywords':df.main_keys, 
                             'main_label':False},
                 color_discrete_sequence=px.colors.qualitative.D3,
                 template='plotly_white')

fig.update_layout(xaxis_showgrid=False, 
                  yaxis_showgrid=False, 
                  xaxis_zeroline=False, 
                  yaxis_zeroline=False, 
                  yaxis_visible=False, 
                  xaxis_visible=False)

fig.update_layout(height=800, width=1200, legend_title='Main Topic', legend= {'itemsizing': 'constant'})

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div([
    html.H1(mytitle), 
    html.A('code + data', href=githublink, target="_blank"),
    html.Br(),
    dcc.Graph(
        id='ERI-map',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
