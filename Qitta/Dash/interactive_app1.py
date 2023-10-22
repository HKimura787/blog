import pandas as pd
import geopandas as gpd
import os
from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import numpy as np

def data_handring():

    # the function to get absolute path 
    def get_absolute_path(path):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(this_dir, path)

    # read geojson
    gdf = gpd.read_file(get_absolute_path('data\prefectures.geojson'))

    # read csv
    df = pd.read_csv(get_absolute_path('data\SSDSE-B-2023.csv'), encoding='shift_jis', skiprows=1)

    # merge csv and geojson
    merged_df = gpd.GeoDataFrame(df.merge(gdf, left_on='都道府県', right_on='name', how = 'left'))
    print(merged_df.head())
    
    # plot map
    # merged_df.query('年度==2020').plot(column='総人口', legend=True, figsize=(10, 10))
    # plt.show()

    return merged_df

def main():
    df = data_handring()

    app = Dash(__name__)

    # レイアウトの作成
    app.layout = html.Div([
        html.H1('都道府県別統計データの推移'),
        html.Div([
            html.Div([
                html.H2('データを選択'),
                dcc.Dropdown(
                    id='data',
                    options=[{'label': i, 'value': i} for i in df.columns[3:]],
                    value='総人口',
                    style={'width': '50%'}
                )
            ]),
            html.Div([
                html.H2('地図に表示する年度を選択'),
                dcc.RadioItems(
                    id='year',
                    options=[{'label': i, 'value': i} for i in np.arange(df['年度'].min(), df['年度'].max()+1)],
                    value=df['年度'].max(),
                    style={'display': 'flex'})
            ]),
        ]),
        html.Div([
            html.Div([
                html.H2(id='graph_title',),
                dcc.Graph(id='graph',style={'height': '70vh'}),
            ]),
            html.Div([
                html.H2(id='map_title'),
                dcc.Graph(id='map',style={'height': '70vh'})
            ]),
        ], style={'display': 'flex'})])
    
    # 時系列グラフのタイトルを変更するためのコールバック関数
    @app.callback(Output('graph_title', 'children'),
        [Input('map', 'selectedData'), Input('data', 'value')])
    def data_graph_title(selectedData, data):
        if selectedData is None:
            return f'全国の{data}の推移'
        else:
            location = selectedData['points'][0]['location']
            return f'{location}の{data}の推移'
    
    # 時系列グラフを更新するためのコールバック関数
    @app.callback(Output('graph', 'figure'),
        [Input('map', 'selectedData'), Input('data', 'value')])
    def display_selected_data(selectedData, data):
        if selectedData is None:
            filtered_df = df.groupby('年度').sum().reset_index()
        else:
            location = selectedData['points'][0]['location']
            filtered_df = df.query('都道府県 == @location')
        fig = px.line(filtered_df, x='年度', y=data)
        return fig
    
    # 地図のタイトルを変更するためのコールバック関数
    @app.callback(
        Output('map_title', 'children'),
        [Input('year', 'value'), Input('data', 'value')])
    def map_title(year, data):
        return f'{year}年度の{data}の地図'
    
    # 地図を更新するためのコールバック関数
    @app.callback(
        Output('map', 'figure'),
        [Input('year', 'value'), Input('data', 'value')])
    def update_map(year,data):
        filtered_df = df.query(f'年度 == {int(year)}').set_index('都道府県')       
        fig = px.choropleth(
            filtered_df, 
            geojson=filtered_df.geometry, 
            locations=filtered_df.index, 
            color=data,
            projection="mercator",
            fitbounds="locations",
            range_color=(df[data].min(), df[data].max()),
            color_continuous_scale="Reds",
            color_discrete_map="white",
            basemap_visible=False)
        fig.update_layout(clickmode='event+select')        
        return fig
    
    # サーバーの起動
    app.run_server(debug=True, use_reloader=False)

if __name__ == '__main__':
    main()