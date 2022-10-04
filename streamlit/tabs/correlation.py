import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


# Lecture des datasets
global_land = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
co2_global = pd.read_csv('data/unhappy_earth/co2_global.csv')

# Preprocess sur datasets
co2_global_reduc = co2_global.rename(columns={'Year': 'year'})
temps_reduc = global_land.groupby('year').agg({'abs': 'mean'}).reset_index()
temps_reduc = temps_reduc.loc[(temps_reduc['year'] >= 1850) & (temps_reduc['year'] < 2021),:]
temps_reduc['abs_10y_mov_avg'] = temps_reduc['abs'].rolling(10).mean()
co2_temps = pd.merge(temps_reduc, co2_global_reduc, on='year')
co2_temps['Total emissions (GtCO2)'] = co2_temps['Land use emissions (GtCO2)'] + co2_temps['Fossil fuel and industry emissions (GtCO2)']

# Résolution d'un problème de cohérence d'unité (tonnes / Gigatonnes)
co2_temps[['Land use emissions (GtCO2)', 
           'Fossil fuel and industry emissions (GtCO2)', 
           'Total emissions (GtCO2)']] = co2_temps[['Land use emissions (GtCO2)', 
                                                    'Fossil fuel and industry emissions (GtCO2)', 
                                                    'Total emissions (GtCO2)']] / 1e+09

co2_temps = co2_temps[co2_temps['year']>=1860]

title = "L'évolution des températures est-elle corrélée aux émissions de $CO_2$ ?"
sidebar_name = "Corrélations"                                                  
                                                    
def run():

    st.title(title)

    st.write("Evolution des températures et des émissions de $CO_2$ dans le temps :")
    
    # Affichage graphe températures / émissions CO2:
    fig, ax1 = plt.subplots(figsize=(18,10))

    ax1.plot(co2_temps['year'], co2_temps['Land use emissions (GtCO2)'],
         label = "Emissions de CO2 dues à l'utilisation des sols")
    ax1.plot(co2_temps['year'], co2_temps['Fossil fuel and industry emissions (GtCO2)'],
         label = "Emissions de CO2 des combustibles fossiles et de l'industrie")
    ax1.plot(co2_temps['year'], co2_temps['Total emissions (GtCO2)'],
         label="Emissions totales")
    ax1.set_xlabel("Year")
    ax1.set_ylabel("$CO_2$ émis / Gigatonnes")

    ax2 = ax1.twinx()
    ax2.plot(co2_temps['year'], co2_temps['abs_10y_mov_avg'], c='r', linestyle='--',
         label = "Températures absolues : moyennes glissantes s/ 10 ans")
    ax2.set_ylabel("Température absolue / °C")

    fig.legend(loc='upper center', bbox_to_anchor=(0.28, 0.85))
    
    st.pyplot(fig)
    
    # Tests de corrélation
    
    st.markdown("### Corrélation")
    
    st.markdown("Mesurez la corrélation entre 2 variables :")
    
    cols = {
        "year" : "Année",
        "abs_10y_mov_avg" : "Temperature moyenne",
        "Land use emissions (GtCO2)": "Emissions de CO2 liées à l'utilisation des sols",
        "Fossil fuel and industry emissions (GtCO2)": "Emissions de CO2 des combustibles fossiles et de l'industrie",
        "Total emissions (GtCO2)": "Emissions totales"}
    
    options = st.multiselect("Quelle paire de variables souhaitez-vous tester ?",
                             list(co2_temps.drop("abs", axis=1).columns),
                             format_func=cols.get)
    
    if len(options) == 0 : 
        st.markdown("Selectionnez 2 variables")
    elif len(options) == 1 :
        st.markdown("Sélectionnez une 2nde variable")
    elif len(options) > 2 :
        st.markdown("Merci de ne selectionnez que 2 variables")
    else :
        pearson_coef = round(pearsonr(co2_temps[options[0]], co2_temps[options[1]])[0], 5)
        st.markdown("Le coefficient de corrélation selon le test de Pearson est :")
        st.markdown(str(pearson_coef))
          
        if pearson_coef >= 0.90 :
            st.markdown("La corrélation entre ces 2 variables est FORTE.")
        elif pearson_coef < 0.90 and pearson_coef >= 0.50 :
            st.markdown("La corrélation entre ces 2 variables est MOYENNE.")
        else :
            st.markdown("La corrélation entre ces 2 variables est FAIBLE.")