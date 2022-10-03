import streamlit as st
import pandas as pd
import numpy as np


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

    st.write(new_column.tail())     

