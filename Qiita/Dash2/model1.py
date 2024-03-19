# https://dash.plotly.com/minimal-app
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import base64
import io

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(__name__)

flag_uploaded = False

flag = False

app.layout = html.Div([
    # https://dash.plotly.com/dash-core-components/upload
    html.Div([
        dcc.Upload(
            id = 'upload_file',
            children = html.Div([
                html.Button(
                    children ='Upload File',
                    style={
                        'width': '100%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center'
                    }),
            ]),
            accept = '.csv',
        )
    ]),
    html.Div(id='select_parameters'),
    html.Div(id='graph-area')
])

def read_csv(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
        try:
            df_data = decoded.decode('utf-8-sig')
        except UnicodeDecodeError:
            try:
                df_data = decoded.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    df_data = decoded.decode('shift-jis')
                except UnicodeDecodeError as ue:
                    print(ue)
                    raise ValueError('This CSV file encoding is not supported')
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(df_data))
    elif 'xls' in filename or 'xlsx' in filename:
        # Assume that the user uploaded an excel file
        df = pd.read_excel(io.BytesIO(decoded))
    else:
        raise ValueError('This file type is not supported')
    return df

@callback(
    Output('select_parameters', 'children'),
    Input('upload_file', 'contents'),
    Input('upload_file', 'filename'))
def update_dropdown(contents, filename):
    if contents is not None:
        global df
        df = read_csv(contents, filename)
        global flag
        flag = True
        return [
            dcc.Dropdown(df.columns, value=df.columns[0], id = 'dropdown-selection_x'), 
            dcc.Dropdown(df.columns, value=df.columns[0], id = 'dropdown-selection_y'), 
            dcc.Dropdown(df.columns, value=df.columns[0], id = 'dropdown-selection_switch')]
    else:
        return None
    
# if flag:
@callback(
    Output('graph-area', 'children'),
    Input('dropdown-selection_switch', 'value'))
def update_switch(selected_section):
    if selected_section is not None:
        return html.Div([
            dcc.Dropdown(options=df[selected_section].unique, value=df[selected_section].unique[0], id='dropdown_switch'),
            dcc.Graph(id='graph-content')
        ])
    else:
        return None

# if flag:
@callback(
    Output(component_id='graph-content', component_property='figure'), 
    Input(component_id='dropdown_switch', component_property='value'),
    Input(component_id='dropdown-selection_switch', component_property='value'),
    Input(component_id='dropdown-selection_x', component_property='value'),
    Input(component_id='dropdown-selection_y', component_property='value'),
    )
def update_graph(selected,cols,x,y):
    if selected is not None:
        dff = df[df[cols] == selected]
        return px.line(dff, x=x, y=y, title='Graph')
    else:
        return None

if __name__ == '__main__':
    app.run_server(debug=True)