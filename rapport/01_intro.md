# UnhapPy Earth

Étude de cas : Analyse du réchauffement climatique. 

# Introduction

En quelques décennies à peine, la question du réchauffement climatique est devenu un sujet majeur, inquiétant pour l'avenir de la planète et de sa biodiversité, y compris l'espèce humaine. Pourtant il fait débat, oppose experts et "climato-sceptiques", à l'heure même où les manifestations de ce changement sont chaque jour plus flagrantes.

Notre objectif est de proposer, à l'aide de données fiables et librement accessibles sur internet, une analyse de ce phénomène, en répondant notamment aux problématiques suivantes :

- Pouvons-nous confirmer grâce aux données le phénomène de changement climatique ? Le réchauffement est-il réellement observable ?
- Quand le phénomène apparaît-il ? De manière soudaine ou graduelle ? Au même moment sur l’ensemble du globe ?
- Son évolution est-elle uniforme à travers le monde ou certaines zones sont-elles plus impactées que d’autres ?
- D'après la grande majorité des experts en climatologie, les émissions de CO2 dans l'atmosphère seraient, parmi l’ensemble des gaz à effet de serre, la principale cause du réchauffement de la planète. Quel degré de corrélation exis-t-il entre les émissions de CO2 et l’évolution des températures ?
- Des événements historiques ont-ils eu un impact sur l'évolution de la température ?
- Quelles sont nos prédictions de températures sur les prochaines années ?
- Par cette Data Analyse, parvenons nous à des conclusions similaires à celles des scientifiques - climatologues ? 

Pour ce faire, nous allons :
- Importer et analyser de manière approfondie les données en rapport avec nos questions de recherche ;
- Produire des visualisations graphiques afin de "faire parler" les données, et éventuellement, orienter ou confirmer des intuitions ;
- Construire des modèles de régression et de prédiction.

# Environnement et outils de travail

## Utilisation de Google Drive & Colaboratory

Afin de travailler ensemble, à distance mais de manière collaborative, nous avons créé pour le projet un compte Google, bénéficiant ainsi d'un Google Drive commun, sur lequel nous avons pu importer les jeux de données nécessaires à notre étude et sauvegarder l'avancement de nos travaux. Les Notebooks ont été réalisés sur Google Colaboratory, en connexion avec notre Google Drive, facilitant les imports et sauvegardes.

## Packages

La totalité du code est en langage Python, utilisant les packages et sous-packages suivants :

| Package     	| Sous-package | Fonction spécifique | Utilisation  	                                          |
|---	          |---	         |---	                 |---	                                                      |
| pandas        |   	         |   	                 | Création et manipulation de DataFrames                   |
| numpy   	    |              |             	       | Fonctions mathématiques  	                              |
| matplotlib    |              |           	         | Visualisation (graphiques, colorisation)               	|
| seaborn  	    |              |              	     | Visualisation (heatmap)                                	|
| re            |              |                     | Expressions régulières pour extraction de données        |
| GeoPandas  	  |              |             	       | Données géospatiales et représentations cartographiques 	|
| pycountry  	  |              |             	       | Base de données ISO (codes pays)                         |
| mapclassify   |              |            	       | Classification cartographique  	                        |
| SciPy  	      | stats        | pearsonr  	         | Tests de corrélation  	                                  |
| Scikit-learn  | linear_model | LinearRegression    | Modèle de régression lineaire  	                        |
| Scikit-learn 	| metrics      | r2_score  	         | Evaluation du modèle de régression linéaire  	          |
| FB prophet    | Prophet      |                     | Analyse et prédictions de séries temporelles           	|
| warnings    	|              |           	         | Non-affichage des messages d'avertissement  	            |

## Définition de fonctions

Afin "d'alléger" les NoteBooks en évitant de répéter des lignes de codes similaires, nous avons définis quelques fonctions :

- Fonction `read_txt_file` :  permet de lire un fichier texte de mesures, de récupérer les températures de références et anomalies, puis de calculer les valeurs de températures absolues. 
- Fonction `plot_month` : permet d'afficher un graphique montrant l'évolution des températures par mois, pour un DF donné, ainsi que leur moyenne glissante sur 12 mois.
- Fonction `plot_year` : permet d'afficher un graphique montrant l'évolution des températures par an, pour un DF donné, avec ou sans la marge d'incertitude associée.
- Fonction `mult_plot_year` : permet d'afficher côte-à-côte deux graphiques montrant l'évolution des températures par mois, pour deux DF (deux régions) donnés.
