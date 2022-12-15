import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


title = "Data sources"
sidebar_name = "Data sources"

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
    
    st.header('Identifying data sources')
    
    st.markdown(
        """
We identified two data sources for our research: [Berkeley Earth](http://berkeleyearth.org/data/)
and [Our world in data](https://ourworldindata.org/). The datasets provided are all publicly available, under a
specific license for the first and under the [CC-BY](https://creativecommons.org/licenses/by/4.0/legalcode) for the second.
        """)
        
    with st.expander("More about the data sources"):
        st.markdown(
        """
[Berkeley Earth](http://berkeleyearth.org/data/) is an independent American organization that provides curated and cross-validated historic temperature datasets. They rely on a variety of other data sources, including the well-known [GISTEMP](https://data.giss.nasa.gov/gistemp/) datasets published by the NASA, and provide complete and up-to-date datasets that go up to 2021. The overall dataset contains more than 19 million observations from 46,000 weather stations spread across the world.

[Our world in data](https://ourworldindata.org/) is a well-established organization providing datasets and visualisations about a range of recent hot topics, from pollution to public health and worldwide population. Their datasets are freely [available on GitHub](https://github.com/owid/), and are commonly used in [teaching and research](https://ourworldindata.org/coverage) around the world. We specifically use their $CO_2$ emission dataset, as published in [their dedicated GitHub repository](https://github.com/owid/co2-data).
        """
        )

    st.header('Temperature datasets')

    st.markdown(
        """
Berkeley Earth datasets are provided as a set of txt files, corresponding to monthly updates on various areas from worldwide measures down to hemispheres and countries. 

All files are built along the same format. The headers have a complete description of the dataset, including a set of monthly average measures on a reference time range (from January 1951 to December 1980). This time period was selected on the one hand for the reliability and completeness of the observations, and on the second hand because it represents a sort of median of the whole dataset. Following is a **space-separated table of monthly anomalies**, or relative measures, and their uncertainty on a period ranging from 1750 at the earliest to 2021.

**Anomalies** represent a relative value, expressed in degrees Celsius and corresponding to the difference,
positive or negative, between the measured temperature and the corresponding average reference temperature. More
information on this measurement and the interest of reasoning in terms of anomalies can be found [on the
NASA website](https://data.giss.nasa.gov/gistemp/faq/abs_temp.html).

**Uncertainty** is the dispersion related to various factors, in particular geographical and statistical under-sampling, ultimately influencing the quality of the measurement. It represents the 95% confidence interval. 

**These figures put together allow us to compute the temperatures in absolute values.**
        """
    )

    with st.expander("More about the datasets"):
        tab1, tab2, tab3 = st.tabs(["Global Temperatures", 
                                    "Temperature by hemisphere", 
                                    "Temperatures by country"])
        with tab1:
            st.dataframe(temps_globales.tail(10))
        with tab2:
            st.dataframe(temps_hemis.tail(10))
        with tab3:
            st.dataframe(temps_countries.tail(10))
   
        st.markdown(
        """
Each line has 12 fields:
* The first four columns provide information about the year, month, anomaly and uncertainty for the measure.
* The last 8 columns provide centered moving averages over 1, 5, 10 and 20 years. As an example, the yearly moving average for 1950 (January-December) is reported for June 1950. As a consequence we can observe NaNs at the top and bottom of the dataset.
        """
        )

    st.markdown(
        """
We can visualise the evolution of temperatures across the 180 countries of the dataset: please select any item in the list.
        """
    )
      
    # Add country selection
    options = st.multiselect(
        'Sélectionner un pays',
        temps_countries.columns[2:],
        ['france', 'united-states-of-america', 'china'],
        key = "temps_countries")

    if len(options) == 0 : 
        st.markdown("Warning: please select at least one country.")
    else :
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(temps_countries_10y['year'], temps_countries_10y[options], label=options)
        ax.set_ylim(bottom=0)
        ax.grid(visible=True, alpha=0.5)
        ax.legend(loc='lower left')
        ax.set_title("10 years moving average temperature by country")
        st.pyplot(fig=fig, )
        
        
    st.header('Carbon dioxyde datasets')

    st.markdown(
        """
We identify two datasets for the Carbon dioxyde analysis. The first one is the yearly total emission of $CO_2$ by country, and the second one details annual worldwide emissions associated to *land use* and *fossil fuel and industry*.
        """
        )

    with st.expander("More about the datasets"):
        tab1, tab2 = st.tabs(["CO2 emissions, worldwide", 
                              "CO2 emissions, by country"])
        with tab1:
            st.dataframe(co2_global.tail(10))
        with tab2:
            st.dataframe(co2_countries.tail(10))

    st.markdown(
        """
Countries are identified according to their ISO 3166 - alpha-3 code. As for the temperatures, there are missing values for some countries over some time ranges.
        """
    )

    st.markdown(
        """
We can visualise the evolution of $CO_2$ emissions by country. Please select the countries of your choice in the list to display them. `OWID_WRL` displays the overall worldwide emissions.
        """
    )
    
    # Add country selection
    options = st.multiselect(
        'Select a country',
        co2_countries.columns[1:],
        default=['FRA', 'USA', 'CHN', 'OWID_WRL'],
        key="co2_countries")

    if len(options) == 0 : 
        st.markdown("Warning: please select at least one country.")
    else :
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(co2_countries['year'], co2_countries[options], label=options)
        ax.set_ylim(bottom=0)
        ax.grid(visible=True, alpha=0.5)
        ax.legend(loc='lower left')
        ax.set_title("Yearly $CO_2$ emissions, by country")
        st.pyplot(fig=fig)
        
    st.markdown(
        """

Les **données de $CO_2$ globales** nous fournissent une autre information : la quantité de $CO_2$ émise par l’utilisation 
des terres, en plus de la génération de $CO_2$ liée à la production d'énergie et industrielle. Les terres, en fonction 
de leur utilisation, produisent une certaine quantité de $CO_2$ qui vient s’ajouter à la production industrielle ; dans 
certains cas elles peuvent aussi en consommer, et nous pouvons avoir des valeurs négatives sur cette mesure. 

Visualisons l'évolution des ces deux valeurs (exprimées en Gigatonnes) sur la période de mesure.
        """
    )
    
    # Add country selection
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(co2_global['Year'], co2_global['Land use emissions (GtCO2)'], label='Land use emissions (GtCO2)')
    ax.plot(co2_global['Year'], co2_global['Fossil fuel and industry emissions (GtCO2)'], label='Fossil fuel and industry emissions (GtCO2)')
#    ax.plot(co2_countries['year'], co2_countries['OWID_WRL'], label='Total global')
    ax.set_ylim(bottom=0)
    ax.grid(visible=True, alpha=0.5)
    ax.legend(loc='upper left')
    ax.set_title("Production de $CO_2$ globale, par an")
    st.pyplot(fig=fig)
        

    st.header('Lecture et pré-traitement des données')

    st.subheader('Lecture')

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

Les **informations de $CO_2$ par pays** sont disponibles en format CSV ; comme pour le dataset précédent des 
températures par pays, les valeurs manquantes sont liées à des périodes où le pays, pour quelque raison que ce soit, 
n'a pas pu collecter les données. Ces trous représentent des plages de temps importantes, et nous les laisserons 
tels quels pour ne pas compromettre l'intégrité statistique des données.
        """
    )

    st.subheader('Agrégation des données')

    st.markdown(
        """
Nous souhaitons mettre à disposition de nos utilisateurs les jeux de données nettoyés afin qu'ils puissent les utiliser facilement.
Nous utiliserons pour cela le format CSV, qui peut être aisément importé dans d'autres outils (e.g. Excel) et est plus 
facile à manipuler que les fichier texte originaux. 

Egalement, les informations par hémisphère et par pays sont fournies dans des fichiers distincts (par hémisphère dans le premier 
cas, et par pays dans le second). Afin de faciliter leur lecture, analyse et ré-utilisation, nous les rassemblons pour
obtenir des jeux de données unifiés et cohérents (i.e. un fichier pour les hémisphères, et un fichier pour tous les 
pays). 

Les fichiers générés sont disponibles ci-après :
* [temperatures_globales.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/temperatures_globales.csv) fournit les températures globales,
* [temperatures_hemispheres.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/temperatures_hemispheres.csv) fournit les températures par 
  hémisphère, et
* [temperatures_countries.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/temperatures_countries.csv) fournit les températures par pays,
* [co2_global.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/co2_global.csv) fournit le production de CO2 globale,
* [co2_countries.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/co2_countries.csv) fournit la production de CO2 par pays.


        """
    )
