import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

start = time.time()

# on lit notre csv ATTENTION AVEC LE FILE PATH
df = pd.read_csv('csv_geoloc.csv',delimiter = ';')
# print(df)

# on drop les colonnes de period, gameID ect...   ON SUPP EVENT_TYPE?
df.drop(df.columns[[0,1,2,3,5,6,7,8,9,10,19,20,22,23]],axis=1,inplace=True)


# conversion avec les bons dtypes
# print(df.dtypes)
varcat = df[['SHOT_TYPE','SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','ACTION_TYPE']]

for col in varcat.columns:
    if col in varcat :
        df[col]=df[col].astype('category')

df['PLAYER_NAME']=df['PLAYER_NAME'].astype('string')

df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], format='%Y%m%d')

# print(df.dtypes)
# print(df.head(10))

# csv_data = df.to_csv('lebron_geoloc_clean.csv',encoding = 'utf8',index=False)

# on rajoute des colonnes pour les graphs et compter le nombre de points

dicosaison={}
dfvaluecount = pd.DataFrame(index=range(0, 30))
dfyear = pd.DataFrame(index=range(0, 30))
# dfyear.columns=['Index','Year']
l = []
l1 = []
# boucle pour query et avoir le bon format de date pour les débuts et fins de saison
# for year in range(2003,2018,1):
#     start_date = str(year)+'-10'
#     end_date = str(year+1) +'-05'
#     dicosaison[year]= df.query("GAME_DATE>=@start_date and GAME_DATE<=@end_date")


#     dfsaison = pd.DataFrame.from_dict(dicosaison[year])
#     dfsaison['COMPTEUR']= 1

#     compteur2PT= 1
#     compteur3PT= 1
#     for index, value in dfsaison['SHOT_TYPE'].items():
#         mem3 = compteur3PT
#         mem2 = compteur2PT 

#         if value =='2PT Field Goal':
#             compteur2PT+=1
#             dfsaison['COMPTEUR'].at[index]=mem2

#         elif value == '3PT Field Goal':
#             compteur3PT+=1
#             dfsaison['COMPTEUR'].at[index]=mem3

#     year = pd.Series(year)
#     value_count = dfsaison['SHOT_TYPE'].value_counts()
#     value_count = str(value_count)
#     x = value_count.split()
#     y = tuple((x[3],x[7]))
#     for value in y:
#         y[value]=int(y[value])
#     print(y)
#     l1.append(year)
#     l1.append(year)
#     l.append(value_count)
    # l1 = pd.Series(l1)
    # print(type(l1))
# dfvaluecount = pd.concat([value_count],ignore_index=True)
# dffinale = pd.concat([dfvaluecount])
# id = [i for i in range(0,30)]
# dfvaluecount = dfvaluecount.set_index(id)
# dfvaluecount = pd.concat(l)
# print(dfvaluecount.shape)
# dfyear = pd.concat(l1,ignore_index=True)
# dfyear.columns = ['Year']
# # print(dfyear)

# # print(dfyear)
# dffinal = pd.concat([dfyear, dfvaluecount],axis=1, ignore_index=True)
# print(dffinal)
dfinter = pd.DataFrame(columns=['Year','2PT Field Goal','3PT Field Goal'])
dicointer={}
# serie2pt = pd.Series()
# serie3pt = pd.Series()
# year = pd.Series()
for year in range(2003,2018,1):
    start_date = str(year)+'-10'
    end_date = str(year+1) +'-05'
    dicosaison[year]= df.query("GAME_DATE>=@start_date and GAME_DATE<=@end_date")
l2pt =[]
l3pt = []
lyear = []
for year, dataf in dicosaison.items():
    value_count = dataf['SHOT_TYPE'].value_counts()
    l2pt = np.append(l2pt,value_count[0]).astype(int)
    l3pt = np.append(l3pt,value_count[1]).astype(int)
    lyear = np.append(lyear,year).astype(int)

s2pt = pd.Series(l2pt)
s3pt = pd.Series(l3pt)
syear = pd.Series(lyear)
dfinter = pd.concat([syear,s2pt,s3pt],keys=['Year', '2PT Field Goal','3PT Field Goal'],axis=1)
# print(dfinter)
# les graphs


# dfquery={'2PT Field Goal':df.query('SHOT_TYPE == "2PT Field Goal"'),'3PT Field Goal':df.query('SHOT_TYPE == "3PT Field Goal"')}
# df_2shot = df.query('SHOT_TYPE == "2PT Field Goal"')
# df_3shot = df.query('SHOT_TYPE == "3PT Field Goal"')
# shot_type = df['SHOT_TYPE'].unique()
# print(shot_type)
# dfquery={type_shot:df.query("SHOT_TYPE == @type_shot") for type_shot in shot_type}
# dfquery = dict()
# dfquery['2PT Field Goal']=df_2shot
# dfquery['3PT Field Goal']=df_3shot
# dfgrp = df.groupby("SHOT_TYPE").mean()
# print(dfgrp)

# print(dfquery)
# # print(type(dfquery))
# print('cle',dfquery.keys(),'valeur',dfquery.values())


fig = px.line(dfinter,x='Year',y='2PT Field Goal',title='Evolution des shots en fonction des années')
# fig.show()
# fig2 = px.histogram(df,x='GAME_DATE',y='SHOT_TYPE',histfunc='count',color='SHOT_TYPE')
# fig2.show()

dfsaison={}
# boucle pour query et avoir le bon format de date pour les débuts et fins de saison
for year in range(2003,2018,1):
    start_date = str(year)+'-10'
    end_date = str(year+1) +'-05'
    dfsaison[year]= df.query("GAME_DATE>=@start_date and GAME_DATE<=@end_date")
# print(dfsaison.keys())
# la géolocalisation



fig3 = px.scatter(dfsaison[2003],x='LOC_X',y='LOC_Y',color='SHOT_ZONE_BASIC')
# fig3 = px.scatter(df,x='LOC_X',y='LOC_Y',color='SHOT_ZONE_AREA')
# fig3 = px.scatter(df,x='LOC_X',y='LOC_Y',color='SHOT_ZONE_RANGE')

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

app.layout = html.Div(children=[

    html.H1(children='NBA Dashboard geoloc'),

    # html.Label('Season : '),

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
            {'label':'3PTS', 'value':'3PT Field Goal'},
            {'label':'2PTS', 'value':'2PT Field Goal'},
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
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Input(component_id='years-slider', component_property='value'),
    Input(component_id='point-checklist2', component_property='value'),
)
def update_figure(input_value,input_value2):
    
    fig3 = px.scatter(
        dfsaison[input_value],
        x='LOC_X',
        y='LOC_Y',
        color='SHOT_ZONE_BASIC',
    )
    trace_terrain(fig3),
    fig = px.line(
        dfinter,
        x = 'Year',
        y = input_value2,
        title='Evolution des type de shots en fonction des années',
    )
    return fig3,fig
    

if __name__ == '__main__':
    app.run_server(debug=True) # RUN APP

end = time.time() 

print('execution time :',(end-start), "s")