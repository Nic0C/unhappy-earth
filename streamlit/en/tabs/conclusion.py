import streamlit as st


title = "Conclusion"
sidebar_name = "Conclusion"


def run():
    
    st.image("streamlit/en/assets/Global_Warming.jpg", use_column_width=True)
    
    st.title(title)

    st.markdown("---")
# Bilan :

    st.header("Summary")    

    st.markdown(
        """
        The topics of global warming and temperature forecasting over the upcoming future are widely discussed and studied by highly qualified experts. 
        Our objective was mainly to test the knowledge that we acquired during the course of Data Analyst and see if we would be able to achieve consistent results.
        
        Thanks to the statistical analysis of reliable and concrete data, we were able to respond to the issues raised at the begging of the project:
        1.  We could confirm and quantify the global warming: it is an indisputable reality. The phenomenon is gradual since the industrial revolution of 1880, and it accelerates since 1975, especially in the northern hemisphere.  
        2.  CO2 emissions have a strong influence (correlation / linearity) on the temperature increase.  
        3.  Our predictions are not optimistic. According to the results of Prophet Model, the global average temperature will increase by almost 2°C in the next 50 years. These results are consistent with numerous studies on climate change made by professional climatologists.  
            
        Unfortunately, our conclusions, and a fortiori those of the experts in climatology, are not positive neither for 
        our planet Earth (UnhapPy Earth), nor for the humanity.
        """
        )
        
# Suite du projet :
    
    st.header("Project follow-up")
    
    st. markdown(
        """
        In order to complete our research it would be possible to analyze other causes and consequences related with global warming, in particular:
        * **Greenhouse gas emissions**  other than CO2 (methane, etc.);
        * **Evolution of the distribution between natural soils and soils exploited**  by and for human activity ;
        * **Global sea and ocean level rise** ;
        * **Frequency and intensity increase of natural disasters**.
        """
        )

# Bibliographie :

    st.header("Bibliography")
    
    biblio = st.radio("Which bibliography would you like to consult?",
                     ('Data', 'Publications, researches and articles consulted', 'Python Libraries'))
    
    if biblio == 'Data' :
        st.markdown(
            """
            * [Data Overview - Berkeley Earth](http://berkeleyearth.org/data/)
            * [GISS Surface Temperature Analysis (GISTEMP v4)](https://data.giss.nasa.gov/gistemp/)
            * [Our World in Data](https://ourworldindata.org/)
            """
            )
        
    elif biblio == 'Publications, researches and articles consulted' :
        st.markdown(
            """
            * [6e rapport du GIEC : quelles solutions face au changement climatique ? - Réseau Action Climat](https://reseauactionclimat.org/6e-rapport-du-giec-quelles-solutions-face-au-changement-climatique/)
            * [Le véritable coût du changement climatique | National Geographic](https://www.nationalgeographic.fr/environnement/2017/09/le-veritable-cout-du-changement-climatique)
            * [The Elusive Absolute Surface Air Temperature (SAT)](https://data.giss.nasa.gov/gistemp/faq/abs_temp.html)
            * [Global Carbon Project](https://www.globalcarbonproject.org/)
            * [Changement climatique et effet de serre | Insee](https://www.insee.fr/fr/statistiques/4277613)
            * [Early onset of industrial-era warming across the oceans and continents](http://rdcu.be/jVFv)
            * [Le réchauffement climatique anthropique aurait débuté au tout début de la révolution industrielle](https://www.ipsl.fr/Actualites/Actualites-scientifiques/Le-rechauffement-climatique-anthropique-aurait-debute-au-tout-debut-de-la-revolution-industrielle)
            * [Covid-19 et baisse des émissions de CO2 | Cairn.info](https://www.cairn.info/magazine-pour-la-science-2020-7-page-7.htm)
            * [Hoax climatique #3 : quand les scientifiques prévoyaient un refroidissement](https://www.lemonde.fr/cop21/article/2015/10/22/hoax-climatique-3-dans-les-annees-1970-les-scientifiques-prevoyaient-un-refroidissement_4794858_4527432.html)
            * [La hausse de la température globale s’est encore accentuée, selon le dernier rapport du GIEC](https://www.ecologie.gouv.fr/hausse-temperature-globale-sest-encore-accentuee-selon-dernier-rapport-du-giec)
            * [Réchauffement climatique : voici l'ampleur des hausses que vous connaîtrez](https://www.francelive.fr/article/france-live/vous-pouvez-desormais-savoir-le-changement-climatique-que-vous-subirez-selon-votre-age-7403908/)
            * [Réchauffement climatique : les prévisions alarmantes de Météo France](https://www.lefigaro.fr/sciences/rechauffement-climatique-les-previsions-alarmantes-de-meteo-france-20210201)
            """
            )
    else : 
        st.markdown(
            """
            * [Streamlit](https://streamlit.io/)
            * [NumPy](https://numpy.org/)
            * [pandas](https://pandas.pydata.org/)
            * [Matplotlib](https://matplotlib.org/)
            * [seaborn](https://seaborn.pydata.org/index.html)
            * [GeoPandas](https://geopandas.org/en/stable/)
            * [Pillow](https://pypi.org/project/Pillow/)
            * [scikit-learn](https://scikit-learn.org/)
            * [SciPy](https://scipy.org/)
            * [Prophet | Forecasting at scale](https://facebook.github.io/prophet/)
            """
            )

    st.markdown(
        """
        <br />
        
        ----
        
        Crédit image : Global Warming Representation, [CC-BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0),
        via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Global_Warming_Representation,_NASA_Goddard_Photo_%26_Video.jpg#file).
        """,
        unsafe_allow_html=True
        )
