import pandas as pd
import numpy as np
import plotly.express as px
import dash
from dash import Dash, html, dcc, Input, Output
from functions import clean_data_html
from functions import convert_data_html
from functions import clean_data_csv
from functions import convert_data_csv


def top_ten(df,cat):
    """
    Retourne les 10 meilleurs joueurs selon la catégorie selectionnée

    Args : 
        df : la dataframe \n
        cat :  le nom de la catégorie en str

    Returns : 
        dfsorted : la dataframe triée des 10 meilleurs joueurs selon le critère choisi
    """
    dfsorted = df.sort_values(by=[cat],ascending=False).head(10)

    return dfsorted

def prep_query(dico,df):
    """
    on formate les dates de début et fin de saison pour
    pouvoir utiliser le query correctement.

    Args :
        dico : le dictionnaire qui va accueillir les données\n 
        df : dataframe 

    Retruns : 
        dico : dictionnaire dont les clés sont des années et les valeurs
        sont les données, sous forme de dataframe, correspondantes à la saison
    """
    for year in range(2003,2018,1):
        start_date = str(year)+'-10'
        end_date = str(year+1) +'-05'
        dico[year]= df.query("GAME_DATE>=@start_date and GAME_DATE<=@end_date")

    return dico

def ellipse_arc(x_center=0, y_center=0, a=1, b =1, start_angle=0, end_angle=2*np.pi, N=100, closed= False):
    """
    Permet de faire des arcs de cercle équivalents à ceux proposés en SVG 

    Args : 
        x_center : la coordonée x du centre de l'arc de cercle \n
        y_center : la coordonée y du centre de l'arc de cercle \n
        a : point du début de l'arc de cercle \n
        b : point de fin de l'arc de cerlce \n
        start_angle : angle du début de l'arc de cercle \n
        end_angle : angle de la fin de l'arc de cercle \n
        N = nombre d'échantillons pour linspace \n
        closed : fermer ou non l'arc de cercle (bool) 

    Returns: 
        path : le chemin correspondant au l'arc de cercle en SVG (Scalable Vector Graphics)
    """
    t = np.linspace(start_angle, end_angle, N)
    x = x_center + a*np.cos(t)
    y = y_center + b*np.sin(t)
    path = f'M {x[0]}, {y[0]}'
    for k in range(1, len(t)):
        path += f'L{x[k]}, {y[k]}'
    if closed:
        path += ' Z'

    return path

def trace_terrain(fig3):
    """
    Trace toutes les lignes du terrain de basket sur la figure,
    permet également de mettre en forme la figure

    Args : 
        fig3 : figure utilisée pour la géolocalisation.

    Returns :
        fig3 : retourne la figure avec le terrain de basket tracé.
    """
    # configure l'intervalle de l'axe y pour avoir la moitié du terrain qui nous intéresse
    fig3.update_yaxes(range=[-60,430])

    # pour garder les proportions du terrain
    fig3.update_layout( 
        width=900,
        height=900*0.94,
        )

    # On trace le terrain de basket ligne par ligne

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
    fig3.add_shape(type="path",
        path=ellipse_arc(a=40, b=40, start_angle=0, end_angle=np.pi),
    )# restricted area
    fig3.add_shape(type="path",
        path=ellipse_arc(a=237.5, b=237.5, start_angle=0.386283101, end_angle=np.pi - 0.386283101),
    )# ligne 3 points

    return fig3

def data_inter(dico):
    """
    Crée une dataframe adaptée

    Args : 
        dico : dictionnaire qui est retourné par query et dont les clés sont des années et les valeurs
        sont les données, sous forme de dataframe, correspondantes à la saison.

    Returns :
        dfinter : la dataframe adaptée pour la figure 4 avec pour colonnes :
        'Year', '2PT Field Goal','3PT Field Goal'
    """
    l2pt =[]
    l3pt = []
    lyear = []
    for year, dataf in dico.items():
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

    return dfinter

url = 'https://www.basketball-reference.com/leagues/NBA_2018_totals.html'

df_url = pd.read_html(url,flavor='lxml')[0]
df_url = clean_data_html(df_url)
df_url = convert_data_html(df_url)

dfsorted = top_ten(df_url,'PTS')
fig = px.histogram(
    dfsorted,
    x='Player',
    y='PTS',
    histfunc='sum',
    title='Points en fonction des top 10 joueurs'
)
fig.update_xaxes(title_text='Time')
fig.update_yaxes(title_text='Points')

fig2 = px.histogram(df_url,
    x='Pos',
    y='FG',
    histfunc='sum',
    title='Points marqués en fonction de la position'
)
fig2.update_xaxes(title_text='Position')
fig2.update_yaxes(title_text='Points')

df_csv = pd.read_csv('csv_geoloc.csv',delimiter = ';')
df_csv = clean_data_csv(df_csv)
df_csv = convert_data_csv(df_csv)

dicolebron={}
dicolebron = prep_query(dicolebron,df_csv)

fig3 = px.scatter(
    dicolebron[2003],
    x='LOC_X',
    y='LOC_Y',
    color='SHOT_ZONE_BASIC',
    title='Terrain de basket avec la géolocalisation de chaque panier marqué'
)
fig3 = trace_terrain(fig3)

dfinter = data_inter(dicolebron)

fig4 = px.line(
    dfinter,
    x='Year',
    y='Mid-Range',
    title='Evolution des zones de tirs en fonction des années'
)
fig5 = px.histogram(
    df_url,
    x='Age',y='3P%',
    histfunc='avg',
    title= "Paniers marqués en fonction de l'âge"
)


###################################### Dash App ######################################

app = Dash(__name__)

app.layout = html.Div(children=[

    html.H1(children='NBA Dashboard', style={'text-align':'center','font-family':'Arial'}),

    html.H2('Statistiques sur la saison 2017-2018 :',style={'font-family':'Arial'}),

    html.Label('Type de paniers : ',style={'font-family':'Arial'}),

    # my input 
    dcc.Checklist(
        id='point-checklist',
        options=[
            {'label':'3P (3-Points Field Goals)', 'value':'3PTS'},
            {'label':'2P (2-Points Field Goals)', 'value':'2PTS'},
            {'label':'FT (Free Throws)', 'value':'FT'},
        ],
    ),

    # my output : the Graph figure = fig
    dcc.Graph(
        id='graph1',
        figure=fig
    ),

    html.Label('Type de paniers : ',style={'font-family':'Arial'}),
    
    dcc.Checklist(
        id='point-checklist2',
        options=[
            {'label':'3P (3-Points Field Goals)', 'value':'3PTS'},
            {'label':'2P (2-Points Field Goals)', 'value':'2PTS'},
            {'label':'FT (Free Throws)', 'value':'FT'},
        ],
    ),

    dcc.Graph(
        id='graph2',
        figure=fig2
    ),

    dcc.Checklist(
        id='point-checklist4',
        options=[
            {'label':'FG% (Field Goals%)', 'value':'FG%'},
            {'label':'3P%', 'value':'3P%'},
            {'label':'2P%', 'value':'2P%'},
            {'label':'3PA (3-Points Field Attempted)', 'value':'3PA'},
            {'label':'2PA (2-Points Field Attempted)', 'value':'2PA'},            
        ],
    ),
    dcc.Graph(
        id='graph5',
        figure=fig5
    ),

    html.H2('Statistique sur Lebron James entre 2003 et 2018',style={'font-family':'Arial'}),

    html.Label('Type de représentation : ',style={'font-family':'Arial'}),

    dcc.RadioItems(
        options=[
            {'label': 'Range', 'value': 'SHOT_ZONE_RANGE'},
            {'label': 'Basic', 'value': 'SHOT_ZONE_BASIC'},
            {'label': 'Area', 'value': 'SHOT_ZONE_AREA'},
        ],
        id = 'radio-item',
        value='SHOT_ZONE_BASIC',
    ),

    html.Label('Saison : ',style={'font-family':'Arial'}),

    # my input 
    dcc.Slider(2003,2017, 
        step =1,
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
        id='graph3',
        figure=fig3
    ),

    html.Label('Type de paniers :',style={'font-family':'Arial'}),

    dcc.Checklist(
        id='point-checklist3',
        options=[
            {'label':'3PTS', 'value':'3PT Field Goal(Above 24ft.)'},
            {'label':'Mid-Range', 'value':'Mid-Range'},
        ],
    ),

    dcc.Graph(
        id='graph4',
        figure=fig4
    ),

    html.Div(children='''
            Dashboard crée par Camille Doré et Thomas Ekué pour l’unité DSIA-4101C
    ''',
    style={'font-family':'Arial'}),
])

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='graph4', component_property='figure'),
    Output(component_id='graph5', component_property='figure'),
    Input(component_id='point-checklist', component_property='value'),
    Input(component_id='point-checklist2', component_property='value'),
    Input(component_id='point-checklist3', component_property='value'),
    Input(component_id='point-checklist4', component_property='value'),
)

def update_figure(input_value,input_value2,input_value3,input_value4):
    fig = px.histogram(
        dfsorted, 
        x='Player',
        y= input_value,
        histfunc='sum',
        title='Points en fonction des 10 meilleurs joueurs'
    )
    fig2 = px.histogram(
        df_url, 
        x='Pos',
        y= input_value2,
        histfunc='sum',
        title='Paniers marqués en fonction de la position'
    )
    fig4 = px.line(
        dfinter,
        x = 'Year',
        y = input_value3,
        title='Evolution des type de shots en fonction des années',
    )
    fig5 = px.histogram(
        df_url, 
        x='Age',
        y= input_value4,
        histfunc='avg',
        title= "Paniers marqués en fonction de l'âge"
    )
    return fig,fig2,fig4,fig5


@app.callback(
    Output(component_id='graph3', component_property='figure'),
    Input(component_id='years-slider', component_property='value'),
    Input(component_id='radio-item', component_property='value'),
    # prevent_initial_call=True
)  

def update_map(input_value,input_value2):
    if input_value in [2010,2011,2012,2013]:
        return dash.no_update

    fig3 = px.scatter(
            dicolebron[input_value],
            x='LOC_X',
            y='LOC_Y',
            color= input_value2,
            title='Terrain de basket avec la géolocalisation de chaque panier marqué',
        )
    trace_terrain(fig3),
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True) # RUN APP