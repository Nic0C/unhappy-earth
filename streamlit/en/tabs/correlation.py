import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score


title = "Is the evolution of temperatures correlated to $CO_2$ emissions?"
sidebar_name = "Correlations"                                                  
                                                    
def run():
    
    st.image("streamlit/en/assets/Reftinsky_reservoir_of_Sverdlovsk_region.jpg", use_column_width=True)   
    st.title(title)
    
    
# Création du DataFrame "co2_temps" :
        
    st.markdown(
        """
        The objective of this section is to **analyze the relationship between these 2 variables**, and **model it** in order to measure its
         relevance.
        
        
         For this purpose, we create, from our datasets `temperatures_globales.csv` and `co2_global.csv`, the DataFrame `co2_temps`.
         We calculate the 10-year rolling average of global temperatures, the sum of $CO_2$ emissions due to
         land use and those related to the combustion of fossil fuels. Finally, we reduce it to the 1860 - 2020 period.
        """
        )
    
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
    
    # Affichage optionnel d'un aperçu du DF :
    
    with st.expander("Learn more about this DataFrame...") :
        st.dataframe(co2_temps)
        st.markdown(
            """
            | Name | Type |NaNs| Description | Example |
             |-------|---------|----|-------------|---------|
             | year | int | 0 | The year in xxxx format |2016 |
             | abs | float | 0 | Average annual temperature in absolute value, in °C |10.027833|
             | abs_10y_mov_avg| float | 9 | Moving average temperature over 10 years, in absolute value in °C | 9.635650 |
             | Land use $CO_2$ emissions | float | 0 | Quantity of $CO_2$ emitted by land use (in Gigatons) | 3.703575 |
             | Fossil fuel and industry $CO_2$ emissions | float | 0 | Quantity of $CO_2$ emitted by the combustion of fossil fuels and by industry (in Gigatons) | 35.452459 |
             | Total $CO_2$ emissions | float | 0 | Total $CO_2$ emissions (in Gigatons) | 39.156034 |
            """
            )
    
    # Affichage graphe températures / émissions CO2 :
        
    st.markdown("**We compare the evolution of the 4 main variables in the following graph:**")
    
    fig, ax1 = plt.subplots(figsize=(18,10))
    
    ax1.grid(color='grey', alpha=0.3, linewidth=1)
    ax1.plot(co2_temps['year'], co2_temps['Land use emissions (GtCO2)'],
         label = "Land use CO2 emissions")
    ax1.plot(co2_temps['year'], co2_temps['Fossil fuel and industry emissions (GtCO2)'],
         label = "Fossil fuel and industry CO2 emissions")
    ax1.plot(co2_temps['year'], co2_temps['Total emissions (GtCO2)'],
         label="Total emissions")
    ax1.set_xlabel("Year", fontsize=14)
    ax1.set_ylabel("$CO_2$ emitted / Gigatons", fontsize=14)
    
    ax2 = ax1.twinx()
    ax2.grid(color='grey', alpha=0, linewidth=2)
    ax2.plot(co2_temps['year'], co2_temps['abs_10y_mov_avg'], c='r', linestyle='--',
         label = "Absolute temperatures: 10 years rolling averages")
    ax2.set_ylabel("Absolute temperature / °C", fontsize=14)
    
    ax1.set_title("Evolution of absolute temperatures and $CO_2$ emissions", fontsize=14)
    fig.legend(loc='upper center', bbox_to_anchor=(0.30, 0.85), fontsize=14, frameon=True)
    st.pyplot(fig)
    
    # Commentaire graphique :
        
    st.markdown(
        """
        **Rising temperatures seem to follow that of total $CO_2$ emissions**, although in a less linear way. We
         also note a sharp drop in $CO_2$ emissions in 2020, linked to the overall drop in activity during the Covid crisis.
         Unfortunately, this one-time drop will have no effect on the climate, given the accumulation of $CO_2$ emissions into the
         the atmosphere for several decades (article [here](https://www.cairn.info/magazine-pour-la-science-2020-7-page-7.htm)).
        """
        )
    
    
# Tests de corrélation :
    
    st.header("Correlations")
    
    # Affichage optionnel de la heatmap :
    
    st.markdown(
        """
        We are now going to determine the **correlation coefficients** between our variables, using **Pearson's statistical test**.
        """
        )    
    
    with st.expander("Display a 'heatmap' of the DataFrame's correlations...") :
        fig, ax = plt.subplots()
        sns.heatmap(co2_temps.drop('abs', axis=1).corr(method="pearson"), ax=ax)#,annot=True)
        st.pyplot(fig)
    
        st.markdown(
            """
            The heatmap allows us to **visually identify the degrees of correlation** between our variables. We are already seeing a
            near-perfect correlation between fossil fuels and industry emissions, and total emissions.
            """
            )
    
    st.markdown("Let's measure the **correlation between 2 variables of your choice** of our DataFrame:")
    
    cols = {"year" : "Year",
            "abs_10y_mov_avg" : "Average temperatures",
            "Land use emissions (GtCO2)": "Land use CO2 emissions",
            "Fossil fuel and industry emissions (GtCO2)": "Fossil fuel and industry CO2 emissions",
            "Total emissions (GtCO2)": "Total CO2 emissions"}
    
    options = st.multiselect("Which pair of variables do you want to subject to Pearson's test?",
                             list(co2_temps.drop("abs", axis=1).columns),
                             list(co2_temps.drop(["abs", "Land use emissions (GtCO2)", "Fossil fuel and industry emissions (GtCO2)",
                             "Total emissions (GtCO2)"], axis=1).columns),
                             format_func=cols.get)
    
    if len(options) == 0 : 
        st.markdown("**Warning**: Select 2 variables!")
    elif len(options) == 1 :
        st.markdown("**Warning**: Select another variable!")
    elif len(options) > 2 :
        st.markdown("**Warning**: Please select only 2 variables!")
    else :
        pearson_coef = round(pearsonr(co2_temps[options[0]], co2_temps[options[1]])[0], 5)
        st.markdown(f"The correlation coefficient according to the Pearson test is: **{pearson_coef}**")
          
        if pearson_coef >= 0.90 :
            st.markdown("The correlation between these 2 variables is **HIGH**!")
        elif pearson_coef < 0.90 and pearson_coef >= 0.50 :
            st.markdown("The correlation between these 2 variables is **MEDIUM**.")
        else :
            st.markdown("The correlation between these 2 variables is **LOW**.")
            
    st.markdown(
        """
        Those results confirm that:
         - The total $CO_2$ emissions and the average temperatures over 10 years each show a strong correlation to the years:
             coefficients > 0.90. **As the years pass, $CO_2$ emissions and temperatures increase**.
         - Land use emissions are only moderately correlated to the years: coef = 0.55. On the graph, we indeed observe a drop in
             these over the studied period's last third (1960 - 2020). **Emissions related to fossil fuels and industry actually weigh
             heavily on total emissions**: coef > 0.99!.
         - **Average temperatures** over 10 years and **total emissions** are even more so between themselves: coefficient > 0.95.
             Beyond the general upward trend of these 2 variables, this confirms that overall, **the variations of one follow the variations
             of the other**.
        """
        )
 
    
# Régressions température / émissions CO2 :
    
    st.header("Regressions")
    
    st.markdown(
        """
        **Let's take a closer look at the relationship between $CO_2$ emissions and temperatures.** We can visualize it using a **scatterplot**:
        """
        )
    
    fig, ax = plt.subplots(figsize=(18,10))
    plt.grid(color='grey', alpha=0.5, linewidth=2)
    ax.scatter(co2_temps['Total emissions (GtCO2)'], co2_temps['abs_10y_mov_avg'], 
                c=co2_temps['abs_10y_mov_avg'], cmap='jet', s=20,
                label="Absolute temperatures : 10 years rolling averages")
    ax.set_xlabel('Emitted $CO_2$ / Gigatons',  fontsize=14)
    ax.set_ylabel('Absolute temperatures / °C / 10 years rolling averages', fontsize=14)
    ax.set_title("Evolution of absolute temperatures according to $CO_2$ emissions", fontsize=14)
    fig.legend(loc='upper center', bbox_to_anchor=(0.30, 0.85), fontsize=14, frameon=True)
    st.pyplot(fig)
    
    # Commentaire graphique :
        
    st.markdown(
        """
        We have seen through statistical tests that these 2 variables are strongly correlated, which we can observe in this graphical representation.
        
         **The objective of a regression is to explain a variable Y by means of another variable X.**
         With a polynomial regression, the relationship between the explanatory variable and the explained variable is modeled as a $n$ degree polynomial.
        
         We **model the link between our two variables** thanks to the **LinearRegression** and **PolynomialFeatures** Scikit-Learn functions:
        """
        )
    
    # Regression linéraire :    
        
    x = co2_temps[['Total emissions (GtCO2)']]
    y = co2_temps['abs_10y_mov_avg']
    
    col1, col2 = st.columns(2)
    with col1 :
        degree = st.slider('Select the regression degree:', 1,5)
    
    if degree == 1 :
        
        # Entraînement de la régression :
        
        lr = LinearRegression()
        lr.fit(x, y)
        y_pred = lr.predict(x)
        
        st.markdown(
            f"""
            Intercept (Y value when X = 0): **${lr.intercept_}$**
            
            Coefficient (regression 'slope'): **${lr.coef_[0]}$**

            A $1$ degree polynomial regression is a simple linear regression, which can be interpreted as follows:
                
            $Temperature \ (°C) = {round(lr.intercept_, 3)} + {round(lr.coef_[0], 3)} * CO_2 \ emissions \ (Gt)$
            
            Let's visualize the linear regression result by displaying it on the scatter plot:
            """
            )
            
        # Affichage scatter + droite régression :
        
        fig, ax1 = plt.subplots(figsize=(18,10))
        plt.grid(color='grey', alpha=0.5, linewidth=2)
        ax1.scatter(x,
                    y, 
                    c=y,
                    cmap='jet',
                    s=20,
                    label='Absolute temperatures')
    
        ax2 = ax1
        ax2.plot(x,
                 y_pred,
                 'r--',
                 label='Linear Regression')
        
        ax1.set_title("Evolution of absolute temperatures according to $CO_2$ emissions : Scatterplot & Regression line", fontsize=14)
        plt.xlabel('Emitted $CO_2$ / Gigatons', fontsize=14)
        plt.ylabel('Absolute temperatures / °C / 10 years rolling averages', fontsize=14)
        plt.legend(loc='upper left', bbox_to_anchor=(0.05, 0.9), fontsize=14, frameon=True)
        st.pyplot(fig)
    
        # Evaluation de la régression :
        
        st.markdown("In order to **evaluate our regression**, we use the **$R^2$ score** metric.")
    
        score = round(r2_score(y, y_pred), 5)
        st.markdown(f"Score : **${score}$**")
    
    
    # Régression polynomiale :
    
    if degree > 1 :
        
        # Entraînement de la régression :
        
        poly_feats = PolynomialFeatures(degree=degree, include_bias=False)
        x_poly = poly_feats.fit_transform(x)
        
        plr = LinearRegression()
        plr.fit(x_poly, y)
        
        y_poly_pred = plr.predict(x_poly)
        
        coeffs = []
        for i in plr.coef_ :
            coeffs.append(i)
        
        st.markdown(
            f"""
            Intercept (Y value when X = 0): **${round(plr.intercept_,5)}$**
            
            Coefficient (regression 'slope'): **${coeffs}$**

            This is a ${degree}$ degree polynomial regression, for which:
            
            $Temperature \ (°C) = {round(plr.intercept_,5)} + \sum_1^{degree} coef_{degree} * (polynomial \ of \ (CO_2 \ emissions \ (Gt))_{degree}$
            
            Let's visualize the polynomial regression result by displaying it on the scatter plot:
            """
            )
        
        # Affichage scatter + droite régression :
        
        fig, ax1 = plt.subplots(figsize=(18,10))
        plt.grid(color='grey', alpha=0.5, linewidth=2)
        ax1.scatter(x,
                    y, 
                    c=y,
                    cmap='jet',
                    s=20,
                    label='Absolute temperatures')
    
        ax2 = ax1
        ax2.plot(x,
                 y_poly_pred,
                 'r--',
                 label=f'{degree} degree polynomial regression')
        
        ax1.set_title(f"Evolution of absolute temperatures according to $CO_2$ emissions : Scatterplot & {degree} degree regression curve",
                      fontsize=14)
        plt.xlabel('Emitted $CO_2$ / Gigatons', fontsize=14)
        plt.ylabel('Absolute temperatures / °C / 10 years rolling averages', fontsize=14)
        plt.legend(loc='upper left', bbox_to_anchor=(0.05, 0.9), fontsize=14, frameon=True)
        st.pyplot(fig)
        
        # Evaluation de la régression :
        
        st.markdown("In order to **evaluate our regression**, we use the **$R^2$ score** metric.")
    
        score = round(r2_score(y, y_poly_pred), 5)
        st.markdown(f"Score : **${score}$**")
    
    st.markdown(
        """
        By varying the degree of the polynomial regression from 1 to 5, **we obtain increasing $R^2$ scores between 0.918 and 0.966** (with a
        risk of overfitting).
        **Therefore the model is efficient** and confirms the close relationship that exists between our 2 variables. **$CO_2$ emissions are
        a major explanatory variable for the rise in temperatures**.
        """
        )    
    

# Interprétation des résultats :
    
    st.header("Results interpretation")
    
    st.markdown(
        """
        Based on the results of the Pearson statistical tests, and on the scores obtained with the different degrees of regression, we are now
        able to affirm that **statistically, the rise in temperatures is very strongly linked to that of $CO_2$ emissions**.
        
         **Though, let's be careful**: in the context of a **statistical** study like ours, **correlation or linearity does not necessarily mean
         causality**.
        """
        )

    st.markdown(
        """
        <br />
        
        ----
    
        Image credit: Vasily Iakovlev, [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0),
        via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Reftinsky_reservoir_of_Sverdlovsk_region.jpg).
         """,
         unsafe_allow_html=True
         )
    
