import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet


title = "Prédictions"
sidebar_name = "Prédictions"


def run():

    st.image("streamlit/assets/station_meteo.jpg", use_column_width=True)    

#Importer les donnes:
    df = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    
    st.title("Modélisation / prédiction de la température sur les prochaines années.")
    
    st.markdown("---")
    
    st.subheader("Pouvons-nous prédire les températures sur les prochaines décennies ?")
    
    st.markdown("Parmi différents modèles, nous avons choisi **Facebook Prophet**. Prophet permet la **prédiction** de données **de séries temporelles**. Nous avons testé le modèle multiplicatif et le **modèle additif** de Facebook Prophet et nous avons vu que le deuxième correspond mieux à nos données: aux tendances non-linéaires s'ajoute une composante liée à la saisonnalité. Cette librairie est donc particulièrement **adaptée à notre étude**.")
    
    st.markdown("Nous allons nous concentrer sur la **période où la tendance de la température absolue est croissante, constante et explicite**. Dans le graphique suivant nous visualisons bien que c'est la **période comprise entre 1975 et 2022**.")

    col1, col2 = st.columns(2)
    col1.metric("Temperature 1975", "8.7 °C")
    col2.metric("Temperature 2022", "10 °C", "1.3 °C")

    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: center;
    }
    </style>
    ''', unsafe_allow_html=True)

#Definition des donnes a traiter: 
    new_column = df.loc[(df['date'] >= '1975-01-15')] 
    new_column = new_column[['date', 'abs']] 
    new_column.dropna(inplace=True)
    new_column.columns = ['ds', 'y'] 

# Affichage graphe evolution températures / tendance:
    fig, ax1 = plt.subplots(figsize=(16,4))
    formatter = mdates.DateFormatter("%Y") ### formatter of the date
    
    ax1.xaxis.set_major_formatter(formatter) ## calling the formatter for the x-axis   
    
    ax1.plot(mdates.date2num(new_column['ds']), new_column['y'], label="Temperature absolue")    

    x = mdates.date2num(new_column['ds'])
    z = np.polyfit(x, new_column['y'], 1)
    p = np.poly1d(z)
     
    ax1.plot(x,p(x),"r--", label="Tendance")
    ax1.set_xlabel("Date (par annnée)", fontsize=14)
    ax1.set_ylabel("Température absolue en °C", fontsize=14)
    plt.title("Température absolue entre 1975 et 2022 (données mensuelles)", fontsize=18)
    plt.grid(color='grey', alpha=0.2)

    fig.legend(loc='upper center', bbox_to_anchor=(0.20, 0.91))
    
    st.pyplot(fig)


#Prediction Prophet    
    st.markdown("A partir de nos données, Facebook Prophet calcule la **prédiction** suivante pour les **températures sur les 50 prochaines années**:")


    m = Prophet(seasonality_mode='additive').fit(new_column)
    future = m.make_future_dataframe(periods=600, freq='M')
    fcst = m.predict(future)
    fig = m.plot(fcst, figsize=(16,6), xlabel ='Date (par annnée)', ylabel='Température absolue en °C')
    axes = fig.get_axes()

    axes[0].set_xlabel('Date (par annnée)', fontsize=18)
    axes[0].set_ylabel('Température absolue en °C', fontsize=18)

    fig.suptitle("Prédiction de la température sur les 50 prochaines années",  y=1.02, fontsize=24)
    import warnings
    warnings.filterwarnings("ignore")
    st.pyplot(fig)

    st.markdown("La prédiction qui commence à partir de l'année 2022 sur ce graphique, nous montre **toujours une évolution** de la température **à la hausse**. ")

#Presentation des components: tendance et la déviation
    st.markdown("Pour plus de détail, visualisons **2 composantes de la prédiction** :")
    st.markdown("- **la tendance** ;")
    st.markdown("- **les déviations saisonnières** de cette tendance :")
    
    fig = m.plot_components(fcst, figsize=(18, 10))
    fig.suptitle("Prediction de la tendance de la température absolue et de la variation saisonnière", y=1.02, fontsize=24)
    axes = fig.get_axes()

    axes[0].set_xlabel('Date (par annnée)', fontsize=18)
    axes[0].set_ylabel('Température absolue en °C', fontsize=18)
    axes[1].set_xlabel("Mois de l'année", fontsize=18)
    axes[1].set_ylabel('Var saisonnière temp / tendance, en°C', fontsize=18)
    warnings.filterwarnings("ignore")
    
    st.pyplot(fig)

#Conclusion

    col1, col2 = st.columns(2)
    col1.metric("Temperature 2022", "10 °C")
    col2.metric("Temperature 2072", "11.9 °C", "1.9 °C")

    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: center;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.markdown("Notre prévision repose sur le **principe** que la température globale absolue va suivre la **même tendance que ces 46 dernières années, sans action climatique majeure**. Dans ce cas, notre modèle prédit une **croissance approximative de 1.9 °C dans 50 ans**. En **comparaison** avec la multitude d'**études prévisionnelles** qui existent actuellement, **notre résultat** semble **juste et raisonnable**, mais bien peu optimiste.$^[$ $^1$ $^]$ $^,$ $^[$ $^2$ $^]$ $^,$ $^[$ $^3$ $^]$")

    st.markdown(
        """
        <br />
        
        ----
        Liens vers les articles et études consultées:  
         <font size="2"> $^[$ $^1$ $^]$ [La hausse de la température globale s’est encore accentuée, selon le dernier rapport du GIEC](https://www.ecologie.gouv.fr/hausse-temperature-globale-sest-encore-accentuee-selon-dernier-rapport-du-giec)  
        $^[$ $^2$ $^]$ [L'ampleur des hausses que vous connaîtrez](https://www.francelive.fr/article/france-live/vous-pouvez-desormais-savoir-le-changement-climatique-que-vous-subirez-selon-votre-age-7403908/)  
        $^[$ $^3$ $^]$ [Les prévisions alarmantes de Météo France](https://www.lefigaro.fr/sciences/rechauffement-climatique-les-previsions-alarmantes-de-meteo-france-20210201) </font>    
        
        Crédit image : Michal Osmenda, [CC-BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0),
        via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Weather_station_on_Mount_Vesuvius_(2437693238).jpg).
        """,
        unsafe_allow_html=True
        )    
    