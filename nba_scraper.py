import pandas as pd
import numpy as np
import time
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, html, dcc, Input, Output


start = time.time()

# on recupère les données du site
url = 'https://www.basketball-reference.com/leagues/NBA_2018_totals.html'
df = pd.read_html(url,flavor='lxml')[0]

# on commence à nettoyer la df pour avoir l'essentiel

# on supp les lignes qui reprennent le nom des colonnes en plein milieu
asup = df[df['Rk']=='Rk']
df.drop(asup.index, axis=0,inplace=True)

# on drop les colonnes de rebonds ect...
df.drop(df.columns[[0,6,21,22,23,24,25,26,27,28]],axis=1,inplace=True)

# on drop les duplicates
df = df.drop_duplicates(subset=['Player'])

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

# quelques caractéristiques de la df clean
# print(df.dtypes)
# print(df.describe())
# print(df)s
# csv_data = df.to_csv('csv_data_2018_clean.csv',encoding = 'utf8',index=False)

# on affiche les 10 meilleurs joueurs de la saison selon différents critères
dfsorted = df.sort_values(by=['PTS'],ascending=False).head(10)
# print(dfsorted)

# histogrammes avec plotly express et plotly go

fig = px.histogram(dfsorted, x='Player',y='PTS',histfunc='sum',title='Top 10 Players by Points')

fig2 = px.histogram(df, x='Pos',y='FG',histfunc='sum',title='Points scored by players per Position')

fig5 = go.Figure()
fig5.add_trace(go.Histogram(
    x=dfsorted['Player'],
    y=dfsorted['3PTS'],
    histfunc='sum',
    name='3P'
    ))

fig5.add_trace(go.Histogram(
    x=dfsorted['Player'],
    y=dfsorted['2PTS'],
    histfunc='sum',
    name='2P'
    ))

fig5.add_trace(go.Histogram(
    x=dfsorted['Player'],
    y=dfsorted['FT'],
    histfunc='sum',
    name='FT'
    ))
fig5.update_layout(
    title_text='Top 10 players with proportion of 3, 2 and free throws points made',
    xaxis_title_text='Player',
    yaxis_title_text='Field goals',
    barmode='stack'
)
# fig.update_traces(opacity=0.75)
# fig5.show()


# dashboard
# visit http://127.0.0.1:8050/ in your web browser.
# app = dash.Dash() # On crée une instance de la classe Dash
app = Dash(__name__)

# layout
app.layout = html.Div(children=[

    html.H1(children='NBA Dashboard'),

    html.Label('Type of field goals : '),

    # my input 
    dcc.Checklist(
        id='point-checklist',
        options=[
            {'label':'3P (3-Points Field Goals)', 'value':'3PTS'},
            {'label':'2P (2-Points Field Goals)', 'value':'2PTS'},
            {'label':'FT (Free Throws)', 'value':'FT'},
            # {'label':'PTS (Points)', 'value':'PTS'}
        ],
    ),

    # my output : the Graph figure = fig
    dcc.Graph(
        id='graph1',
        figure=fig
    ),

    dcc.Checklist(
        id='point-checklist2',
        options=[
            {'label':'3P (3-Points Field Goals)', 'value':'3PTS'},
            {'label':'2P (2-Points Field Goals)', 'value':'2PTS'},
            {'label':'FT (Free Throws)', 'value':'FT'},
            # {'label':'PTS (Points)', 'value':'PTS'}
        ],
    ),

    dcc.Graph(
        id='graph2',
        figure=fig2
    ),

    html.Div(children='''
            Description of the graph above. Mouse over for details
    '''),
])

# callback pour update nos données en fonction des cases cochées ect...
@app.callback(
    Output(component_id='graph1', component_property='figure'),
    Output(component_id='graph2', component_property='figure'),
    Input(component_id='point-checklist', component_property='value'),
    Input(component_id='point-checklist2', component_property='value'),
)

def update_figure(input_value,input_value2):
    fig = px.histogram(
        dfsorted, 
        x='Player',
        y= input_value,
        histfunc='sum',
        title='Top 10 Players by type of points'
    ) 
    fig2 = px.histogram(
        df, 
        x='Pos',
        y= input_value2,
        histfunc='sum',
        title='Type of Goals made by Position'
    ) 
    return fig, fig2

if __name__ == '__main__':
    app.run_server(debug=True) # RUN APP

end = time.time() 

print('execution time :',(end-start), "s")