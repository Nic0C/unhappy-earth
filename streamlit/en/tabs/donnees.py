import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


title = "Data sources"
sidebar_name = "Data sources"

plt.style.use('seaborn-whitegrid')


def read_temps():
    globales = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    hemispheres = pd.read_csv('data/unhappy_earth/temperatures_hemispheres.csv')
    countries = pd.read_csv('data/unhappy_earth/temperatures_countries.csv')
    return globales, hemispheres, countries

def read_co2():
    globales = pd.read_csv('data/unhappy_earth/co2_global.csv')
    countries = pd.read_csv('data/unhappy_earth/co2_countries.csv')
    return globales, countries


def run():

    st.title(title)

    temps_globales, temps_hemis, temps_countries = read_temps()
    temps_countries_10y = pd.concat([temps_countries['year'], temps_countries.iloc[:,2:].rolling(120).mean()], axis=1)

    co2_global, co2_countries = read_co2()
    co2_countries_10y = pd.concat([co2_countries['year'], co2_countries.iloc[:,2:].rolling(120).mean()], axis=1)
    
    st.header('Identifying data sources')
    
    st.markdown(
        """
For our research we identified two main data sources: [Berkeley Earth](http://berkeleyearth.org/data/)
and [Our world in data](https://ourworldindata.org/). The datasets provided are all publicly available, under a
specific license for the first one and under the [CC-BY](https://creativecommons.org/licenses/by/4.0/legalcode) for the second.
        """)
        
    with st.expander("More about the data sources"):
        st.markdown(
        """
[Berkeley Earth](http://berkeleyearth.org/data/) is an independent American organization that provides curated and cross-validated historic temperature datasets. They rely on a variety of other data sources, including the well-known [GISTEMP](https://data.giss.nasa.gov/gistemp/) datasets published by the NASA, and provide complete and up-to-date datasets that go up to 2021. The overall dataset contains more than 19 million observations from 46,000 weather stations spread across the world.

[Our world in data](https://ourworldindata.org/) is a well-established organization providing datasets and visualisations about a range of recent hot topics, from pollution to public health and worldwide population. Their datasets are freely [available on GitHub](https://github.com/owid/), and are commonly used in [teaching and research](https://ourworldindata.org/coverage) around the world. We specifically use their $CO_2$ emission dataset, as published in [their dedicated GitHub repository](https://github.com/owid/co2-data).
        """
        )

    st.header('Temperature datasets')

    st.markdown(
        """
**Berkeley Earth** datasets are provided as a set of **txt files**, corresponding to **monthly global world data**, **monthly data by hemispheres** and **monthly data by countries**. 

All original files have a similar format. Each txt file include a description of the dataset, including a special table with **reference data**: set of monthly average measures on a specific time range (**from January 1951 to December 1980**). This time period was selected on one hand for the reliability and completeness of the existing observations, and on the other, it represents a sort of median of the whole dataset.  

Thereafter, the main dataset follow, which is a space-separated table of 12 columns:
* The first four columns give us the information about the year, month, temperature anomalies and their uncertainty.
* The last 8 columns provide centered moving averages over 1, 5, 10 and 20 years. As an example, the yearly moving average for 1950 (January-December) is reported for June 1950. As a consequence we can observe NaNs at the top and bottom of the dataset.    
    
The time range differs from one dataset to another. For global temperatures the measures start from 1750 and go till the beginning of 2021.
       

      """
    )

    st.image("streamlit/en/assets/exempledata.jpg", use_column_width=True)  
    st.markdown(
        """
**Anomalies**, expressed in degrees Celsius, represent the difference,
positive or negative, between the real - absolute temperature and the corresponding average reference temperature. A positive anomaly indicates that the observed temperature was warmer than the reference value, while a negative anomaly indicates that the observed temperature was cooler than the reference value. More
information on this measurement and the interest of reasoning in terms of anomalies can be found [on the
NASA website](https://data.giss.nasa.gov/gistemp/faq/abs_temp.html).

**Uncertainty** is the dispersion related to various factors, in particular to geographical and statistical under-sampling, ultimately influencing the quality of the measurement. It represents the 95% confidence interval. 

**Using the above data we are able to recalculate and obtain the temperature in absolute values.**
        """
    )

    with st.expander("More about the datasets"):
        tab1, tab2, tab3 = st.tabs(["Global Temperatures", 
                                    "Temperature by hemisphere", 
                                    "Temperatures by country"])
        with tab1:
            st.dataframe(temps_globales.tail(10))
        with tab2:
            st.dataframe(temps_hemis.tail(10))
        with tab3:
            st.dataframe(temps_countries.tail(10))
   

    st.markdown(
        """
We can visualise the evolution of temperatures across the 180 countries of the dataset: please select any item in the list.
        """
    )
      
    # Add country selection
    options = st.multiselect(
        'Select a country',
        temps_countries.columns[2:],
        ['france', 'united-states-of-america', 'china'],
        key = "temps_countries")

    if len(options) == 0 : 
        st.markdown("Warning: please select at least one country.")
    else :
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(temps_countries_10y['year'], temps_countries_10y[options], label=options)
        ax.set_ylim(bottom=0)
        ax.grid(visible=True, alpha=0.5)
        ax.legend(loc='lower left')
        ax.set_title("10 years moving average temperature by country")
        st.pyplot(fig=fig, )
        
        
    st.header('Carbon dioxyde datasets')

    st.markdown(
        """
We identify two datasets for the Carbon dioxyde analysis. The first one is the yearly total emission of $CO_2$ by country, and the second one details annual worldwide emissions associated to *land use* and *fossil fuel and industry*.
        """
        )

    with st.expander("More about the datasets"):
        tab1, tab2 = st.tabs(["CO2 emissions, worldwide", 
                              "CO2 emissions, by country"])
        with tab1:
            st.dataframe(co2_global.tail(10))
        with tab2:
            st.dataframe(co2_countries.tail(10))

    st.markdown(
        """
Countries are identified according to their ISO 3166 - alpha-3 code. As for the temperatures, there are missing values for some countries over some time ranges.
        """
    )

    st.markdown(
        """
We can visualise the evolution of $CO_2$ emissions by country. Please select the countries of your choice in the list to display them. `OWID_WRL` displays the overall worldwide emissions.
        """
    )
    
    # Add country selection
    options = st.multiselect(
        'Select a country',
        co2_countries.columns[1:],
        default=['FRA', 'USA', 'CHN', 'OWID_WRL'],
        key="co2_countries")

    if len(options) == 0 : 
        st.markdown("Warning: please select at least one country.")
    else :
        fig, ax = plt.subplots(figsize=(10,6))
        ax.plot(co2_countries['year'], co2_countries[options], label=options)
        ax.set_ylim(bottom=0)
        ax.grid(visible=True, alpha=0.5)
        ax.legend(loc='lower left')
        ax.set_title("Yearly $CO_2$ emissions, by country")
        st.pyplot(fig=fig)
        
    st.markdown(
        """

**Global $CO_2$ data** provides us with another information: the amount of $CO_2$ emitted by land use, 
in addition to the generation of $CO_2$ related to energy and industrial production. Land, depending on its use, 
produces a certain amount of $CO_2$ which is added to industrial production; in some cases the land can also consume it, 
so we can see negative values on this measure.

Let's visualize the evolution of these two values (expressed in Gigatons) over the measurement period.
        """
    )
    
    # Add country selection
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(co2_global['Year'], co2_global['Land use emissions (GtCO2)'], label='Land use emissions (GtCO2)')
    ax.plot(co2_global['Year'], co2_global['Fossil fuel and industry emissions (GtCO2)'], label='Fossil fuel and industry emissions (GtCO2)')
#    ax.plot(co2_countries['year'], co2_countries['OWID_WRL'], label='Total global')
    ax.set_ylim(bottom=0)
    ax.grid(visible=True, alpha=0.5)
    ax.legend(loc='upper left')
    ax.set_title("Global $CO_2$ production, per year")
    st.pyplot(fig=fig)
        

    st.header('Reading and pre-processing of data')

    st.subheader('Reading')

    st.markdown(
        """
Most of our datasets include NaNs; we identify them and decide whether to maintain or replace them on 
a case-by-case basis.
* For the **global temperatures**, it is rare that no sensor is available at a planet level and the few existing NaNs 
  are at the very beginning of the dataset, in the years 1751/1752. We identify only 3 non-consecutive lines with NaNs 
  and we decide to replace them using linear interpolation. 
  
* For **temperatures by hemisphere**, there is only one missing value on the northern hemisphere and 2 on the 
  southern hemisphere dataset. Identically as in the previous case, we use linear interpolation to replace these 
  values based on their continuity. It should also be noted that the start date of the two datasets is different:
  1840 for the North hemisphere and 1880 for the South.
  
* Still for the temperatures by hemisphere, we also calculate a mooving average over 12 months, which makes 
  possible to smooth out seasonal variations and to obtain more readable curves.
  
* For **temperatures by country**, many lines of dataset contain NaNs - it can be due to different reasons as the 
  late temperature sensor installation, or to periods of geopolitical instability. The missing values 
  which are spread over large periods of time – correspond for example to the duration of a war or the autarky of a country. 
  Therefore we cannot use interpolation to replace NaNs, so we decide to keep them as they are.
  

The **$CO_2$ information by country** is available in CSV format; idem as with the previous dataset "temperatures by country", 
the missing values are related to periods when the country, for whatever reason, could not collect the data. These holes 
represent significant time ranges, and we decide to keep them untouchable with the aim of not to compromise the statistical 
integrity of the data.

        """
    )

    st.subheader('Data aggregation')

    st.markdown(
        """
We proceeded to the dataset cleaning in order to facilitate their use. For this purpose we use the CSV format,
which can be easily imported into other tools (example: Excel) and it is easier to handle with rather than the original text files.

Also, the information by hemisphere and by country originally comes in separate files (by each hemisphere in the first case, 
and by each country in the second). In order to facilitate their reading, analysis and use, we aggregate them together to
obtain a unified and consistent dataset (one file for the hemispheres, and one file for all countries).
The generated files are available below :
* [global_temperatures.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/temperatures_globales.csv) provides global temperatures,
* [temperatures_by_hemisphere.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/temperatures_hemispheres.csv) provides temperatures for both hemisphere,
* [temperatures_by_country.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/temperatures_countries.csv) provides temperatures for each country,
* [co2_global.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/co2_global.csv) provides global $CO_2$ production,
* [co2_countries.csv](https://github.com/borisbaldassari/unhappy-earth/tree/main/data/unhappy_earth/co2_countries.csv) provides $CO_2$ production for each country.
        """
    )
        
    st.markdown(
        """
        <br />
        
        ----
        """,
    unsafe_allow_html=True
    )
