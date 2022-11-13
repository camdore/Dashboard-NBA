# Projet NBA 

Ce projet python permet de visualiser des statistiques sur la saison 2017-2018 de NBA, ainsi que sur la carrière de Lebron James entre 2003 et 2017.
## Présentation du sujet

Pour cela nous avons utilisé 2 sets de données : un set pour la saison 2017-2018 et un autre pour la géolocalisation des tirs de Lebron James entre 2003 et 2017. Notons que pour le dataset de Lebron James ne sont pas renseigné les saisons 2010-2011 à 2013-2014.

Une fois l’application lancée vous aurez accès aux données sur les différents types de tirs que ce soient des tirs à 3 points, 2points, lancer franc, leur pourcentage de réussite ou encore leur localisation.

## User Guide 

Ci-dessous les instructions et les précautions nécessaires pour faire tourner l’application dans de bonnes conditions.

### Prérequis 

Vous devez d’abord vous assurer d’avoir la dernière version de Python installée sur votre machine. 
Si ce n’est pas le cas vous pouvez suivre les instructions d'installation [ici](https://www.python.org/downloads/).

Pour s’assurer que toutes les librairies suivantes soient installées sur votre machine exécuter la commande suivante : 
> ` $ python -m pip install -r requirements.txt `

### Installation 

Pour installer l’application effectuer l’instruction suivante : 
> ` $ git clone https://git.esiee.fr/amouzoue/projetnba `

Pour lancer l’application sur Windows taper l’instruction suivante depuis le terminal : 
> ` $ cd /path /projetnba `
>
> ` $ python main.py `

Pour lancer l’application sur Linux/MacOS taper l’instruction suivante depuis le terminal : 
> ` $ cd /path /projetnba `
>
> ` $ python3 main.py `

L’application Dashboard tourne sur n'importe quel navigateur à l’adresse suivante : http://127.0.0.1:8050/

### Utilisation
L'utilisateur peut cocher les différentes cases et filtres à disposition. Il peut également passer la souris sur les graphiques pour avoir des informations numériques sur les graphiques.

## Developper Guide 

### Arbre du projet

    projet-python/ 

    |-- requirements.txt 

    |-- csv_geoloc.csv 

    |-- main.py 

    |-- README.md 

### Fonctions des différents fichiers 

requirement.txt contient les instructions pour installer les librairies nécessaires.

csv_geoloc.csv contient les données pour les saisons 2003 à 2017 de Lebron James.

### Copyright

Je déclare sur l’honneur que le code fourni a été produit par moi/nous même, à l’exception des lignes ci dessous.

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

La fonction ellipse_arc vient du site suivant : https://community.plotly.com/t/arc-shape-with-path/7205/5 .

Parce que  dans la fonction add_shape() le paramètre path n'accepte pas les arcs de cercle (A) (doc officielle).

## Rapport d'analyse

### La saison 2017-2018




### Carrière de Lebron James


### Conclusion 

## Auteurs 
Camille Doré et Thomas Ekué 