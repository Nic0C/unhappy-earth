import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


title = "Confirmation du phénomène"
sidebar_name = "Confirmation"

def read_temps():
    globales = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    hemispheres = pd.read_csv('data/unhappy_earth/temperatures_hemispheres.csv')
    countries = pd.read_csv('data/unhappy_earth/temperatures_countries.csv')
    return globales, hemispheres, countries

def read_co2():
    globales = pd.read_csv('data/unhappy_earth/co2_global.csv')
    countries = pd.read_csv('data/unhappy_earth/co2_countries.csv')
    return globales, countries

def plot_month(df, title) :
    """
    Display both a plot and a scatter plot from a DF, with x = date (by month) and y = absolute temperature.
    Add a cmap to colorize the scatter based on y value.
    Plot 12-months moving average temperature.
    """
    # Set the figure size and grid.
    plt.figure(figsize=(24,10))
    plt.grid(color='grey', alpha=0.2)

    # Display line for monthly measures
    plt.plot(df['date'], df['abs'], c='lightgrey', zorder=1)
    # Display points (circles) for monthly measures
    plt.scatter(df['date'], df['abs'], c=df['abs'], cmap='jet', s=15, zorder=2,
                label='Moyennes mensuelles')
    # Display 12-months moving average as a straight, larger line.
    plt.plot(df['date'], df['mov_average'], color='k', linewidth=2, label='Moyenne glissante sur 12 mois')

    # Add the cmap.
    plt.colorbar()
    plt.clim(df['abs'].min(), df['abs'].max())
    
    # Labels, legend, title.
    plt.xlabel('Date (par mois)')
    plt.ylabel('Température absolue en °C')
    plt.legend()
    plt.title(title)

    return plt

def plot_year(df, title, show_uncert=False) :
    """
    Display both a plot and a scatter plot from a DF, with x = date (by year) and y = absolute temperature.
    The 'show_uncert' parameter allows, if True, to display the uncertainty margin.
    Add a cmap to colorize the scatter plot based on y value, when uncertainty is not plotted.
    """
    # Compute the average of abs and uncert by year.
    temp_year = df[['year', 'abs', 'uncert']].groupby('year').mean().reset_index()
    # Set the figure size and grid.
    plt.figure(figsize=(24,10))
    plt.grid(color='grey', alpha=0.2)

    # Display absolute temperatures.
    plt.plot(temp_year['year'], temp_year['abs'], c='grey', zorder=1)

    # If required, display points and fill the area of uncertainty measures.  
    if show_uncert==True :
        plt.scatter(temp_year['year'], temp_year['abs'],
                    edgecolor='none', zorder=2, label='Moyennes annuelles')
        plt.fill_between(temp_year['year'], 
                         temp_year['abs'] - temp_year['uncert'], 
                         temp_year['abs'] + temp_year['uncert'],
                         color='#D3D3D3', zorder=0, label='Incertitude')
        # Otherwise display absolute temps with a colormap.
    else :
        plt.scatter(temp_year['year'], temp_year['abs'], c=temp_year['abs'],
                    cmap='jet', vmin=-40.5, vmax=40, edgecolor='none', zorder=2,
                    label='Moyennes annuelles')
        plt.colorbar()
        plt.clim(temp_year['abs'].min(), temp_year['abs'].max())

    # Labels, legend, title.
    plt.xlabel('Date (par annnée)')
    plt.ylabel('Température absolue en °C')
    plt.title(title)
    plt.legend()

    return plt

def run():
    
    st.title(title)
    
    temps_globales, temps_hemis, temps_countries = read_temps()
    temps_countries_10y = pd.concat([temps_countries['year'], temps_countries.iloc[:,2:].rolling(120).mean()], axis=1)

    co2_global, co2_countries = read_co2()
    co2_countries_10y = pd.concat([co2_countries['year'], co2_countries.iloc[:,2:].rolling(120).mean()], axis=1)
    
    
    st.header("Qu'est-ce que le réchauffement climatique?")
    
    st.markdown(
        """
Le réchauffement climatique est un phénomène de changement climatique caractérisé par une augmentation générale 
des températures moyennes à la surface de la Terre, qui modifie l'équilibre climatique et les écosystèmes.
        """
    )

    st.header('Pouvons-nous confirmer le phénomène de changement climatique ?')

    st.markdown(
        """
Commençons notre analyse en tentant de confirmer ce phénomène. A cet effet, à partir des données du data set: 
`global_land` nous présentons un graphique sur l'évolution des températures mensuelles globales, de 1750 à 2021. 
Egalement, nous allons présenter la moyenne annuelle glissante sur l'ensemble des données du même data set, 
rendant plus visible la tendance générale :

        """
    )

    st.pyplot(fig=plot_year(temps_globales, 'Evolution des températures globales par mois'))
    
    st.markdown(
        """
Nous pouvons observer des variations saisonnières correspondant à chaque année, matérialisées par les bandes de 
couleurs pour chaque variation annuelle de température. Également, une tendance croissante est visible en suivant 
les points d'une même couleur (i.e. les valeurs saisonnières augmentent globalement).  

Approximativement, jusqu'à la moitié du graphique (année 1880) la dispersion des bandes de couleurs est beaucoup 
plus importante, qui s'accompagne d'une plus grande incertitude. Les données collectées à cette époque sont moins 
fiables, à cause des capteurs utilisés et d'un nombre de stations météorologiques restreint. Cette incertitude 
est clairement représentée dans le graphique suivant, obtenu à partir du même data set : 

        """
    )

    st.pyplot(fig=plot_year(temps_globales[:-1], 
                            'Evolution des températures globales (surface terres uniquement) par an, avec incertitude',
                            show_uncert=True)
              )
    
    st.markdown(
        """
La tendance est encore plus visible sur la moyenne annuelle glissante : si jusqu'en 1880 la moyenne oscillait autour 
de 8 °C, elle remonte sur les dernières décennies autour de 10 °C. Nous pouvons identifier une augmentation 
approximative de 2 °C en à peine plus d'un siècle. 

Bien que cette valeur puisse paraître relativement petite (au vu, par exemple, des oscillations de la température 
                                                           entre jour et nuit, ou même été et hiver), les conséquences 
sur l'équilibre global sont énormes.

Afin de mieux se rendre compte de cette tendance, et pour lisser un peu les variations annuelles que l'on peut observer, 
nous calculons et présentons sur le graphique suivant une moyenne glissante sur 10 ans:
        """
    )


    st.markdown(
        """
Les premières années sont assez chaotiques, cela étant directement lié à l'incertitude que nous avons déjà observée. À 
partir de ces observations, nous sélectionnons une période plus stable, par exemple à partir des années 1850, et calculons 
les différences avec les 10 dernières années :
    • La différence de température moyenne sur 10 ans entre 1850 et 2022 est de 1.943°C.
    • La différence de température moyenne sur 10 ans entre 1900 et 2022 est de 1.63°C.

Donc, **oui, le réchauffement climatique est bel et bien une réalité** !

        """
    )


    
