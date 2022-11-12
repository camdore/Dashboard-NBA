import pandas as pd
import numpy as np
import time
import plotly.express as px
from dash import Dash, html, dcc, Input, Output

start = time.time()

def url_scraper(url):
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
    les colonnes inutiles, les doublons

    Args :
        df : dataframe brut/extraite

    Returns :
        df : dataframe nettoyée
    """
    asup = df[df['Rk']=='Rk']
    df.drop(asup.index, axis=0,inplace=True)

    # on supprime les colonnes de rebonds ect...
    df.drop(df.columns[[0,6,21,22,23,24,25,26,27,28]],axis=1,inplace=True)

    # on supprime les doublons pour les joueues ayant changer d'équipe durant la saison
    df = df.drop_duplicates(subset=['Player'])

    return df

def convert_data_html(df):
    """
    Convertie toutes les colonnes dans les bon dtypes 
    + création de colonnes associées au pts par type de shot

    Args :
        df : dataframe brut/extraite

    Returns :
        df : dataframe nettoyée
    """
    # on crée des subsets pour les conversions
    varfloat = df[['FG%','3P%','2P%','eFG%','FT%']]
    varint = df[['Age','G','MP','FG','FGA','3P','3PA','2P','2PA','PTS','FT','FTA']]  
    # conversion avec les bon dtypes
    for col in varfloat.columns:
        if col in varfloat :
            df[col]=df[col].astype('float')
    for col in varint.columns:
        if col in varint :
            df[col]=df[col].astype('int')

    df['Player']=df['Player'].astype('string')
    df['Tm']=df['Tm'].astype('string')
    df['Pos']=df['Pos'].astype('category')

    # création de colonnes associées au pts par type de shot 
    # par ex : nb de pts pour les tir à 3pts = 3P * 3
    # et les Free Throws valent chacun 1pts
    df['3PTS']=df['3P']*3
    df['2PTS']=df['2P']*2

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

    return dfsorted

def histo (df,xaxis,yaxis,titre):
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

    return fig

def clean_data_csv(df):
    """
    Nettoie la 2e dataframe extraite du csv en enlevant toutes les colonnes inutiles

    Args :
        df : la dataframe extraite du csv
    
    Returns : 
        df : la dataframe nettoyée
    """
    df.drop(df.columns[[0,1,2,3,5,6,7,8,9,10,19,20,22,23]],axis=1,inplace=True)
    return df

def convert_data_csv(df):
    """
    Convertie toutes les colonnes dans les bon dtypes 
    + création de colonnes associées au pts par type de shot

    Args :
        df : dataframe brut/extraite

    Returns :
        df : dataframe nettoyée
    """
    # création de subset pour les convertions
    varcat = df[['SHOT_TYPE','SHOT_ZONE_BASIC','SHOT_ZONE_AREA','SHOT_ZONE_RANGE','ACTION_TYPE']]
    
    # conversion avec les bons dtypes
    for col in varcat.columns:
        if col in varcat :
            df[col]=df[col].astype('category')

    df['PLAYER_NAME']=df['PLAYER_NAME'].astype('string')

    df['GAME_DATE'] = pd.to_datetime(df['GAME_DATE'], format='%Y%m%d')

    return(df)


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

def data_inter(dico):
    """
    Crée une dataframe adaptée

    Args : 
        dico : dictionnaire qui est retourné par query et dont les clés sont des années et les valeurs
        sont les données, sous forme de dataframe, correspondantes à la saison

    Returns :
        dfinter : la dataframe adaptée pour la figure 4 avec pour colonnes :
        'Year', '2PT Field Goal','3PT Field Goal'
    """
    l2pt =[]
    l3pt = []
    lyear = []
    for year, dataf in dico.items():
        value_count = dataf['SHOT_TYPE'].value_counts()
        l2pt = np.append(l2pt,value_count[0]).astype(int)
        l3pt = np.append(l3pt,value_count[1]).astype(int)
        lyear = np.append(lyear,year).astype(int)

    s2pt = pd.Series(l2pt)
    s3pt = pd.Series(l3pt)
    syear = pd.Series(lyear)
    dfinter = pd.concat([syear,s2pt,s3pt],keys=['Year', '2PT Field Goal','3PT Field Goal'],axis=1)

    return dfinter

url = 'https://www.basketball-reference.com/leagues/NBA_2018_totals.html'

df_url = url_scraper(url)
df_url = clean_data_html(df_url)
df_url = convert_data_html(df_url)

dfsorted = top_ten(df_url,'PTS')
fig = histo(dfsorted,'Player','PTS','Points en fonction des top 10 joueurs')
fig2 = histo(df_url,'Pos','FG','Paniers marqués en fonction de la position')

df_csv = pd.read_csv('csv_geoloc.csv',delimiter = ';')
df_csv = clean_data_csv(df_csv)
df_csv = convert_data_csv(df_csv)

dicolebron={}
dicolebron = prep_query(dicolebron,df_csv)

fig3 = px.scatter(dicolebron[2003],x='LOC_X',y='LOC_Y',color='SHOT_ZONE_BASIC',title='Terrain de basket avec la géolocalisation de chaque panier marqués')
fig3 = trace_terrain(fig3)

dfinter = data_inter(dicolebron)

fig4 = px.line(dfinter,x='Year',y='2PT Field Goal',title='Evolution des shots en fonction des années')

app = Dash(__name__)
app.layout = html.Div(children=[

    html.H1(children='NBA Dashboard', style={'text-align':'center','font-family':'Arial'}),

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
            {'label':'3PTS', 'value':'3PT Field Goal'},
            {'label':'2PTS', 'value':'2PT Field Goal'},
        ],
    ),

    dcc.Graph(
        id='graph4',
        figure=fig4
    ),

    html.Div(children='''
            Description of the graph above. Mouse over for details
    ''',
    style={'font-family':'Arial'}),
])

@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Output(component_id='graph3', component_property='figure'),
    Output(component_id='graph4', component_property='figure'),
    Input(component_id='point-checklist', component_property='value'),
    Input(component_id='point-checklist2', component_property='value'),
    Input(component_id='years-slider', component_property='value'),
    Input(component_id='point-checklist3', component_property='value'),
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
    fig3 = px.scatter(
        dicolebron[input_value3],
        x='LOC_X',
        y='LOC_Y',
        color='SHOT_ZONE_BASIC',
        title='Terrain de basket avec la géolocalisation de chaque panier marqués',
    )
    trace_terrain(fig3),

    fig4 = px.line(
        dfinter,
        x = 'Year',
        y = input_value4,
        title='Evolution des type de shots en fonction des années',
    )
    return fig,fig2,fig3,fig4

if __name__ == '__main__':
    app.run_server(debug=True) # RUN APP


end = time.time() 

print('execution time :',(end-start), "s")