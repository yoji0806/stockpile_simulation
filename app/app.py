import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go


with open('.mapbox_token', 'r') as file:
    mapbox_access_token = file.read().rstrip()


df_scatter_map = pd.read_csv("wip_kobe_evacuation_sites.csv")

external_stylesheets = ['app/assets/stylesheet.css']
app = dash.Dash()
app.config.external_stylesheets = external_stylesheets


blackbold={'color':'black', 'font-weight': 'bold'}



# Radar chart
radar_chart = go.Figure()
categories = ['飲料水','食料','簡易トイレ',
              '赤ちゃん用品', '女性の生活用品', '高齢者の生活用品']
radar_chart.add_trace(go.Scatterpolar(
      r=[1, 5, 2, 2, 3, 4],
      theta=categories,
      fill='toself',
      name='必要とされる量'
))
radar_chart.add_trace(go.Scatterpolar(
      r=[4.0, 3.1, 2.5, 1.1, 1.4, 1.8],
      theta=categories,
      fill='toself',
      name='実際の備蓄量'
))

radar_chart.update_layout(
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
                html.Li("Compost", className='circle', style={'background': '#ff00ff','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Electronics", className='circle', style={'background': '#0000ff','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),
                html.Li("Hazardous_waste", className='circle', style={'background': '#FF0000','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Plastic_bags", className='circle', style={'background': '#00ff00','color':'black',
                    'list-style':'none','text-indent': '17px'}),
                html.Li("Recycling_bins", className='circle',  style={'background': '#824100','color':'black',
                    'list-style':'none','text-indent': '17px'}),
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),

            # Borough_checklist
            html.Label(children=['Borough: '], style=blackbold),
            dcc.Checklist(id='boro_name',
                    options=[{'label':str(b),'value':b} for b in sorted(df_scatter_map['boro'].unique())],
                    value=[b for b in sorted(df_scatter_map['boro'].unique())],
            ),

            # Recycling_type_checklist
            html.Label(children=['対象: '], style=blackbold),
            dcc.Checklist(id='recycling_type',
                    options=[{'label':str(b),'value':b} for b in sorted(df_scatter_map['type'].unique())],
                    value=[b for b in sorted(df_scatter_map['type'].unique())],
            ),

            # Web_link
            html.Br(),
            html.Label(['Website:'],style=blackbold),
            html.Pre(id='web_link', children=[],
            style={'white-space': 'pre-wrap','word-break': 'break-all',
                 'border': '1px solid black','text-align': 'center',
                 'padding': '12px 12px 12px 12px', 'color':'blue',
                 'margin-top': '3px'}
            ),
        ], className='two columns'),

    ], 
    className='row'),


    # second row 
    html.Div([
        
        # Radar chart 1
        html.Div([
            dcc.Graph(figure=radar_chart),
            html.H4('災害発生から1日後'),
        ], className='four columns', style={'text-align':'center'}),

        # Radar chart 2
        html.Div([
            dcc.Graph(figure=radar_chart),
            html.H4('2日後'),
        ], className='four columns', style={'text-align':'center'}),

        # Radar chart 3
        html.Div([
            dcc.Graph(figure=radar_chart),
            html.H4('3日後'),
        ], className='four columns', style={'text-align':'center'}),

    ], className='row',style={'margin':'0dp', 'padding':'0dp'})



], className='ten columns offset-by-one',style={'margin':'0dp', 'padding':'0dp'}
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('boro_name', 'value'),
               Input('recycling_type', 'value')])

def update_figure(chosen_boro,chosen_recycling):
    df_sub = df_scatter_map[(df_scatter_map['boro'].isin(chosen_boro)) &
                (df_scatter_map['type'].isin(chosen_recycling))]

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['longitude'],
                    lat = df_sub['latitude'],
                    mode='markers',
                    marker={'color' : df_sub['color']},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=df_sub['hov_txt'],
                    customdata=df_sub['website']
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
                bearing=25,
                style='light',
                center=dict(
                    lat=34.72481,
                    lon=135.29442
                ),
                pitch=40,
                zoom=11.5
            ),
        )
    }
#---------------------------------------------------------------
# callback for Web_link
@app.callback(
    Output('web_link', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return 'Click on any bubble'
    else:
        # print (clickData)
        the_link=clickData['points'][0]['customdata']
        if the_link is None:
            return 'No Website Available'
        else:
            return html.A(the_link, href=the_link, target="_blank")
# #--------------------------------------------------------------



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8050", debug=True)