import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output
from dash.exceptions import PreventUpdate

start = time.time()

# on lit notre csv ATTENTION AVEC LE FILE PATH
df = pd.read_csv('csv_geoloc.csv',delimiter = ';')

# on drop les colonnes de period, gameID ect...   ON SUPP EVENT_TYPE?
df.drop(df.columns[[0,1,2,3,5,6,7,8,9,10,19,20,22,23]],axis=1,inplace=True)

# conversion avec les bons dtypes
varcat = df[['SHOT_TYPE','SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','ACTION_TYPE']]

for col in varcat.columns:
    if col in varcat :
        df[col]=df[col].astype('category')

df['PLAYER_NAME']=df['PLAYER_NAME'].astype('string')

df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], format='%Y%m%d')


# csv_data = df.to_csv('lebron_geoloc_clean.csv',encoding = 'utf8',index=False)

# boucle pour query et avoir le bon format de date pour les débuts et fins de saison
dicosaison={}

for year in range(2003,2018,1):
    start_date = str(year)+'-10'
    end_date = str(year+1) +'-05'
    dicosaison[year]= df.query("GAME_DATE>=@start_date and GAME_DATE<=@end_date")

l2pt =[]
l3pt = []
lyear = []
for year, dataf in dicosaison.items():
    value_count = dataf['SHOT_ZONE_RANGE'].value_counts(sort=False)
    value_count2 = dataf['SHOT_ZONE_BASIC'].value_counts(sort=False)
    l2pt = np.append(l2pt,value_count2[3]).astype(int)
    l3pt = np.append(l3pt,value_count[1]).astype(int)
    lyear = np.append(lyear,year).astype(int)

s2pt = pd.Series(l2pt)
s3pt = pd.Series(l3pt)
syear = pd.Series(lyear)
dfinter = pd.concat([syear,s2pt,s3pt],keys=['Year', 'Mid-Range','3PT Field Goal(Above 24ft.)'],axis=1)
dfinter = dfinter.drop([7,8,9,10])

# les graphs
fig = px.line(dfinter,x='Year',y='Mid-Range',title='Evolution des zones en fonction des années')

color_list = px.colors.qualitative.Plotly
color_dict = {
    'zone_basic_color' : {
    'Mid-Range': color_list[0], 'In The Paint (Non-RA)': color_list[1],
    'Restricted Area': color_list[2], 'Left Corner 3': color_list[3],
    'Above the Break 3': color_list[4],'Right Corner 3' :color_list[5] 
    },
    'zone_area_color' : {
    'Right Side(R)': color_list[0], 'Left Side(L)': color_list[1],
    'Center(C)': color_list[2], 'Right Side Center(RC)': color_list[3],
    'Left Side Center(LC)': color_list[4]
    },
    'zone_range_color' : {
    '8-16 ft.': color_list[0], '16-24 ft.': color_list[1],
    'Less Than 8 ft.': color_list[2], '24+ ft.': color_list[3],
    },
}

# la géolocalisation
fig3 = px.scatter(
    dicosaison[2003],
    x='LOC_X',
    y='LOC_Y',
    color='SHOT_ZONE_BASIC',
    color_discrete_map = color_dict['zone_basic_color'],
    title='Terrain de basket avec la géolocalisation de chaque panier marqué'
)

def trace_terrain(fig3):
    # set axes ranges pour avoir la moitié du terrain qui nous intéresse
    # fig3.update_xaxes(range=[-250,250])
    fig3.update_yaxes(range=[-60,430])

    fig3.update_layout( # pour garder les proportions du terrain
        width=900,
        height=900*0.94,
        )

    # On trace le terrain de basket

    fig3.add_shape(type="rect",
        x0=-250, x1=250, y0=-52, y1=420,
    )# contour terrain
    fig3.add_shape(type="rect",
        x0=-80, x1=80, y0=-52, y1=138,
    )# in the paint
    fig3.add_shape(type="rect",
        x0=-250, x1=-220, y0=-52, y1=88,
    )# left corner
    fig3.add_shape(type="rect",
        x0=220, x1=250, y0=-52, y1=88,
    )# right corner
    fig3.add_shape(type="line",
        x0=250, x1=220, y0=237.5, y1=237.5,
    )
    fig3.add_shape(type="line",
        x0=-250, x1=-220, y0=237.5, y1=237.5,
    )
    fig3.add_shape(type="circle",
        x0=-7.5, y0=-7.5, x1=7.5, y1=7.5,
    )# panier
    fig3.add_shape(type="circle",
        x0=-60, y0=77.5, x1=60, y1=197.5,
    )
    fig3.add_shape(type="rect",
        x0=-2, y0=-7.25, x1=2, y1=-12.5,
    )
    fig3.add_shape(type="line",
        x0=-30, y0=-12.5, x1=30, y1=-12.5,
    )
    # from https://community.plotly.com/t/arc-shape-with-path/7205/5
    # because in fonction add_shape() arg path doesn't accept arcs (A) (doc officielle) 
    def ellipse_arc(x_center=0, y_center=0, a=1, b =1, start_angle=0, end_angle=2*np.pi, N=100, closed= False):
        t = np.linspace(start_angle, end_angle, N)
        x = x_center + a*np.cos(t)
        y = y_center + b*np.sin(t)
        path = f'M {x[0]}, {y[0]}'
        for k in range(1, len(t)):
            path += f'L{x[k]}, {y[k]}'
        if closed:
            path += ' Z'
        return path

    fig3.add_shape(type="path",
        path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
    )# restricted area
    fig3.add_shape(type="path",
        path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
    )# ligne 3 points

    return fig3


# dashboard
# visit http://127.0.0.1:8050/ in your web browser.
# app = dash.Dash() # On crée une instance de la classe Dash
app = Dash(__name__)

all_options = {
    'Zone': ['SHOT_ZONE_BASIC','SHOT_ZONE_RANGE',  'SHOT_ZONE_AREA'],
    'Color': [u'zone_basic_color', 'zone_range_color', 'zone_area_color']
}

app.layout = html.Div(children=[

    html.H1(children='NBA Dashboard geoloc'),

    # html.Label('Season : '),
    dcc.RadioItems(
        list(all_options.keys()),
        'Zone',
        id='zone-radio',#input1
    ),
    dcc.RadioItems(id='color-radio'),#input2 lié à input1

    # # my input 
     dcc.Slider(2003, 2017, 
        step=1,
        marks={
            2003 : '2003-2004',
            2004 : '2004-2005',
            2005 : '2005-2006',
            2006 : '2006-2007',
            2007 : '2007-2008',
            2008 : '2008-2009',
            2009 : '2009-2010',
            2014 : '2014-2015',
            2015 : '2015-2016',
            2016 : '2016-2017',
            2017 : '2017-2018',
        },
        id='years-slider',
        value=2003
    ),

    # my output : the Graph figure = fig 
    dcc.Graph(
        id='graph1',
        figure=fig3
    ),

    dcc.Checklist(
        id='point-checklist2',
        options=[
            {'label':'3PTS', 'value':'3PT Field Goal(Above 24ft.)'},
            {'label':'Mid-Range', 'value':'Mid-Range'},
        ],
    ),

    dcc.Graph(
        id='graph2',
        figure=fig
    ),

    html.Div(children='''
            Description of the graph above. Mouse over for details
    '''),
])
@app.callback(
    Output('color-radio', 'options'),
    Input('zone-radio', 'value')
)
def set_color_options(selected_zone):
    return [{'label': i, 'value': i} for i in all_options[selected_zone]]

@app.callback(
    Output('color-radio', 'value'),
    Input('color-radio', 'options')
)
def set_color_value(available_options):
    return available_options[0]['value']

@app.callback(
    Output('graph1', 'figure'),
    Input('color-radio', 'value'),
    Input('zone-radio', 'value'),
    Input('years-slider', 'value'))
    
def update_map(selected_zone,selected_color,input_value):

    fig3 = px.scatter(
        dicosaison[input_value],
        x='LOC_X',
        y='LOC_Y',
        color=selected_zone,
        color_discrete_map = color_dict[selected_color]
    )
    trace_terrain(fig3),
    if input_value == 2004:
        raise PreventUpdate
    else:
        return fig3

@app.callback(
    Output('graph2', 'figure'),
    Input('point-checklist2','value'))   
def update_figure(input_value2):
    fig = px.line(
        dfinter,
        x = 'Year',
        y = input_value2,
        title='Evolution des type de shots en fonction des années',
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True) # RUN APP

end = time.time() 

print('execution time :',(end-start), "s")