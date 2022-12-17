import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


title = "Phenomenon confirmation"
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
    Plot 12-months rolling average temperature.
    """
    # Set the figure size and grid.
    plt.figure(figsize=(24, 10))
    plt.grid(color='grey', alpha=0.2)

    # Display line for monthly measures
    plt.plot(df['date'], df['abs'], c='lightgrey', zorder=1)
    # Display points (circles) for monthly measures
    plt.scatter(df['date'], df['abs'], c=df['abs'], cmap='jet', s=15, zorder=2,
                label='Monthly averages')
    # Display 12-months rolling average as a straight, larger line.
    plt.plot(df['date'], df['mov_average'], color='k',
             linewidth=2, label='12 months rolling average')

    # Add the cmap.
    plt.colorbar()
    plt.clim(df['abs'].min(), df['abs'].max())

    # Labels, legend, title.
    plt.xlabel('Date (by month)')
    plt.ylabel('Absolute temperature in °C')
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
                    edgecolor='none', zorder=2, label='Annual averages')
        plt.fill_between(temp_year['year'],
                         temp_year['abs'] - temp_year['uncert'],
                         temp_year['abs'] + temp_year['uncert'],
                         color='#D3D3D3', 
                         zorder=0, label='Uncertainty')
        # Otherwise display absolute temps with a colormap.
    else:
        plt.scatter(temp_year['year'], temp_year['abs'], c=temp_year['abs'],
                    cmap='jet', vmin=-40.5, vmax=40, edgecolor='none', 
                    zorder=2, label='Annual averages')
        plt.colorbar()
        plt.clim(temp_year['abs'].min(), temp_year['abs'].max())

    # Labels, legend, title.
    plt.xlabel('Date (by year')
    plt.ylabel('Absolute temperature in °C')
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

    st.header('Can we confirm the climate change phenomenon?')

    st.markdown(
        """
Let's start our analysis by trying to confirm this phenomenon. For this purpose, from the `global_land` data set we
present a graph showing the evolution of global monthly temperatures, from 1750 to 2021.
Also, we will present the rolling annual average over the whole data set, making the general trend more visible:
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

    uncert = st.checkbox("Include uncertainty", key='temps_globales_uncert')
    st.pyplot(fig=plot_year(temps_globales.iloc[:-1,:],
                            'Annual global temperatures', show_uncert=uncert))

    st.markdown(
        """
We can observe, despite local variations, a visible growing trend. Since the 1850s, the visible average has risen between 
1.5 and 2°C.

Up to half of the graph (year 1880) the temperature variability is much greater, and it is accompanied by greater 
uncertainty: the data collected at this time are less reliable, because of the sensors used and a limited number of 
meteorological stations. This uncertainty and its correlation to the fluctuations during the first decades is clearly 
represented on the graph (by clicking on the option).

        """
    )
    
    st.markdown(
        """
It is not possible to establish precisely the beginning of global warming. It is even a subject of disagreement between 
experts: some research correlates it with the Western industrial revolution, such as the work of Abram et al. or those 
of the PAGES group. Other studies indicate an earlier onset.

Global warming is very gradual, and undergoes cyclical variations that make precise dating difficult. Nevertheless, by 
studying the graph again, we can observe a much more explicit, strong and continuous trend from the years 1975. In the 
decades preceding the 1970s, the global average temperatures even seem to be quite stable, which caused [strong controversies](https://www.lemonde.fr/cop21/article/2015/10/22/hoax-climatique-3-dans-les-annees-1970-les-scientifiques-prevoyaient-un-refroidissement_4794858_4527432.html) 
at the time.
        """
    )

    st.markdown(
        """
To make things easier to identify, we select a more stable period, for example from the 1850s, and calculate the 
differences with the later years:
* The 10-year average temperature difference between 1850 and 2022 is 1.943°C.
* The 10-year average temperature difference between 1900 and 2022 is 1.63°C.

So, **yes, global warming is indeed a reality**!

        """
    )
        
    st.header('Does warming start at the same time all over the globe?')
    
    st.markdown(
        """
Let's visualize the evolution of temperature in different parts of the world, starting with the northern and southern 
hemispheres. In order to obtain a smoother curve, and more readable measurements, we calculate a rolling average over 10 years:        """
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
    hems_mov_average_10y['north_abs_10y_centered'].plot(label='Northern hemisphere')
    hems_mov_average_10y['south_abs_10y_centered'].plot(label='Southern hemisphere')
    plt.title('Temperature by terrestrial hemisphere - 10 years rolling average, centered')
    plt.legend()
    plt.grid()
    st.pyplot(fig)
    
    st.markdown(
        """
As for global temperatures, in this graph by hemisphere we cannot precisely identify a starting point for global warming. 
Both hemispheres show an increasing trend, but their behavior is different between one and the other. The temperature 
rise in the southern hemisphere is gradual and constant, while significant variations appear in the northern hemisphere.

Over this last period (1970 - 2021), the average temperature increases from 16.9°C to 18°C in the southern hemisphere, 
i.e. a 1.1°C increase, while the temperature increases from 10°C to 11.8°C in the northern hemisphere, i.e. a 1.8°C increase
over the same period.

Because of these variations, it is difficult to confirm whether the warming started earlier in one hemisphere than in the 
other, but globally we can observe **a faster warming of the northern hemisphere**.

In order to validate this interpretation, we will focus on the evolution of temperatures in the different countries and 
continents. In the following graph, we define two groups of countries, which we visualize with different line styles. This 
allows to visualize, and identify, similar evolutions by region -- in our case, by hemisphere. 

You can choose other sets of countries to visualize other geographical comparisons (e.g. between continents).
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
    
    countries1 = st.multiselect("Group 1 countries", 
                               temps_countries_year_centered.columns[1:],
                               default=selected_countries_n,
                               key='countries_1')
    countries2 = st.multiselect("Group 2 countries", 
                               temps_countries_year_centered.columns[1:],
                               default=selected_countries_s,
                               key='countries_2')


    if len(countries1) == 0 or len(countries2) == 0: 
        st.markdown("**Warning**: Select at least one country for each group.")
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
We find on this graph the previously observed elements: the warming is faster in the northern hemisphere (solid lines) 
than in the southern hemisphere (dotted lines). On all the selected countries, we can even observe that the more the 
countries are located in the North, the more the temperature difference is visible.

        """
    )

    st.header('Geographical evolution')

    st.subheader('Global temperature')
    
    st.markdown(
        """
Let's visualize the evolution of temperatures in all the countries where the data could be collected. The following 
graph allows you to navigate through time, from the first measurements (1743) to the most recent (2020). Missing data 
are displayed in gray, and the color scale does not vary to allow better comparison.

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
    annee = st.slider("Choose year", 
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
    ax1.set_title('Land temperatures', fontsize=25)
    st.pyplot(fig)

    st.markdown(
        """
The increase is visible; many countries took on a deeper hue in 2010 -- almost all countries took on at least one darker color hue.

        """
    )

    st.subheader('Difference over a century')

    st.markdown(
        """
We want to identify the temperature increase in all countries, taking the temperatures observed at the beginning of the 
previous century (1900) as a reference and comparing them to the temperatures observed on a chosen date..

        """
    )

    
    annee = st.slider("Choose year", 
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
    plt.title('Temperature difference', fontsize=25)
    st.pyplot(fig)

    st.markdown(
        """
Again, we find the previous observations: the increase in temperature is on average greater in the northern hemisphere, and 
increases globally going up towards the North. This is not uniform, however, we know that climatology is a complex science, 
and local parameters (local environment, or regulations of certain countries) as much as systemic (global effects of the 
climate such as the modification of oceanic and atmospheric currents) must be taken into account.
        """
    )


