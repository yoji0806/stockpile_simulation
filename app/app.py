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


df_scatter_map = pd.read_csv("./assets/df_disaster_related_site_kobe.csv")

external_stylesheets = ['app/assets/stylesheet.css']
app = dash.Dash()
app.config.external_stylesheets = external_stylesheets


blackbold={'color':'black', 'font-weight': 'bold'}
 


# Radar chart 1

# 災害発生1日後に、想定される量（完全に想定通りの場合）：
water_ideal = 5
food_ideal = 5
toilet_real = 5
baby_ideal = 5
woman_ideal = 5
elderly_ideal = 5

water_real = 4.5
food_real = 4.5
toilet_real = 4.5
baby_real = 4.5
woman_real = 4.5
elderly_real = 4.5
 

radar_1st_ideal = [4, 4, 4, 4, 4, 4]
radar_2nd_ideal = [3, 3, 3, 3, 3, 3]
radar_3rd_ideal = [2, 2, 2, 2, 2, 2]



# SpreadSheetを読みとる。=============================================================
url = "https://sheets.googleapis.com/v4/spreadsheets/{}/values/フォームの回答 1?key={}".format(gcp_spreadsheet_id, gcp_spreadsheet_token)
payload={}
headers = {}
response = requests.request("GET", url, headers=headers, data=payload)

jsonData = json.loads(response.text)
cols = jsonData['values'][0]
len_v = len(jsonData['values'])


# 通常の場合の、各備蓄物資への変化
effect_on_water = -1
effect_on_food = -1
effect_on_toilet = -1
effect_on_baby = -1
effect_on_women = -1
effect_on_elderly = -1


for i in range(1,len_v):
    v = jsonData['values'][i]
    
    '''
    ロジック：（for demo in 078kobe）
    - 【家族構成】×【どこへ歩いて避難しますか？】の2つのデータを用いる。
    - 何も問題がない場合、（完全な想定内＝従業員が会社に避難する。）全ての備蓄物が、1日分だけ減る。
        - 従業員が会社に避難しない場合、その分だけ備蓄物の減りは遅くなる。
        - 従業員が家族と共に会社に避難した場合、その分だけ備蓄物の減りは早くなる。
        - 1人分の変化は、1/3目盛り分とする。（10人程度の中小企業が対象と思えば妥当ではないだろうか。）
        （※単純化のために、最小/最大の1日の減りは0~3分目とする。つまり想定の0~3倍。）
    【家族構成】
        - 家族構成で特に、注目するのは幼児・成人女性・高齢者。なぜなら、彼/彼女らの特定の備蓄品は少ないと思われるから。
        - 子供は成人男性としてカウントする。（特に特別な物資を必要としないため。）
    【どこへ歩いて避難しますか？】
        - 会社の場合
            →（社員が独身の場合）：想定内。
            →（社員が家族と暮らしている場合）：想定してなかった人も来るということで、備蓄の過小ポイント。
        - 会社以外の場合→想定していた社員が来ないということで、備蓄の過剰ポイント。
    
    '''
    
    
    gender = v[1]
    
    
    
    #【家族構成】 幼児　（"人"が含まれているので数字だけする。）
    num_baby = int(v[3][0])
    
    #【家族構成】 子供
    num_child = int(v[4][0])
    
    #【家族構成】 成人（男性）
    num_man = int(v[5][0])
    
    #【家族構成】 成人（女性）
    num_woman = int(v[6][0])
    
    #【家族構成】 高齢者（男性、65歳以上）
    num_elder_man = int(v[7][0])
    
    #【家族構成】 高齢者（女性、65歳以上）
    num_elder_woman = int(v[8][0])
    
    #家族人数
    family_number = num_baby + num_child + num_man + num_woman + num_elder_man + num_elder_woman
    
    
    #【どこへ歩いて避難しますか？】
    answer_15 = v[-1]
    
    
    # '完全な想定内'ー＞従業員は独身で、（自宅が半壊した場合、）会社に避難する。
    if (answer_15 == '会社') & (family_number==1):
        pass
        
    # '想定外の不足'ー＞従業員は家族と共に、（自宅が半壊した場合、）会社に避難する。
    elif (answer_15 == '会社') & (family_number>1):
        number_effect = family_number-1
        # （性別・年齢に関わらず）人数の影響を受ける備蓄：
        effect_on_water -=  number_effect/3
        effect_on_food -=  number_effect/3
        effect_on_toilet -=  number_effect/3
        
        #特定の年齢/性別によって影響を受ける備蓄：
        effect_on_baby -= num_baby/3
        effect_on_women -= (num_woman + num_elder_woman)/3
        effect_on_elderly -= (num_elder_man + num_elder_woman)/3
        
    
    # '想定外の余り'ー＞従業員は（自宅が半壊した場合、）会社に避難しない。
    elif (answer_15 != '会社'):
        
        # （性別・年齢に関わらず）人数の影響を受ける備蓄：
        #TODO: 何人分のデータがあっても、正しい値が出るように正規化する。
        effect_on_water +=  1/3
        effect_on_food +=  1/3
        effect_on_toilet +=  1/3
        
        if gender == '女性':
            effect_on_women += 2 #1/3
            

        
# 最終的な調整：　　　 （※単純化のために、最小/最大の1日の減りは0~3分目とする。つまり想定の0~3倍。）

# +（備蓄が増える現象）にならないように調整。
effect_on_water = min(0, effect_on_water)
effect_on_food = min(0, effect_on_food)
effect_on_toilet = min(0, effect_on_toilet)
effect_on_baby = min(0, effect_on_baby)
effect_on_women = min(0, effect_on_women)
effect_on_elderly = min(0, effect_on_elderly)

# -（備蓄の減り）が大きくなりすぎないように調整。
effect_on_water = max(-3, effect_on_water)
effect_on_food = max(-3, effect_on_food)
effect_on_toilet = max(-3, effect_on_toilet)
effect_on_baby = max(-3, effect_on_baby)
effect_on_women = max(-3, effect_on_women)
effect_on_elderly = max(-3, effect_on_elderly)



# 災害発生から1日後の　実際の備蓄量
water_real += effect_on_water
food_real += effect_on_food
toilet_real += effect_on_toilet
baby_real += effect_on_baby
woman_real += effect_on_women
elderly_real += effect_on_elderly

radar_1st_real =  [
    water_real,
    food_real,
    toilet_real, 
    baby_real,
    woman_real,
    elderly_real
    ]



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


# 災害発生から2日後の　実際の備蓄量
water_real += effect_on_water
food_real += effect_on_food
toilet_real += effect_on_toilet
baby_real += effect_on_baby
woman_real += effect_on_women
elderly_real += effect_on_elderly

radar_2nd_real =  [
    water_real,
    food_real,
    toilet_real,
    baby_real,
    woman_real,
    elderly_real
    ]




# Radar chart 2
radar_chart_2 = go.Figure()
categories = ['飲料水','食料','簡易トイレ',
              '赤ちゃん用品', '女性の生活用品', '高齢者の生活用品']
radar_chart_2.add_trace(go.Scatterpolar(
      r=radar_2nd_ideal,
      theta=categories,
      fill='toself',
      name='必要とされる量'
))
radar_chart_2.add_trace(go.Scatterpolar(
      r=radar_2nd_real,
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



# 災害発生から3日後の　実際の備蓄量
water_real += effect_on_water
food_real += effect_on_food
toilet_real += effect_on_toilet
baby_real += effect_on_baby
woman_real += effect_on_women
elderly_real += effect_on_elderly

radar_2rd_real =  [
    water_real,
    food_real,
    toilet_real,
    baby_real,
    woman_real,
    elderly_real
    ]

# Radar chart 3
radar_chart_3 = go.Figure()
categories = ['飲料水','食料','簡易トイレ',
              '赤ちゃん用品', '女性の生活用品', '高齢者の生活用品']
radar_chart_3.add_trace(go.Scatterpolar(
      r=radar_3rd_ideal,
      theta=categories,
      fill='toself',
      name='必要とされる量'
))
radar_chart_3.add_trace(go.Scatterpolar(
      r=radar_2rd_real,
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