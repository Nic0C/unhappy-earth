import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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
#        [temps_countries['year'], temps_countries.iloc[:, 2:].rolling(120).mean()], axis=1)
#    temps_globales['uncert_abs'] = temps_globales['abs'] + temps_globales['uncert']
    temps_globales['uncert_mov_average'] = temps_globales['mov_average'] + temps_globales['uncert']
#    temps_globales_10y = pd.concat(
#        [temps_globales['year'], temps_globales.iloc[:, 3:].rolling(120).mean()], axis=1)

    co2_global, co2_countries = read_co2()
#    co2_countries_10y = pd.concat(
#        [co2_countries['year'], co2_countries.iloc[:, 2:].rolling(120).mean()], axis=1)

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
Nous pouvons observer, malgré les variations locales, une tendance croissante visible. Entre les années 1850, l'augmentation de moyenne visible est comprise entre 1.5 et 2 °C.

Jusqu'à la moitié du graphique (année 1880) la variabilité des températures est beaucoup plus importante, et elle
s'accompagne d'une plus grande incertitude : les données collectées à cette époque sont moins 
fiables, à cause des capteurs utilisés et d'un nombre de stations météorologiques restreint. Cette incertitude 
et sa corrélation aux fluctuations lors des premières décennies est clairement représentée sur le graphe 
(en cliquant sur l'option).

        """
    )
    
    st.markdown(
        """
Il n'est pas possible d'établir précisément le début du 
réchauffement climatique. Il s'agit même d'un sujet de désaccord entre experts : certaines recherches le 
corrèlent avec la révolution industrielle occidentale, tels que les travaux de Abram et. al. ou ceux du groupe 
PAGES. D'autres études indiquent un début plus précoce. 

Le réchauffement climatique est très graduel, et subit des variations cycliques qui rendent difficile une 
datation précise. Néanmoins, en étudiant à nouveau le graphique, nous pouvons observer une tendance beaucoup 
plus explicite, forte et continue à partir des années 1975. Dans les décennies précédant les années 1970, les 
températures moyennes mondiales semblent même être assez stables, ce qui a suscité de [vives controverses](https://www.lemonde.fr/cop21/article/2015/10/22/hoax-climatique-3-dans-les-annees-1970-les-scientifiques-prevoyaient-un-refroidissement_4794858_4527432.html)
à l'époque.
        """
    )

    st.markdown(
        """
Pour rendre les choses plus identifiables, nous sélectionnons une période plus stable, par exemple à partir des années 1850, et 
calculons les différences avec les dernières années :
* La différence de température moyenne sur 10 ans entre 1850 et 2022 est de 1.943°C.
* La différence de température moyenne sur 10 ans entre 1900 et 2022 est de 1.63°C.

Donc, **oui, le réchauffement climatique est bel et bien une réalité** !

        """
    )
        
    st.header('Le réchauffement commence-t-il au même moment sur l’ensemble du globe ?')
    
    st.markdown(
        """
Visualisons l'évolution de la température dans différentes parties du monde, en commençant par les hémisphères Nord et Sud. Afin d'obtenir une courbe plus lisse, et des mesures plus lisibles, nous calculons une moyenne glissante sur 10 ans :
        """
    )
        
    # Moyenne glissante sur 10 ans.
    hems_mov_average_10y_na = []
    hems_mov_average_10y_nu = []
    hems_mov_average_10y_sa = []
    hems_mov_average_10y_su = []
    for i in np.arange(120, temps_hemis.shape[0]):
        i_prec = i - 120
        hems_mov_average_10y_na.append(temps_hemis.iloc[i_prec:i, 4].mean())
        hems_mov_average_10y_nu.append(temps_hemis.iloc[i_prec:i, 5].mean())
        hems_mov_average_10y_sa.append(temps_hemis.iloc[i_prec:i, 8].mean())
        hems_mov_average_10y_su.append(temps_hemis.iloc[i_prec:i, 9].mean())

    hems_mov_average_10y = pd.DataFrame({'north_abs': hems_mov_average_10y_na, 
                                         'north_uncert': hems_mov_average_10y_nu, 
                                         'south_abs': hems_mov_average_10y_sa, 
                                         'south_uncert': hems_mov_average_10y_su
                                         }, index=temps_hemis['date'][120:])
    
    hems_mov_average_10y['north_abs_10y_centered'] = hems_mov_average_10y['north_abs'] - hems_mov_average_10y['north_abs'].mean()
    hems_mov_average_10y['north_uncert_10y_centered'] = hems_mov_average_10y['north_uncert'] - hems_mov_average_10y['north_uncert'].mean()
    hems_mov_average_10y['south_abs_10y_centered'] = hems_mov_average_10y['south_abs'] - hems_mov_average_10y['south_abs'].mean()
    hems_mov_average_10y['south_uncert_10y_centered'] = hems_mov_average_10y['south_uncert'] - hems_mov_average_10y['south_uncert'].mean()
    
    fig, ax1 = plt.subplots(figsize=(18, 8))
    hems_mov_average_10y['north_abs_10y_centered'].plot(label='Hémisphère Nord')
    hems_mov_average_10y['south_abs_10y_centered'].plot(label='Hémisphère Sud')
    plt.title('Température par hémisphère terrestre - moyenne glissante sur 10 ans, centrée')
    plt.legend()
    plt.grid()
    st.pyplot(fig)
    
    st.markdown(
        """
De la même manière que pour les températures globales, dans ce graphique par hémisphère nous ne pouvons pas identifier 
avec précision un point de départ du réchauffement climatique. Les deux hémisphères montrent une tendance croissante, 
mais il est intéressant de remarquer que leur comportement est différent entre l'un et l'autre. La hausse de température 
dans l'hémisphère Sud est graduelle et constante, tandis que dans l'hémisphère Nord d'importantes variations apparaissent.

Sur cette dernière période (1970 - 2021), dans l'hémisphère Sud la température moyenne passe de 16,9 °C à 18 °C, soit une 
augmentation de 1,1 °C, tandis que dans l'hémisphère Nord la température passe de 10 °C à 11,8 °C, soit 1,8 °C d'augmentation 
sur la même periode.

A cause de ces variations, il est difficile d'établir si le réchauffement a débuté plus tôt dans un hémisphère que dans 
l'autre, mais nous pouvons observer globalement **un réchauffement plus rapide de l'hémisphère Nord**. 

Afin de valider cette interprétation, nous allons étudier plus en détail l'évolution des températures dans les différents pays et 
continents. Dans le graphique suivant, nous définissons deux groupes de pays, que nous visualisons avec des traits différents. Cela 
permet de visualiser, et d'identifier, des évolutions similaires par région -- dans notre cas, par hémisphère. 

Vous pouvez choisir d'autres ensembles de pays pour visualiser d'autres comparaisons géographiques (e.g. entre continents).
        """
    )
    
    

    # Compute yearly average
    temps_countries_year = pd.DataFrame(columns=temps_countries.iloc[:,2:].columns)
    #display(temps_countries)
    temps_countries_year = temps_countries.groupby(by='year').agg('mean')
    temps_countries_year = temps_countries_year.reset_index()
    
    #display(temps_countries_year)
    for c in temps_countries_year.columns[1:]:
      temps_countries_year[c] = temps_countries_year[c].rolling(10).mean()
    
    temps_countries_year_centered = temps_countries_year.copy()
    for c in temps_countries_year.columns:
      temps_countries_year_centered[c] = temps_countries_year[c] - temps_countries_year[c].mean()
    
    selected_countries_n = ['sudan', 'united-states-of-america', 
                          'greenland', 'russia', 'china']
    selected_countries_s = ['brazil', 'australia', 'antarctica']
    
    countries1 = st.multiselect("Pays groupe 1", 
                               temps_countries_year_centered.columns[1:],
                               default=selected_countries_n,
                               key='countries_1')
    countries2 = st.multiselect("Pays groupe 2", 
                               temps_countries_year_centered.columns[1:],
                               default=selected_countries_s,
                               key='countries_2')


    if len(countries1) == 0 or len(countries2) == 0: 
        st.markdown("Attention : Selectionner au moins un pays pour chaque groupe.")
    else :
        fig, ax1 = plt.subplots(figsize=(18, 8))
        #plt.ylim(-.5, 2)
        for c in countries1:
            plt.plot(temps_countries_year['year'], temps_countries_year_centered[c], alpha=.5, label=c, linestyle='-')
        for c in countries2:
            plt.plot(temps_countries_year['year'], temps_countries_year_centered[c], alpha=.7, label=c, linestyle=':')
        plt.legend()
        plt.grid()
        st.pyplot(fig)


    st.markdown(
        """
Nous retrouvons sur ce graphique les éléments observés précédemment : le réchauffement est plus rapide dans 
l'hémisphère nord (courbes en trait plein) que dans l'hémisphère sud (courbes en trait pointillé). Sur 
l'ensemble des pays sélectionnés, on peut même observer que plus les pays sont situés au Nord, plus la différence 
de température est visible.
        """
    )

    st.header('Evolution géographique')

    st.subheader('Température mondiale')
    
    st.markdown(
        """
Visualisons l'évolution des températures dans l'ensemble des pays du monde pour lesquels les données ont pu être 
collectées. Le graphique suivant permet de naviguer dans le temps, des premières mesures (1743) aux plus récentes 
(2020). Les données manquantes sont affichées en gris, et l'échelle de couleurs ne varie pas pour permettre une meilleure comparaison.

        """
    )
    
        
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
    annee = st.slider("Choisir l'année", 
                      temps_countries_from, 
                      temps_countries_to, 
                      1900, key='temps_annee')
    
    
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

    st.markdown(
        """
L'augmentation est visible ; beaucoup de pays ont une couleur plus prononcée en 2010 -- la quasi-totalité des 
pays a pris au moins une teinte de couleur plus sombre.

        """
    )

    st.subheader('Différence sur un siècle')

    st.markdown(
        """
Nous voulons identifier l'augmentation de température sur l'ensemble des pays, en prenant comme référence les 
températures observées au début du siècle précédent (1900) et en les comparant aux températures observées à 
une date choisie).

        """
    )

    
    annee = st.slider("Choisir l'année", 
                      1900, 
                      temps_countries_to, 2014, key='temps_annee_diff')
    merge['diff'] = merge[annee] - merge[1900]

    # plot world map 
    fig, ax1 = plt.subplots(figsize=(14, 12))
    merge.plot(ax=ax1, column='diff', 
               legend=True, cmap='YlOrRd',
               missing_kwds= dict(color="lightgrey",), 
               edgecolor='darkgrey', linewidth=1, legend_kwds={'loc': 'lower left'},
               scheme='NaturalBreaks')
    plt.title('Différence de températures', fontsize=25)
    st.pyplot(fig)

    st.markdown(
        """
On retrouve les observations précédentes : l'augmentation de température est en moyenne plus importante dans 
l'hémisphère nord, et croît globalement en remontant vers le Nord. Cela n'est pas uniforme, cependant, et d'autres 
paramètres doivent entrer en compte. Nous savons que la climatologie est une science complexe, et des paramètres 
locaux (type environnement local, ou régulations de certains pays) autant que systémique par les effets globaux 
du climat, tels que les modifications des courants océaniques et atmosphériques.
        """
    )


