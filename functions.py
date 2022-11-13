import pandas as pd
import numpy as np

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
    + création de colonnes associées au points par type de shot

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