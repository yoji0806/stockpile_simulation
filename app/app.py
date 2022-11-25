import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go
import requests
import json




with open('.mapbox_token', 'r') as file:
    mapbox_access_token = file.read().rstrip()

with open('.gcp_spreadsheet_id', 'r') as file:
    gcp_spreadsheet_id = file.read().rstrip()

with open('.gcp_spreadsheet_token', 'r') as file:
    gcp_spreadsheet_token = file.read().rstrip()


df_scatter_map = pd.read_csv("./assets/df_disaster_related_site.csv")

external_stylesheets = ['app/assets/stylesheet.css']
app = dash.Dash()
app.config.external_stylesheets = external_stylesheets


blackbold={'color':'black', 'font-weight': 'bold'}



# Radar chart 1

# 災害発生1日後に、想定される量（完全に想定通りの場合）：
radar_1st_ideal = [5, 5, 5, 5, 5, 5]
radar_1st_real = [4.5, 4.5, 4.5, 4.5, 4.5, 4.5]


# SpreadSheetを読み取る。
url = "https://sheets.googleapis.com/v4/spreadsheets/{}/values/フォームの回答 1?key={}".format(gcp_spreadsheet_id, gcp_spreadsheet_token)
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

jsonData = json.loads(response.text)


radar_chart_1 = go.Figure()
categories = ['飲料水','食料','簡易トイレ',
              '赤ちゃん用品', '女性の生活用品', '高齢者の生活用品']
radar_chart_1.add_trace(go.Scatterpolar(
      r=radar_1st_ideal,
      theta=categories,
      fill='toself',
      name='必要とされる量'
))
radar_chart_1.add_trace(go.Scatterpolar(
      r=radar_1st_real,
      theta=categories,
      fill='toself',
      name='実際の備蓄量'
))

radar_chart_1.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=True
)


# Radar chart 2
radar_chart_2 = go.Figure()
categories = ['飲料水','食料','簡易トイレ',
              '赤ちゃん用品', '女性の生活用品', '高齢者の生活用品']
radar_chart_2.add_trace(go.Scatterpolar(
      r=[4, 4, 4, 4, 4, 4],
      theta=categories,
      fill='toself',
      name='必要とされる量'
))
radar_chart_2.add_trace(go.Scatterpolar(
      r=[3.5, 3.5, 3.5, 3.5, 3.5, 3.5],
      theta=categories,
      fill='toself',
      name='実際の備蓄量'
))

radar_chart_2.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=True
)



# Radar chart 3
radar_chart_3 = go.Figure()
categories = ['飲料水','食料','簡易トイレ',
              '赤ちゃん用品', '女性の生活用品', '高齢者の生活用品']
radar_chart_3.add_trace(go.Scatterpolar(
      r=[3, 3, 3, 3, 3, 3],
      theta=categories,
      fill='toself',
      name='必要とされる量'
))
radar_chart_3.add_trace(go.Scatterpolar(
      r=[2.5, 2.5, 2.5, 2.5, 2.5, 2.5],
      theta=categories,
      fill='toself',
      name='実際の備蓄量'
))

radar_chart_3.update_layout(
  polar=dict(
    radialaxis=dict(
      visible=True,
      range=[0, 5]
    )),
  showlegend=True
)





app.layout = html.Div([
#---------------------------------------------------------------

    # first row
    html.Div([

        # Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#00FC87','height':'65vh'}
            )
        ], className='ten columns'
        ),

        html.Div([
            # Map-legend
            html.Ul([
                html.Li("避難所", className='circle', style={'background': '#ff00ff','color':'black',
                    'list-style':'none','text-indent': '17px', 'font-size':'40px', 'margin-top':'150px'}),
                html.Li("災害用トイレ", className='circle', style={'background': '#daa520','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap', 'font-size':'30px'}),
                html.Li("給水拠点", className='circle', style={'background': '#00bfff','color':'black',
                    'list-style':'none','text-indent': '17px', 'font-size':'30px'}),
                # html.Li("Plastic_bags", className='circle', style={'background': '#00ff00','color':'black',
                #     'list-style':'none','text-indent': '17px'}),
                # html.Li("Recycling_bins", className='circle',  style={'background': '#FF0000','color':'black',
                #     'list-style':'none','text-indent': '17px'}),
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),

            # _checklist
            html.Label(children=['施設: '], style=blackbold),
            dcc.Checklist(id='kind',
                    options=[{'label':str(b),'value':b} for b in sorted(df_scatter_map['kind'].unique())],
                    value=[b for b in sorted(df_scatter_map['kind'].unique())],
            ),

        ], className='two columns'),

    ], 
    className='row'),


    # second row 
    html.Div([
        
        # Radar chart 1
        html.Div([
            dcc.Graph(figure=radar_chart_1),
            html.H4('災害発生から1日後'),
        ], className='four columns', style={'text-align':'center'}),

        # Radar chart 2
        html.Div([
            dcc.Graph(figure=radar_chart_2),
            html.H4('2日後'),
        ], className='four columns', style={'text-align':'center'}),

        # Radar chart 3
        html.Div([
            dcc.Graph(figure=radar_chart_3),
            html.H4('3日後'),
        ], className='four columns', style={'text-align':'center'}),

    ], className='row',style={'margin':'0dp', 'padding':'0dp'})



], className='ten columns offset-by-one'
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(
    Output('graph', 'figure'),
    Input('kind', 'value')
    )

def update_figure(chosen_boro):
    df_sub = df_scatter_map[(df_scatter_map['kind'].isin(chosen_boro))]


    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['longitude'],
                    lat = df_sub['latitude'],
                    mode='markers',
                    marker={'color' : df_sub['color'], 'size':10},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=df_sub['name'],
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            title=dict(text="078KOBE 備蓄の需要シミュレーション",font=dict(size=50, color='green')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                style='light',
                center=dict(
                    lat=34.72481,
                    lon=135.29442
                ),
                pitch=50,
                zoom=12
            ),
        )
    }






if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=True)