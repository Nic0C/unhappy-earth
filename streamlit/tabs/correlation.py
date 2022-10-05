import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


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
    
    # Création du DataFrame "co2_temps" :
        
    st.markdown("Afin d'analyser la relation entre ces deux variables, nous créons, à partir de nos datasets 'temperatures_globales.csv' et 'co2_global.csv', le DataFrame 'co2_temps'.")
    st.markdown("Nous calculons la moyenne glissante sur 10 ans des températures globales, la somme des émissions de $CO_2$ dues à l’utilisation des sols et de celles liés à la combustion d’énergie fossiles.")
    st.markdown("Enfin, nous le réduisons à la période 1860 - 2020.")
    
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
    
    # Affichage graphe températures / émissions CO2 :
        
    st.markdown("Nous pouvons comparer l’évolution de ces 4 variables de ce DataFrame dans le graphique suivant :")
    
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
    
    # Commentaire graphique :
        
    st.markdown("La hausse des températures semble suivre celle des émissions totales de $CO_2$, bien que de manière moins linéaire. Nous constatons également une nette baisse des émissions de $CO_2$ en 2020, liée à la baisse globale d'activité pendant la crise Covid. Malheureusement, cette baisse ponctuelle n’aura eu aucun effet sur le climat, face à l’accumulation des rejets de $CO_2$ dans l’atmosphère pendant plusieurs décennies (article [ici](https://www.cairn.info/magazine-pour-la-science-2020-7-page-7.htm)).")
    
    
    # Tests de corrélation :
    
    st.header("Corrélation")
    
    st.markdown("Mesurons la corrélation entre 2 variables de notre DataFrame :")
    
    cols = {
        "year" : "Année",
        "abs_10y_mov_avg" : "Températures moyennes",
        "Land use emissions (GtCO2)": "Emissions de CO2 liées à l'utilisation des sols",
        "Fossil fuel and industry emissions (GtCO2)": "Emissions de CO2 des combustibles fossiles et de l'industrie",
        "Total emissions (GtCO2)": "Emissions totales"}
    
    options = st.multiselect("Quelle paire de variables souhaitez-vous soumettre au test de Pearson ?",
                             list(co2_temps.drop("abs", axis=1).columns),
                             #list(co2_temps.drop(["abs", "Land use emissions (GtCO2)", "Fossil fuel and industry emissions (GtCO2)", "Total emissions (GtCO2)"], axis=1).columns),
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
            
    st.markdown("Les résultats de ces tests nous confirment que :")
    st.markdown("- Les émissions totales de CO2 et les températures moyennes sur 10 ans présentent chacune une forte corrélation aux années : coefs > 0.90. Les années passant, les émissions de CO2 et les températures augmentent.")
    st.markdown("- Les températures moyennes sur 10 ans et les émissions totales le sont encore plus entre elles : coef > 0.95. Au-delà de la tendance générale à la hausse de ces 2 variables, cela confirme que globalement, les variations de l'une suit les variations de l'autre.")
    st.markdown("- Les émissions dues à l'utilisation des sols ne sont que moyennement corrélées aux années : coef = 0.55. Sur le graphique, nous observons en effet une baisse de celles-ci sur le dernier tiers de la période étudiée (1960 - 2020).")
    
    
    # Régression linéaire température / émissions CO2 :
    
    st.header("Régression")
    
    st.markdown("Intéressons nous de plus près à la relation qu'entretiennent émissions de $CO_2$ et températures. Nous pouvons la visualiser à l'aide d'un **scatterplot** (nuage de points) :")
    
    fig, ax = plt.subplots(figsize=(18,10))
    plt.grid(color='grey', alpha=0.5, linewidth=2)
    ax.scatter(co2_temps['Total emissions (GtCO2)'], co2_temps['abs_10y_mov_avg'], 
                c=co2_temps['abs_10y_mov_avg'], cmap='jet', s=20)
    ax.set_xlabel('$CO^2$ émis / Gigatonnes')
    ax.set_ylabel('Température absolue / °C / Moyennes glissantes sur 10 ans')
    ax.set_title("Evolution des températures absolues en fonction des émissions de $CO^2$")
    st.pyplot(fig)
    
    # Commentaire graphique :
        
    st.markdown("Nous avons vu grâce aux tests statistiques que ces 2 variables sont fortement corrélées, il n'est pas surprenant d'observer une relative linéarité dans cette représentation graphique.")
    
    st.markdown("Une régression linéaire simple a pour objectif d’expliquer une variable Y par le moyen d’une autre variable X.")
    st.markdown("Nous modélisons le lien entre nos deux variables avec la fonction LinearRegression.")
    
    # Entraînement de la régression :
    
    slr = LinearRegression()
    slr.fit(co2_temps[['Total emissions (GtCO2)']], co2_temps['abs_10y_mov_avg'])
    
    st.markdown("Valeur de l'intercept (= valeur de Y lorsque X = 0) :")
    st.markdown(slr.intercept_)
    st.markdown("Valeur du coefficient (= 'pente' de la régression) :")
    st.markdown(slr.coef_[0])
    
    st.markdown("Nous pouvons donc interprêter le modèle grâce à cette formule :")
    st.markdown("$Température \ (°C) = 7.990 + 0.038 * émissions \ de \ CO_2 \ (Gt)$.")
    
    # Affichage scatter + droite régression
    
    st.markdown("Il est plus facile de comprendre ces résultats en visualisant la droite de régression sur le nuage de points :")
    
    fig, ax1 = plt.subplots(figsize=(18,10))
    plt.grid(color='grey', alpha=0.5, linewidth=2)
    ax1.scatter(co2_temps['Total emissions (GtCO2)'],
                co2_temps['abs_10y_mov_avg'], 
                c=co2_temps['abs_10y_mov_avg'],
                cmap='jet',
                s=20,
                label='Températures absolues')
    ax2 = ax1
    ax2.plot(co2_temps['Total emissions (GtCO2)'],
             slr.intercept_ + slr.coef_[0] * co2_temps['Total emissions (GtCO2)'],
             'r--',
             label='Régression linéaire')
    plt.xlabel('$CO^2$ émis / Gigatonnes')
    plt.ylabel('Température absolue / °C / Moyennes glissantes sur 10 ans')
    plt.legend(loc='upper left', bbox_to_anchor=(0.05, 0.9))
    st.pyplot(fig)
    
    # Evaluation de la régression :
    
    st.markdown("Afin d'évaluons notre régression, nous utilisons la métrique du score $R^2$. Voici le score obtenu :")

    pred_temp = slr.predict(co2_temps[['Total emissions (GtCO2)']])
    score = r2_score(co2_temps['abs_10y_mov_avg'], pred_temp)
    
    st.markdown(score)
    st.markdown("Notre modèle obtient un score R2 proche de 0.92, il est donc performant et confirme la linéarité entre nos variables. Les émissions de $CO_2$ semblent donc bien être une variable explicative majeure de la hausse des températures.")
    
    # Conclusion
    
    st.header("Conclusion")
    
    st.markdown("Forts des résultats des tests statistiques de Pearson, et du score obtenu par le modèle de régression linéaire, nous sommes à présent en mesure d'affirmer que **statistiquement, la hausse des températures est très fortement liée à celle des émissions de $CO^2$**.")
    st.markdown("**Attention cependant** : dans le cadre d'une étude statistique comme la nôtre, **corrélation ou linéarité ne signifient pas nécessairement causalité**.")
    