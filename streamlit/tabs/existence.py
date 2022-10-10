import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


title = "Confirmation du phénomène"
sidebar_name = "Confirmation"


def read_temps():
    globales = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    hemispheres = pd.read_csv(
        'data/unhappy_earth/temperatures_hemispheres.csv')
    countries = pd.read_csv('data/unhappy_earth/temperatures_countries.csv')
    return globales, hemispheres, countries


def read_co2():
    globales = pd.read_csv('data/unhappy_earth/co2_global.csv')
    countries = pd.read_csv('data/unhappy_earth/co2_countries.csv')
    return globales, countries


def plot_month(df, title):
    """
    Display both a plot and a scatter plot from a DF, with x = date (by month) and y = absolute temperature.
    Add a cmap to colorize the scatter based on y value.
    Plot 12-months moving average temperature.
    """
    # Set the figure size and grid.
    plt.figure(figsize=(24, 10))
    plt.grid(color='grey', alpha=0.2)

    # Display line for monthly measures
    plt.plot(df['date'], df['abs'], c='lightgrey', zorder=1)
    # Display points (circles) for monthly measures
    plt.scatter(df['date'], df['abs'], c=df['abs'], cmap='jet', s=15, zorder=2,
                label='Moyennes mensuelles')
    # Display 12-months moving average as a straight, larger line.
    plt.plot(df['date'], df['mov_average'], color='k',
             linewidth=2, label='Moyenne glissante sur 12 mois')

    # Add the cmap.
    plt.colorbar()
    plt.clim(df['abs'].min(), df['abs'].max())

    # Labels, legend, title.
    plt.xlabel('Date (par mois)')
    plt.ylabel('Température absolue en °C')
    plt.legend()
    plt.title(title)

    return plt


def plot_year(df, title, show_uncert=False):
    """
    Display both a plot and a scatter plot from a DF, with x = date (by year) and y = absolute temperature.
    The 'show_uncert' parameter allows, if True, to display the uncertainty margin.
    Add a cmap to colorize the scatter plot based on y value, when uncertainty is not plotted.
    """
    # Compute the average of abs and uncert by year.
    temp_year = df[['year', 'abs', 'uncert']].groupby(
        'year').mean().reset_index()
    # Set the figure size and grid.
    plt.figure(figsize=(12, 5))
    plt.grid(color='grey', alpha=0.2)

    # Display absolute temperatures.
    plt.plot(temp_year['year'], temp_year['abs'], c='grey', zorder=1)

    # If required, display points and fill the area of uncertainty measures.
    if show_uncert == True:
        plt.scatter(temp_year['year'], temp_year['abs'],
                    edgecolor='none', zorder=2, label='Moyennes annuelles')
        plt.fill_between(temp_year['year'],
                         temp_year['abs'] - temp_year['uncert'],
                         temp_year['abs'] + temp_year['uncert'],
                         color='#D3D3D3', 
                         zorder=0, label='Incertitude')
        # Otherwise display absolute temps with a colormap.
    else:
        plt.scatter(temp_year['year'], temp_year['abs'], c=temp_year['abs'],
                    cmap='jet', vmin=-40.5, vmax=40, edgecolor='none', 
                    zorder=2, label='Moyennes annuelles')
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
    temps_countries_10y = pd.concat(
        [temps_countries['year'], temps_countries.iloc[:, 2:].rolling(120).mean()], axis=1)
    temps_globales['uncert_abs'] = temps_globales['abs'] + temps_globales['uncert']
    temps_globales['uncert_mov_average'] = temps_globales['mov_average'] + temps_globales['uncert']
    temps_globales_10y = pd.concat(
        [temps_globales['year'], temps_globales.iloc[:, 3:].rolling(120).mean()], axis=1)

    co2_global, co2_countries = read_co2()
    co2_countries_10y = pd.concat(
        [co2_countries['year'], co2_countries.iloc[:, 2:].rolling(120).mean()], axis=1)

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

    # mesures = st.multiselect("Sélectionner les mesures", 
    #     temps_globales.columns[3:],
    #     default=['abs', 'mov_average'],
    #     key='temps_globales')


    # if len(mesures) == 0 : 
    #     st.markdown("Attention : Selectionner au moins un pays !")
    # else :
    #     fig, ax = plt.subplots(figsize=(10, 6))
    #     ax.plot(temps_globales['year'], temps_globales[mesures], label=mesures)
    #     ax.set_ylim(bottom=0)
    #     ax.grid(visible=True, alpha=0.5)
    # #    ax.legend(loc='lower left')
    #     ax.set_title("Températures globales, moyenne sur 10 ans")
    #     st.pyplot(fig=fig, )

    uncert = st.checkbox("Inclure l'incertitude", key='temps_globales_uncert')
    st.pyplot(fig=plot_year(temps_globales.iloc[:-1,:],
                            'Températures globales annuelles', show_uncert=uncert))

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

    st.header('Evolution géographique')

    st.markdown(
        """
Afin de mieux appréhender les différences de température au niveau mondial et à l'aide de l’outil geopandas (projet 
source intégré à la librairie pandas), nous visualisons les températures dans l'ensemble des pays du monde (pour lesquels 
nous avons des données dans le data set “temp_countries”) au début du siècle dernier, en 1900, et aujourd'hui (données 
accessibles jusqu'en 2020). Nous utilisons la même échelle de couleur pour permettre une bonne comparaison :

        """
    )
    
    
    

    # Compute yearly average
    temps_countries_year = pd.DataFrame(columns=temps_countries.iloc[:,2:].columns)
    #display(temps_countries)
    temps_countries_year = temps_countries.groupby(by='year').agg('mean')
#    for c in temps_countries.iloc[:,2:]:
#      temps_countries_year[c] = temps_countries.groupby(by='year').agg({c: 'mean'})
    temps_countries_year = temps_countries_year.reset_index()
    
    #display(temps_countries_year)
    for c in temps_countries_year.columns[1:]:
      temps_countries_year[c] = temps_countries_year[c].rolling(10).mean()
    
    temps_countries_year_centered = temps_countries_year.copy()
    for c in temps_countries_year.columns:
      temps_countries_year_centered[c] = temps_countries_year[c] - temps_countries_year[c].mean()

        
    import geopandas as gpd
    
    # get the geometry (and some more info) about countries.
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    # rename the columns so that we can merge with our data
    world.columns=['pop_est', 'continent', 'name', 'CODE', 'gdp_md_est', 'geometry']
    # Fix some bugs/missing codes in pycountry
    world['CODE'].loc[world['name'] == 'France'] = 'FRA'
    world['CODE'].loc[world['name'] == 'Norway'] = 'NOR'
    
    # Build our dataframe with proper formatting.
    df_geo = temps_countries_year.set_index('year').T.reset_index().rename(columns={'index': 'CODE'})
    
    # pycountry lookup doesn't recognise some country name, help it a bit.
    df_geo['CODE'] = df_geo['CODE'].replace({
        'russia': 'Russian Federation',
        'united-states-of-america': 'United States',
        'united-kingdom': 'United Kingdom',
        'syria': 'Syrian Arab Republic',
        'central-african-republic': 'Central African Republic',
        'south-africa': 'South Africa',
        'federated-states-of-micronesia': 'Micronesia, Federated States of',
        'iran': 'Iran, Islamic Republic of',
        'islas-baleares': 'islas-baleares',
        'laos': "Lao People's Democratic Republic",
        'timor': 'Timor-Leste',
        'south-korea': "Korea, Republic of",
        'north-korea': "Korea, Democratic People's Republic of",
        'cabo-verde': 'Cabo Verde',
        'costa-rica': 'Costa Rica',
        'saudi-arabia': 'Saudi Arabia',
        'bosnia-and-herzegovina': 'Bosnia and Herzegovina',
        'reunion': 'Réunion',
        'new-zealand': 'New Zealand',
        })

    
    # convert countries to 3-letter code
    import pycountry
    remove_rows = []
    for i, v in enumerate(df_geo['CODE']):
        try:
          c = pycountry.countries.lookup(v)
          df_geo.iloc[i, 0] = c.alpha_3
        except Exception:
          #display(f"Could not find country {v}.")
          remove_rows.append(i)
    df_geo = df_geo.drop(index=remove_rows, axis=0)
    
    # then merge with our data 
    merge = pd.merge(world, df_geo, on='CODE', how='outer')
    
    
    from matplotlib.colors import Normalize
    from mapclassify import UserDefined
    
    temps_countries_from, temps_countries_to = int(temps_countries.iloc[0, 1]), int(temps_countries.iloc[-1, 1])
    annee = st.slider("Choisir l'année", temps_countries_from, temps_countries_to, 1900)
    
    
    bins = UserDefined(merge[annee], bins=[0,3,5,7,9,11,13,15,17,19,21,23,25,27]).bins
    fig, ax1 = plt.subplots(figsize=(14, 12))
    # plot world map 
    merge.plot(ax=ax1, column=annee,
               legend=True, cmap='YlOrRd',
               missing_kwds= dict(color="lightgrey",), 
               edgecolor='darkgrey', linewidth=1, legend_kwds={'loc': 'lower left'},
               scheme='userdefined', classification_kwds={'bins':bins}, norm=Normalize(0, len(bins)), vmin=-20, vmax=23)
    ax1.set_title('Températures des terres', fontsize=25)
    
    st.pyplot(fig)