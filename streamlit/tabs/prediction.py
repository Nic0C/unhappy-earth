import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet


title = "Prédictions"
sidebar_name = "Prédictions"


def run():
#Importer les donnes:
    df = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    
    st.title("Modélisation / prédiction de la température sur les prochaines années.")
    
    st.subheader("Pouvons-nous prédire les températures sur les prochaines décennies ?")
    
    st.markdown("Parmi différents modèles, nous avons choisi Facebook Prophet. Prophet permet la prédiction de données de séries temporelles. Nous avons testé le modèle multiplicatif et le modèle additif de Facebook Prophet et nous avons vu que le deuxième correspond mieux à nos données: aux tendances non-linéaires s'ajoute une composante liée à la saisonnalité. Cette librairie est donc particulièrement adaptée à notre étude.")
    
    st.markdown("Nous allons nous concentrer sur la période où la tendance croissante de la température est constante et forte, c'est-à-dire à partir de 1975.")

    st.markdown("Dans le graphique suivant nous visualisons bien que pendant la période comprise entre 1975 et 2022 la tendance de la température absolue est explicite, croissante, constante et forte (augmentation de la tendance de 8,7 °C en 1975 jusqu’à 10 °C en 2022) :")


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
    ax1.set_xlabel("Date (par annnée)")
    ax1.set_ylabel("Température absolue en °C")
    plt.title("Température absolue entre 1975 et 2022 (données mensuelles)")
    plt.grid(color='grey', alpha=0.2)

    fig.legend(loc='upper center', bbox_to_anchor=(0.28, 0.85))
    
    st.pyplot(fig)


#Prediction Prophet    
    st.markdown("A partir de nos données, Facebook Prophet calcule la prédiction suivante pour les températures sur les 50 prochaines années:")

    m = Prophet(seasonality_mode='additive').fit(new_column)
    future = m.make_future_dataframe(periods=600, freq='M')
    fcst = m.predict(future)

    fig = m.plot(fcst, figsize=(16,6), xlabel ='Date (par annnée)', ylabel='Température absolue en °C')
    fig.suptitle("Prédiction de la température sur les 50 prochaines années",  y=1.02)
    import warnings
    warnings.filterwarnings("ignore")
    st.pyplot(fig)

    st.markdown("La prédiction qui commence à partir de l'année 2022 sur ce graphique, nous montre toujours une évolution de la température à la hausse. ")

#Presentation des components: tendance et la déviation
    st.markdown("Pour plus de détail, visualisons 2 composantes de la prédiction :")
    st.markdown("- la tendance ;")
    st.markdown("- les déviations saisonnières de cette tendance :")
    
    fig = m.plot_components(fcst, figsize=(16,8))
    fig.suptitle("Prediction de la tendance de la température absolue et de la variation saisonnière", y=1.02, fontsize=14)
    axes = fig.get_axes()

    axes[0].set_xlabel('Date (par annnée)')
    axes[0].set_ylabel('Température absolue en °C')
    axes[1].set_xlabel("Mois de l'année")
    axes[1].set_ylabel('Var saisonnière de la temp par rapport à la tendance, en°C')
    warnings.filterwarnings("ignore")
    st.pyplot(fig)
    
#Conclusion
    st.markdown("Notre prévision repose sur le principe que la température globale absolue va suivre la même tendance que ces 46 dernières années, sans action climatique majeure. Dans ce cas, notre modèle prédit une croissance approximative de 1.9 °C dans 50 ans (10 °C en 2021, jusqu’à 11,9 °C en 2072) . En comparaison avec la multitude d'études prévisionnelles qui existent actuellement, notre résultat semble juste et raisonnable, mais bien peu optimiste.")
    