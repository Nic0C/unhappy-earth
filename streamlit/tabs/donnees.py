import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


title = "Données utilisées"
sidebar_name = "Données"

plt.style.use('seaborn-whitegrid')


def read_temps():
    globales = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    hemispheres = pd.read_csv('data/unhappy_earth/temperatures_hemispheres.csv')
    countries = pd.read_csv('data/unhappy_earth/temperatures_countries.csv')
    return globales, hemispheres, countries

def read_co2():
    globales = pd.read_csv('data/unhappy_earth/co2_global.csv')
    countries = pd.read_csv('data/unhappy_earth/co2_countries.csv')
    return globales, countries


def run():

    st.title(title)

    temps_globales, temps_hemis, temps_countries = read_temps()
    temps_countries_10y = pd.concat([temps_countries['year'], temps_countries.iloc[:,2:].rolling(120).mean()], axis=1)

    co2_global, co2_countries = read_co2()
    co2_countries_10y = pd.concat([co2_countries['year'], co2_countries.iloc[:,2:].rolling(120).mean()], axis=1)
    
    st.header('Identification des sources')
    
    st.markdown(
        """
Nous avons identifié deux sources de données pour nos recherches : [Berkeley Earth](http://berkeleyearth.org/data/) 
et [Our world in data](https://ourworldindata.org/). Toutes nos données sont publiquement téléchargeables, sous une 
licence spécifique pour le premier et [CC-BY](https://creativecommons.org/licenses/by/4.0/legalcode) pour le second. 
        """)
        
    with st.expander("En savoir plus sur les sources de données..."):
        st.markdown(
        """
[Berkeley Earth](http://berkeleyearth.org/data/) est une organisation américaine indépendante qui fournit des données 
de température historiques nettoyées et cross-vérifiées. Recoupant elle-même plusieurs sources, notamment l'analyse 
[GISTEMP](https://data.giss.nasa.gov/gistemp/) réalisée sous l'égide de la NASA, elle fournit un ensemble de jeux de 
données actualisés, les mesures vont jusqu'à 2021, et complets, avec plus de 19 millions d’observations depuis 46 000 
stations météo.

[Our world in data](https://ourworldindata.org/) est un organisme reconnu pour la qualité de leurs publications de 
données sur un ensemble de sujets d'actualité tels que la pollution, la santé ou la population. Leurs données sont 
librement [téléchargeables sur GitHub](https://github.com/owid/), et sont notamment utilisées pour [l'enseignement 
et la recherche](https://ourworldindata.org/coverage) à travers le monde. Nous nous appuyons sur leurs données 
d'émission de CO2 disponibles dans [leur référentiel GitHub](https://github.com/owid/co2-data).
        """
        )

    st.header('Données de températures')

    st.markdown(
        """
Les jeux de données de Berkeley Earth sont fournis sous forme de fichiers .txt, chacun d’entre eux correspondant 
à une région (totalité du globe, par hémisphère ou par pays). La fréquence d'échantillonnage est mensuelle.

Ils sont tous construits de la même manière, avec en en-tête une **description complète**, incluant un élément 
crucial : une liste de 12 températures de _référence absolues mensuelles_ et leur incertitude sur une période 
fixe de 30 ans, de janvier 1951 à décembre 1980. Cette période a été retenue d'une part pour la fiabilité et 
la complétude des observations effectuées, mais également car elle représente une sorte de médiane sur l'ensemble 
du dataset. Ensuite, un **tableau donne le détail des résultats** moyens sous forme d’_anomalies_, ou _températures 
relatives_, assorties de leur incertitude, observées par mois pour la région donnée, pour une période allant de 
1750 au plus tôt, et jusqu’en 2021. 

L’**anomalie de température** est une valeur relative, exprimée en degrés Celsius correspondant à l’écart, 
positif ou négatif, entre la température mesurée et la température moyenne de référence correspondante. Plus 
d'informations concernant ce mesurement et l'intérêt de raisonner en termes d'anomalies peut être trouvé [sur le 
site de la NASA](https://data.giss.nasa.gov/gistemp/faq/abs_temp.html). 

L’**incertitude** est la dispersion liée à différents facteurs, notamment de sous-échantillonnage statistique et 
spatial, influant in fine sur la qualité de la mesure. Elle représente l'intervalle de confiance à 95 %. **Ces 
références nous permettent de calculer les températures en valeurs absolues.**
        """
    )

    tab1, tab2, tab3, tab4 = st.tabs(["Complete_TAVG_complete.txt", 
                                      "northern-hemisphere-TAVG-Trend.txt", 
                                      "southern-hemisphere-TAVG-Trend.txt",
                                      "Sets_by_country"])

    with tab1:
       st.dataframe(temps_globales.tail(10))
    
    with tab2:
       st.header("A dog")
       st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
    
    with tab3:
       st.header("An owl")
       st.image("https://static.streamlit.io/examples/owl.jpg", width=200)
   
    st.markdown(
        """
| Nom |  Type  |  NaNs  |  Description  |  Exemple  |  Moyenne  |  Min  |  Max  |
|---|---|---|---|---|---|---|---|
| date |  datetime  |  0  |  Date au format yyyy-mm-dd.  |  1950-12-24  |  X  |  X  |  X  |
| year |  int  |  0  |  L'année au format xxxx.  |  1950  |  X  |  X  |  X  |
| month |  int  |  0  |  Le mois au format numérique.  |  120  |  X  |  X  |  X  |
| ano |  float  |  1  |  Anomalie constatée (°C).  |  0.122  |  -0.265  |  -6.018  |  5.531  |
| uncert |  float  |  3  |  Incertitude (°C).  |  0.041  |  0.903  |  0.022  |  6.521  |
|  abs  |  float  |  1  |  Température absolue (°C).  |  13.124  |  8.329  |  -2.423  |  17.780  |

Les données sont réparties sur 12 colonnes :
* Les quatre premières colonnes fournissent les informations suivantes : l’année, le mois de l’année, l’anomalie
  de température moyenne estimée pour ce mois et son incertitude.
* Les huit dernières colonnes rapportent les anomalies et incertitudes sous la forme de moyennes glissantes 
  annuelles, quinquennales, décennales et vicennales, centrées sur le mois considéré. Par exemple, la moyenne 
  annuelle de janvier à décembre 1950 est rapportée à juin 1950, ce qui explique la présence de « NaNs » en début et 
  fin de ces colonnes dans les Data Sets.

Les fichiers que nous utilisons pour nos analyses ont tous été récupérés sur le site de Berkeley Earth, et sont les 
suivants :
* Températures globales :
  - `Complete_TAVG_complete.txt` : liste des températures globales moyennes sur terre.
* Températures par hémisphères :
  - `northern-hemisphere-TAVG-Trend.txt` : liste des températures moyennes par hémisphère (nord)
  - `southern-hemisphere-TAVG-Trend.txt` : liste des températures moyennes par hémisphère (sud)
* Températures par pays :
  - `Sets_by_country` : liste des températures moyennes par pays.
        """
    )
      
    # Add country selection
    options = st.multiselect(
        'Sélectionner un pays',
        temps_countries.columns,
        ['france', 'united-states-of-america', 'china'],
        key = "temps_countries")

    if len(options) == 0 : 
        st.markdown("Attention : Selectionner au moins un pays !")
    else :
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(temps_countries_10y['year'], temps_countries_10y[options], label=options)
        ax.set_ylim(bottom=0)
        ax.grid(visible=True, alpha=0.5)
        ax.legend(loc='lower left')
        ax.set_title("Températures par pays, moyenne sur 10 ans")
        st.pyplot(fig=fig, )
        
        
    st.header('Données de dioxyde de carbone')

    st.markdown(
        """
Nous identifions deux jeux de données pour le CO2 : le premier est la quantité totale produite par pays et par an, 
l'autre détaille les émissions dues à la production industrielle et à l'utilisation des sols, tous pays confondus 
et par an.

Les pays sont identifiés par leur trigramme ISO 3166 - alpha-3, et comme pour les températures, les données peuvent 
manquer en fonction des années et des pays. 
        """
    )
    
    # Add country selection
    options = st.multiselect(
        'Sélectionner un pays',
        co2_countries.columns,
        default=['FRA', 'USA', 'CHN', 'OWID_WRL'],
        key="co2_countries")

    if len(options) == 0 : 
        st.markdown("Attention : Selectionner au moins un pays !")
    else :
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(co2_countries['year'], co2_countries[options], label=options)
        ax.set_ylim(bottom=0)
        ax.grid(visible=True, alpha=0.5)
        ax.legend(loc='lower left')
        ax.set_title("Production de CO2 par pays, par an")
        st.pyplot(fig=fig)
        
    st.markdown(
        """
Les **données de CO2 globales** nous fournissent une autre information : la quantité de CO2 émise par l’utilisation 
des terres, en plus de la génération de CO2 liée à la production d'énergie et industrielle. Les terres, en fonction 
de leur utilisation, produisent une certaine quantité de CO2 qui vient s’ajouter à la production industrielle ; dans 
certains cas elles peuvent aussi en consommer, et nous pouvons avoir des valeurs négatives sur cette mesure.
        """
    )

    st.header('Lecture et pré-traitement des données')

    st.markdown(
        """

Les données de température sont fournies sous forme de fichiers txt, et doivent être pré-traitées afin d’en extraire les mesures de 
références et calculer les valeurs de température absolues. Nous avons écrit une fonction Python qui prend soin de lire les fichiers 
et retourne des datasets Pandas formatés de la même manière, incluant les valeurs d’anomalie et de température absolue.

|     Nom    |  Type  |  NaNs |                                        Description                                       |   Exemple   |  Moyenne  |    Min    |    Max    |
|:----------:|:------:|:-----:|:----------------------------------------------------------------------------------------:|:-----------:|:---------:|:---------:|:---------:|
| year       | int    | 0     | L'année au format xxxx.                                                                  | 1950        | X         | X         | X         |
| ico_code   | object | 4029  | Code ISO du pays.                                                                        | AFG         | X         | X         | X         |
| country    | object | 0     | Dénomination usuelle du pays.                                                            | Afghanistan | X         | X         | X         |
| co2        | float  | 1319  | Quantité de CO2 émise (millions de tonnes)                                               | 5.333       | 326.658   | 0         | 36702.503 |
| gpd        | float  | 12520 | Produit Intérieur Brut ($).                                                              | 3.045e+10   | 2.89e+11  | 5.543e+07 | 1.136e+14 |
| population | float  | 3097  | Population du pays.                                                                      | 4.87e+06    | 7.068e+07 | 1490      | 7.795e+09 |
| total_ghg  | float  | 20338 | Quantité totale de gaz à effet de serre émise, en équivalent deCO2 (millions de tonnes). | 33.9        | 420.52    | -178.71   | 48939.71  |
        """
    )

    st.subheader('Lecture et pré-traitement des données')

    st.markdown(
        """
La plupart des jeux de données lus incluent des NaNs ; nous les identifions et décidons de leur maintien ou 
de leur remplacement au cas par cas.
* Pour les **températures globales**, il est rare qu’aucun capteur ne soit disponible au niveau planétaire et 
  les quelques NaNs sont présents en tout début de jeu, dans les années 1751/1752. Nous en identifions seulement 
  3 lignes, non-consécutives, et décidons de les remplacer par interpolation linéaire. 
* Pour les **températures par hémisphère**, il y a une seule valeur manquante sur l’hémisphère nord et 2 sur 
  l’hémisphère sud. Nous utilisons encore une fois une interpolation linéaire pour remplacer ces valeurs en 
  s’appuyant sur leur continuité. Il faut noter également que la date de début de collecte est différente entre 
  les deux jeux de données, dès 1840 pour le Nord et à partir de 1880 pour le Sud. 
* Pour les températures par hémisphère toujours, nous calculons également une moyenne glissante sur 12 mois, 
  qui permet de lisser les variations saisonnières et d’obtenir des courbes plus lisibles. 
* Pour les **températures par pays**, les mesures sont souvent manquantes - lorsque les capteurs ont été 
  installés tardivement, ou lors de périodes d’instabilité géopolitique. Pour ces raisons les NaNs se 
  répartissent sur de grandes plages de temps – correspondant par exemple à la durée d’une guerre ou la mise en 
  autarcie d’un pays. Nous ne pouvons donc utiliser d’interpolation pour les remplacer et décidons de les conserver 
  tels quels. 

Les **informations de CO2 par pays** sont disponibles en format CSV ; comme pour le dataset précédent des 
températures par pays, les valeurs manquantes sont liées à des périodes où le pays, pour quelque raison que ce soit, 
n'a pas pu collecter les données. Ces trous représentent des plages de temps importantes, et nous les laisserons 
tels quels pour ne pas compromettre l'intégrité statistique des données.
        """
    )

    st.subheader('Agrégation des données')

    st.markdown(
        """
Les informations par hémisphère et par pays sont fournies dans des fichiers distincts (par hémisphère dans le premier cas, et par pays dans le second). Nous souhaitons les rassembler afin d’obtenir les données semblables (par hémisphère, par pays) en un jeu de données unique, plus facile à manipuler, analyser et visualiser. 

Les **températures par hémisphère** contiennent à la fois les données sud et nord sur la plus grande période possible (i.e. à partir de 1840). Cela introduit un grand nombre de NaNs pour les 40 premières années, les mesures ayant commencé plus tard dans l’hémisphère sud. Comme cela représente une grande plage de temps, nous ne pouvons les remplacer sans introduire de biais et décidons donc de les conserver telles quelles. 

Les températures par pays rassemblent les données de température de 188 pays, sur la même période de temps (de 1740 pour les premières mesures à 2020). Comme on peut s’y attendre, cela introduit un grand nombre de NaNs pour les pays qui ont commencé la collecte après la date de début du jeu. Les pays les plus complets sont ceux d’où est partie l’initiative de mesure et sont principalement européens. A l’inverse, les pays en voie de développement, non-habités ou non-vivables (e.g. l’antartique) ont beaucoup moins de mesures disponibles.


        """
    )
