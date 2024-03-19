# https://dash.plotly.com/minimal-app
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

app.layout = html.Div([
    html.H1(children='Title of Dash App',style={'textAlign': 'center'}),
    dcc.Dropdown(df.country.unique(), value='Canada', id = 'dropdown-selection'),
    dcc.Graph(id = 'graph-content')
])

@callback(
    Output(component_id='graph-content', component_property='figure'), 
    Input(component_id='dropdown-selection', component_property='value'))
def update_graph(selected_country):
    dff = df[df.country == selected_country]
    return px.line(dff, x='year', y='gdpPercap', title='GDP per Capita')

if __name__ == '__main__':
    app.run_server(debug=True)