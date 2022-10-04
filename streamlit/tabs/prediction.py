import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as datetime
from prophet import Prophet


title = "Prédictions"
sidebar_name = "Prédictions"


def run():
#Importer les donnes:
    df = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    
    st.title("Modélisation / prédiction de la température sur les prochaines années.")
    
    st.markdown("Parmi les différents modèles, nous avons choisi Facebook Prophet. Prophet permet la prédiction des données de séries temporelles, en se basant sur un modèle additif : aux tendances non-linéaires s'ajoute une composante liée à la saisonnalité. Cette librairie est donc particulièremet adaptée à notre étude.")
    
    st.markdown("Nous allons filtrer quelques colonnes de notre data set 'global_land'. NeuralProphet ne s’attend qu’à deux colonnes (temporalité / donnée). De plus, concentrons nous sur la période où la tendance croissante de la température est constante et forte, c'est à dire à partir de 1975:")

    new_column = df.loc[(df['date'] >= '1975-01-15')] 
    new_column = new_column[['date', 'abs']] 
    new_column.dropna(inplace=True)
    new_column.columns = ['ds', 'y'] 
    new_column.tail()  

#Premier tableau:
    st.write(new_column.tail()) 

    st.markdown("Nous visualisons bien que pendant la période entre 1975 et 2022 la tendance de la température absolue est explicite, croissante, constante et forte :")    

#Premier graphique:
    import altair as alt

    chart = (
        alt.Chart(
            data = new_column,
            title = "Température absolue entre 1975 et 2022 (données mensuelles)",
        )
        .mark_line()
        .encode(
            x = alt.X("ds", axis = alt.Axis(labelOverlap="greedy",grid=False, title = "Date")),
            y = alt.Y("y", axis = alt.Axis(title = "Température absolue en °C"))
            ).properties(height = 360, width = 140)
        )

    st.altair_chart(chart, use_container_width = True)

    st.markdown("Prédiction de la température sur les 50 prochaines années :")


    # Affichage graphe evolution températures / tendance:
    fig, ax1 = plt.subplots(figsize=(16,4))


    ax1.plot(new_column['ds'], new_column['y'], label="Temperature absolue")
    
    ax2 = ax1.twinx()

    x = mdates.date2num(new_column['ds'])
    y= new_column['y']
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
      
    ax2.plot(x,p(x),"r--")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Température absolue en °C")
    plt.title("Température absolue entre 1975 et 2022 (données mensuelles)")


    fig.legend(loc='upper center', bbox_to_anchor=(0.28, 0.85))
    
    st.pyplot(fig)


#Prediction Prohet    
    st.markdown("Prédiction de la température sur les 50 prochaines années :")

    m = Prophet(seasonality_mode='additive').fit(new_column)
    future = m.make_future_dataframe(periods=600, freq='M')
    fcst = m.predict(future)

    fig = m.plot(fcst, figsize=(16,6), xlabel ='Date (par annnée)', ylabel='Température absolue en °C')
    fig.suptitle("Prédiction de la température sur les 50 prochaines années",  y=1.02)
    import warnings
    warnings.filterwarnings("ignore")
    st.pyplot(fig)