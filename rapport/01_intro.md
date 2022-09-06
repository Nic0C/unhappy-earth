# UnhapPy Earth

Étude de cas : Analyse du réchauffement climatique. 

# Introduction

En quelques décennies à peine, la question du réchauffement climatique est devenu un sujet majeur, inquiétant pour l'avenir de la planète et de sa biodiversité, y compris l'espèce humaine. Pourtant il fait débat, oppose experts et "climato-sceptiques", à l'heure même ou les manifestations de ce changement sont de plus en plus flagrants.

Notre objectif est de proposer, à l'aide de données fiables et librement accessibles sur internet, une analyse du réchauffement climatique, en répondant notamment aux problématiques suivantes :

- Pouvons-nous confirmer grâce à ces données le phénomène de changement climatique ? Le réchauffement est-il réellement observable ?
- Quand le phénomène apparaît-il ? De manière soudaine ou graduelle ? Au même moment sur l’ensemble du globe ?
- Son évolution est-elle uniforme à travers le monde ou certaines zones sont-elles plus impactées que d’autres ?
- Les émissions de CO2 dans l'atmosphère seraient, parmi l’ensemble des gaz à effet de serre, la principale cause du réchauffement de la planète. Existe-t-il une forte corrélation entre les émissions de CO2 et l’évolution des températures ?
- Des événements historiques ont-ils eu un impact sur l'évolution de la température ?
- Quelles sont nos prédictions de température sur les prochaines années ?
- Nos conclusions sont-elles similaires à celles des scientifiques - climatologues ? 

Pour ce faire, nous allons :
- Analyser de manière approfondie les données en rapport avec nos questions de recherche ;
- Produire des représentation graphiques afin de mieux visualiser les données, et confirmer ou orienter des intuitions ;
- Construire des modèles de régression et de prédiction.

# Environnement et outils de travail

## Utilisation de Google Drive & Colaboratory

Afin de travailler ensemble, à distance mais de manière collaborative, nous avons créé pour le projet un compte Google, bénéficiant ainsi d'un Google Drive commun, sur lequel nous avons pu importer les jeux de données nécessaires à notre étude et sauvegarder l'avancement de nos travaux. Les Notebooks ont été réalisés sur Google Colaboratory, en liaison avec notre Google Drive pour plus de facilité en imports et sauvegardes.

## Packages

La totalité des notebooks a été codée en langage Python, à l'aide des packages et sous-packages suivants :

| Package     	| Sous-package   	| Fonction    	   | Utilisation  	|
|---	          |---	            |---	             |---	          |
| pandas        |   	            |   	             | Création et manipulation de DataFrames |
| numpy   	    |                	|             	   | Fonctions mathématiques  	|
| matplotlib    |                	|           	     | Visualisations (graphiques, colorisation 	|
| seaborn  	    |               	|              	   | Visualisations (heatmap)  	|
| re            |                 |                  | Expressions régulières pour extraction de données depuis fichiers textes |
| GeoPandas  	  |               	|             	   | Données géospatiales et représentations cartographiques 	|
| pycountry  	  |               	|             	   | Base de données ISO pour les codes pays |
| mapclassify   |               	|            	     | Classification cartographique  	|
| SciPy  	      | stats         	| pearsonr  	     | Tests de corrélation  	|
| Scikit-learn  | linear_model  	| LinearRegression | Modèle de régression lineaire  	|
| Scikit-learn 	| metrics       	| r2_score  	     | Evaluation du modèle de régression linéaire  	|
| FB prophet    | Prophet       	|                  | Analyse et prédictions de séries temporelles  	|
| warnings    	|               	|           	     | Allègement visuel des NoteBooks en empêchant l'affichage des messages d'avertissement  	|

## Fonctions

Test d'image

![Graphique](images/103_Plot_evo_temp_par_mois.png)


## Questions de recherche


