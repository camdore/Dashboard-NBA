from distutils.command import clean
import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output

start = time.time()

def scraper_html(url):
    """
    Extrait les données de l'url donnée

    Args : 
        url : adresse du site à étudier

    Returns :
        df : la dataframe extraite
    """
    df = pd.read_html(url,flavor='lxml')[0]
    return df

def clean_data_html(df):
    """
    Nettoie la dataframe extraite à partir de l'url en enlevant toutes 
    les colonnes inutiles et convertie les données dans les bons dtypes

    Args :
        df : dataframe brut/extraite

    Returns :
        df : dataframe nettoyée
    """
    # nettoyage de la df
    asup = df[df['Rk']=='Rk']
    df.drop(asup.index, axis=0,inplace=True)
    df.drop(df.columns[[0,6,21,22,23,24,25,26,27,28]],axis=1,inplace=True)
    df = df.drop_duplicates(subset=['Player'])

    # création de subset pour les convertions
    varfloat = df[['FG%','3P%','2P%','eFG%','FT%']]
    varint = df[['Age','G','MP','FG','FGA','3P','3PA','2P','2PA','PTS','FT','FTA']]

    # conversion avec les bon dtypes
    for col in varfloat.columns :
        if col in varfloat :
            df[col]=df[col].astype('float') # a modfier et utiliser .loc ou .at

    for col in varint.columns :
        if col in varint :
            df[col]=df[col].astype('int')

    df['Player']=df['Player'].astype('string')
    df['Tm']=df['Tm'].astype('string')
    df['Pos']=df['Pos'].astype('category')
    
    # print(df)
    return df

def clean_data_csv(df):
    """
    Nettoie la 2e dataframe extraite du csv en enlevant toutes 
    les colonnes inutiles et convertie les données dans les bons dtypes

    Args :
        df : la dataframe extraite du csv
    
    Returns : 
        df : la dataframe nettoyée
    """
    # nettoyage de la df, on enlève les colonnes inutiles
    df.drop(df.columns[[0,1,2,3,5,6,7,8,9,10,19,20,22,23]],axis=1,inplace=True)

    # création de subset pour les convertions
    varcat = df[['SHOT_TYPE','SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','ACTION_TYPE']]

    # conversion avec les bon dtypes
    for col in varcat.columns:
        if col in varcat :
            df[col]=df[col].astype('category')

    df['PLAYER_NAME']=df['PLAYER_NAME'].astype('string')
    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], format='%Y%m%d')
    # print(df)
    return df

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
    # print(dfsorted)

    return dfsorted

def prep_query(df): # a mettre dans le main???
    """
    on formate les dates de début et fin de saison pour
    pouvoir utiliser le query correctement.

    Args : 
        df : dataframe 

    Retruns : 
        dico : dictionnaire dont les clés sont des années et les valeurs
        sont les données, sous forme de dataframe, correspondantes à la saison
    """
    dico = {}
    for year in range(2003,2018,1):
        start_date = str(year)+'-10'
        end_date = str(year+1) +'-05'
        dico[year]= df.query("GAME_DATE>=@start_date and GAME_DATE<=@end_date")

    return dico

def histo(df,xaxis,yaxis,titre):
    """
    Créé un histogramme en fonction des différents paramètres

    Args :
        df : la dataframe utilisée \n
        x : axe des abscisses en str \n
        y : axe des ordonnées en str \n
        title : titre du graphique en srt

    Returns :
        fig : le graphique correspondant
    """
    fig = px.histogram(df, x=xaxis,y=yaxis,histfunc='sum',title=titre)
    # fig.show()
    return fig

def ellipse_arc(x_center=0, y_center=0, a=1, b =1, start_angle=0, end_angle=2*np.pi, N=100, closed= False):
    """
    la fonction ellipse_arc vient du site suivant : 
    https://community.plotly.com/t/arc-shape-with-path/7205/5
    parce que  dans la fonction add_shape() le paramètre path
    n'accepte pas les arcs de cercle (A) (doc officielle) 
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
    trace toutes les lignes du terrain de basket sur la figure,
    permet également de mettre en forme la figure

    Args : 
        fig3 : figure utilisée pour la géolocalisation

    Returns :
        fig3 : retourne la figure avec le terrain de basket tracé
    """
    # set l'intervalle de l'axe y pour avoir la moitié du terrain qui nous intéresse
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



url = 'https://www.basketball-reference.com/leagues/NBA_2018_totals.html'
url2 = 'https://www.basketball-reference.com/leagues/NBA_2013_totals.html'
url3 = 'https://www.basketball-reference.com/leagues/NBA_2004_totals.html'
dfsaison = scraper_html(url)
dfsaison = clean_data_html(dfsaison)
dflebron = pd.read_csv('csv_geoloc.csv',delimiter = ';')
dflebron = clean_data_csv(dflebron)
# df2 = scraper_html(url2)
# df2 = clean_data(df2)
# df3 = scraper_html(url3)
# df3 = clean_data(df3)
dfsort = top_ten(dfsaison,'PTS')
dicolebron = prep_query(dflebron)
fig = histo(dfsort,'Player','PTS','PTS en fonction des joueurs')
fig2 = histo(dfsaison,'Pos','PTS','PTS en fonction des positions')
fig3 = px.scatter(dicolebron[2003],x='LOC_X',y='LOC_Y')
fig3 = trace_terrain(fig3)

# MAIN
app = Dash(__name__)

app.layout = html.Div(children=[

html.H1(children='NBA Dashboard geoloc'),

html.Label('Season : '),

    # my input 
     dcc.Slider(2003, 2017, 
        step=1,
        marks={
          2003 : '2003',
          2004 : '2004',
          2005 : '2005',
          2006 : '2006',
          2007 : '2007',
          2008 : '2008',
          2009 : '2009',
          2010 : '2010',
          2011 : '2011',
          2012 : '2012',
          2013 : '2013',
          2014 : '2014',
          2015 : '2015',
          2016 : '2016',
          2017 : '2017',
        },
        id='years-slider',
        value=2003
    ),

    # my output : the Graph figure = fig 
    dcc.Graph(
        id='graph1',
        figure=fig3
    ),

    html.Div(children='''
            Description of the graph above. Mouse over for details
    '''),
])

@app.callback(
        Output(component_id='graph1', component_property='figure'),
        # Output(component_id='graph2', component_property='figure'),
        Input(component_id='years-slider', component_property='value'),
        # Input(component_id='point-checklist2', component_property='value'),
)

def update_figure(input_value):
    fig3 = px.scatter(
        dfsaison[input_value],
        x='LOC_X',
        y='LOC_Y',
        # color='SHOT_ZONE_BASIC'  
    )
    trace_terrain(fig3),
    return fig3

    
if __name__ == '__main__':
    app.run_server(debug=True) # RUN APP

end = time.time() 

print('execution time :',(end-start), "s")