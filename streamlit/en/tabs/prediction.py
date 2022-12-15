import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet


title = "Forecast"
sidebar_name = "Forecast"


def run():

    st.image("streamlit/en/assets/station_meteo.jpg", use_column_width=True)    

#Importer les donnes:
    df = pd.read_csv('data/unhappy_earth/temperatures_globales.csv')
    
    st.title("Modeling / Temperature Forecast over the next decades.")
    
    st.markdown("---")
    
    st.subheader("Can we predict the temperature over the upcoming years?")
    
    st.markdown("To build a temperature prediction for the next decades, we decided to choose Facebook Prophet among multiple existing models to forecast time series. We consider that Prophet is quite simple to understand, comparing to other models, it is easy to apply and it adapts perfectly to our data and to our objective. Then, the two methods inside the model to analyze the seasonality of a Time Series are basically: additive (tends to show a linear trend) and multiplicative (exponential trend). We tested both of them and we saw that the additive method gives better results, so we proceeded with it.")
    
    st.markdown("Regarding the data used to train the model: we select just the period when the absolute temperature trend is increasing, constant and explicit. In the following graph we clearly see that this is the period between 1975 and 2022.")

    col1, col2 = st.columns(2)
    col1.metric("Temperature 1975", "8.7 °C")
    col2.metric("Temperature 2022", "10 °C", "1.3 °C")

    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: center;
    }
    </style>
    ''', unsafe_allow_html=True)

#Definition des donnes a traiter: 
    new_column = df.loc[(df['date'] >= '1975-01-15')] 
    new_column = new_column[['date', 'abs']] 
    new_column.dropna(inplace=True)
    new_column.columns = ['ds', 'y'] 

# Affichage graphe evolution températures / tendance:
    fig, ax1 = plt.subplots(figsize=(16,4))
    formatter = mdates.DateFormatter("%Y") ### formatter of the date
    
    ax1.xaxis.set_major_formatter(formatter) ## calling the formatter for the x-axis   
    
    ax1.plot(mdates.date2num(new_column['ds']), new_column['y'], label="Absolute Temperature")    

    x = mdates.date2num(new_column['ds'])
    z = np.polyfit(x, new_column['y'], 1)
    p = np.poly1d(z)
     
    ax1.plot(x,p(x),"r--", label="Trend")
    ax1.set_xlabel("Date (by year)", fontsize=14)
    ax1.set_ylabel("Absolute Temperature in °C", fontsize=14)
    plt.title("Absolute Temperature between 1975 and 2022 (monthly data)", fontsize=18)
    plt.grid(color='grey', alpha=0.2)

    fig.legend(loc='upper center', bbox_to_anchor=(0.20, 0.91))
    
    st.pyplot(fig)


#Prediction Prophet    
    st.markdown("From our data, Facebook Prophet calculates the following temperature forecast over the next 50 years:")


    m = Prophet(seasonality_mode='additive').fit(new_column)
    future = m.make_future_dataframe(periods=600, freq='M')
    fcst = m.predict(future)
    fig = m.plot(fcst, figsize=(16,6), xlabel ='Date (by year)', ylabel='Absolute Temperature in °C')
    axes = fig.get_axes()

    axes[0].set_xlabel('Date (by year)', fontsize=18)
    axes[0].set_ylabel('Absolute Temperature in °C', fontsize=18)

    fig.suptitle("Temperature forecast over the next 50 years",  y=1.02, fontsize=24)
    import warnings
    warnings.filterwarnings("ignore")
    st.pyplot(fig)

    st.markdown("The forecast (which starts from year 2022 on this graph) shows a clear increasing evolution of the temperature.")

#Presentation des components: tendance et la déviation
    st.markdown("For more detail, we visualize 2 components of the prediction:")
    st.markdown("- **The trend** ;")
    st.markdown("- **Seasonal deviation** from the trend :")
    
    fig = m.plot_components(fcst, figsize=(18, 10))
    fig.suptitle("Trend forecast of the absolute temperature and seasonal deviation", y=1.02, fontsize=24)
    axes = fig.get_axes()

    axes[0].set_xlabel('Date (by year)', fontsize=18)
    axes[0].set_ylabel('Absolute Temperature in °C', fontsize=18)
    axes[1].set_xlabel("Month", fontsize=18)
    axes[1].set_ylabel('Seasonal temp deviation / trend, in°C', fontsize=18)
    warnings.filterwarnings("ignore")
    
    st.pyplot(fig)

#Conclusion

    col1, col2 = st.columns(2)
    col1.metric("Temperature 2022", "10 °C")
    col2.metric("Temperature 2072", "11.9 °C", "1.9 °C")

    st.markdown('''
    <style>
    /*center metric label*/
    [data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: center;
    }

    /*center metric value*/
    [data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: center;
    }
    </style>
    ''', unsafe_allow_html=True)

    st.markdown("Our forecast is based on the premise that the absolute global temperature will follow the same trend as for the past 46 years, without major climate action. In this case, our model predicts an increase of approximately 1.9°C for the next 50 years. Comparing with a multitude of forecasting studies that currently exist, our result seems to be fair and reasonable, but far from optimistic..$^[$ $^1$ $^]$ $^,$ $^[$ $^2$ $^]$ $^,$ $^[$ $^3$ $^]$")

    st.markdown(
        """
        <br />
        
        ----
        Links to articles and researches consulted:  
         <font size="2"> $^[$ $^1$ $^]$ [La hausse de la température globale s’est encore accentuée, selon le dernier rapport du GIEC](https://www.ecologie.gouv.fr/hausse-temperature-globale-sest-encore-accentuee-selon-dernier-rapport-du-giec)  
        $^[$ $^2$ $^]$ [L'ampleur des hausses que vous connaîtrez](https://www.francelive.fr/article/france-live/vous-pouvez-desormais-savoir-le-changement-climatique-que-vous-subirez-selon-votre-age-7403908/)  
        $^[$ $^3$ $^]$ [Les prévisions alarmantes de Météo France](https://www.lefigaro.fr/sciences/rechauffement-climatique-les-previsions-alarmantes-de-meteo-france-20210201) </font>    
        
        Crédit image : Michal Osmenda, [CC-BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0),
        via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Weather_station_on_Mount_Vesuvius_(2437693238).jpg).
        """,
        unsafe_allow_html=True
        )    
    