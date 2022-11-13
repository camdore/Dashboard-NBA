# Projet NBA

Ce projet R permet de visualiser des statistiques sur la saison 2017-2018 de NBA, ainsi que sur la carrière de Lebron James entre 2003 et 2017.

## Présentation du sujet

Pour cela nous avons utilisé 2 sets de données : un set pour la saison 2017-2018 et un autre pour la géolocalisation des tirs de Lebron James entre 2003 et 2017. Notons que pour le dataset de Lebron James ne sont pas renseigné les saisons 2010-2011 à 2013-2014.

Une fois l’application lancée vous aurez accès aux données sur les différents types de tirs que ce soient des tirs à 3 points, 2points, lancer franc, leur pourcentage de réussite ou encore leur localisation.

## User Guide 

Ci-dessous les instructions et les précautions nécessaires pour faire tourner l’application dans de bonnes conditions.

### Prérequis 

Vous devez d’abord vous assurer d’avoir la dernière version de R installée sur votre machine. 
Si ce n’est pas le cas vous pouvez suivre les instructions d'installation [ici](https://cran.r-project.org/bin/windows/base/). Puis vous passez à l'istallation de l'environnement d’édition et d’exécution standard nommé Rstudio dont les instruction d'installations sont renseignées [ici] (https://posit.co/download/rstudio-desktop/)

Assurez-vous d'installer les librairies suivantes par les commander:

    >install.packages(tidyr)
    >install.packages(ggplot2)
    >install.packages(dplyr)
    >install.packages(lubridate)
    >install.packages(jpeg)
    >install.packages(RCurl)
    >install.packages(shinythemes)
    >install.packages(grid)
    >install.packages("devtools")


### Installation 

Pour installer l’application effectuer les instructions suivantes dans votre Git Bash: 

    $ cd Downloads
    $ git clone https://git.esiee.fr/amouzoue/projetnba/projet-R

### Utilisation

Pour lancer l’application dans Rstudio ouvrez les fichers ui.R et server.R et cliquez sur 'Run App' : 

L'utilisateur peut cocher les différentes cases et filtres à disposition.

## Developper Guide 

### Arbre du projet

    projet-R/ 

    |-- assets
        |--positions_basket.jpg
        
    |-- ui.R 
    |-- server.R
    |-- lebron_geoloc_clean.csv
    |-- csv_data_2018_clean.csv
    |-- README_R.md 

### Fonctions des différents fichiers

lebron_geoloc_clean.csv contient les données nettoyées pour les saisons 2003 à 2017 de Lebron James.

csv_data_2018_clean.csv contient les données nettoyées des jouers de la NBA pour les saison 2003 à 2017.

ui.R contient les informations de l'interface utilisateur definissant l'aspect graphique du front end de l'application.

server.R contient le lignes de code pour la préparations des données et la construction des output correspondant aux interactions détectées sur l'ui.

positions_basket.jpg est l'image qui vous permmettra réconnaitre le zones d'un terrain de basket.

### Copyright

Je déclare sur l’honneur que le code fourni a été produit par moi/nous même, à l’exception des lignes ci dessous.

        courtImg.URL <- "https://thedatagame.files.wordpress.com/2016/03/nba_court.jpg"
        court <- rasterGrob(readJPEG(getURLContent(courtImg.URL)),
                    width=unit(1,"npc"), height=unit(1,"npc"))

Suite à des difficultés due aux proportions et à la positions du tracés par rapport aux points cette solution à été privilégié pour le tracé des lignes du terrain. Source : https://thedatagame.com.au/2015/09/27/how-to-create-nba-shot-charts-in-r/

## Rapport d'analyse

### Présentaion

Ce projet à pour but de visualiser des données sur les types de tirs effectués lors de la saison 2017-2016. Il à également pour but d'observer l'évolution du jeu en NBA sur les 10 dernières années à travers les données d'un des meilleurs joueur de l'histoire de la NBA : Lebron James.

### La saison 2017-2018

![Positions des joueurs sur un terrain de basket](/assets/positions_basket.jpg)

Premier onglet de l'application:

À l'aide de deux graphique nous découvrons que les 10 meilleurs joueurs marquent en général beaucoup plus de paniers à 2 points que de paniers 3 points. Seul James Harden à un nombre de 3 points plus élevé que les 2 points. La proportion de lancer francs ("Free Throws") est très petite ce qui est normale puisque ces tirs sont accordés après une faute, et non marqués dans le jeu.

Deuxièmre onglet de l'application:

Sur le 2e graphique nous voyons que le type de points marqués dépend de la position des joueurs. Ainsi nous observons que les paniers à 3 points sont marqués en majorité par les Shooting Guard (SG) et les Point Guard(PG). Ce qui est logique puisqu'ils sont placés au bord de la ligne des 3 points. Pour les paniers à 2 points ils sont inscrits en majorité par les Center (C) qui sont placés au abord du panier. Les lancers francs ne sont pas influencés par la postion et dépendent uniquement de l'adresse du joueurs qui les tire.

Troisième onglet de l'application:

Sur le 3e graphique nous voyons que l'efficicaté des tirs ne change pas malgré l'âge contre ce que l'on auraot pu penser, tout comme le nombre de paniers tentés. Nous remarquons cependant une anomalie pour les joueurs de 39 ans. Cela est expliqué par le fait qu'il n'y en a qu'un seul donc la moyenne est faussée.

### Carrière de Lebron James

Quatrième onglet de l'application:

La principal évolution à lieu sur le fait que la zone Mid-Range est délaissée au fil des années. Lebron James marque de plus en plus derrière la ligne des 3 points malgré sa position de Power Forward ou Small Forward qui est proche du panier. Bien sur il garde quand même une concentration importante de tirs dans les zones proches du panier. Cela est confirmé par le graphique en dessous avec le nombre de 3 point qui fini par dépasser le nombre de tirs dans la Mid-Range.

### Conclusion 

Nous voyons que la manière de jouer a évolué au cours des années en NBA. Le rôle de chacun malgré des positions similaires a changer entre 2003 et 2018.

## Auteurs 

Camille Doré et Thomas Ekué Amouzouglo