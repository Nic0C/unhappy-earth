import streamlit as st


title = "Conclusion"
sidebar_name = "Conclusion"


def run():
    
    st.image("streamlit/assets/Global_Warming.jpg", use_column_width=True)
    
    st.title(title)

    st.markdown("---")
# Bilan :

    st.header("Bilan")    

    st.markdown(
        """
        Ce **sujet** est déjà connu, **largement étudié** et débattu par des experts hautement qualifiés. **Nous souhaitions** principalement
        **savoir si la Data Analyse nous permettrait d’atteindre des résultats concordants**.
        
        Grâce à l'analyse statistique de données fiables et concrètes, nous avons pu **répondre aux problématiques posées** en début de
        projet :
        1. Nous avons pu **confirmer et quantifier le réchauffement climatique : c'est une réalité indiscutable**. Le phénomène est
            graduel depuis la révolution industrielle de 1880, et s'accélère à partir de 1975, de manière plus forte encore dans
            l'hémisphère nord.
        2. **Les émissions de CO2 ont une forte influence (corrélation / linéarité)** sur la hausse des températures.
        3. Nos **prédictions** ne sont pas optimistes. D'après notre modèle Prophet, **la température moyenne globale augmentera de près
            de 2°C dans les 50 prochaines années**. Ces résultats rejoignent ceux de la majorité des études disponibles sur le
            changemen climatique.
            
        Malheureusement, nos **conclusions**, et a fortiori celles des experts en climatologie, **ne sont pas positives** ni pour notre planète
        Terre (**UnhapPy Earth**), ni pour l'humanité.
        """
        )
        
# Suite du projet :
    
    st.header("Suite du projet")
    
    st. markdown(
        """
        Afin de compléter notre étude, de **nombreux autres causes et conséquencs pourraient être analysés**, notamment :
        * **Émissions de Gaz à Effet de Serre** autres que le CO2 (méthane, etc.) ;
        * **Évolution de la répartition entre sols naturels et sols exploités** par et pour l'activité humaine ;
        * **Augmentation du niveau des mers et des océans** ;
        * **Augmentation de la fréquence et de l'intensité des catastrophes dites naturelles**.
        """
        )

# Bibliographie :

    st.header("Bibliographies")
    
    biblio = st.radio("Quelle bibliographie souhaitez-vous consulter ?",
                     ('Données', 'Publications, articles et études consultées', 'Librairies Python'))
    
    if biblio == 'Données' :
        st.markdown(
            """
            * [Data Overview - Berkeley Earth](http://berkeleyearth.org/data/)
            * [GISS Surface Temperature Analysis (GISTEMP v4)](https://data.giss.nasa.gov/gistemp/)
            * [Our World in Data](https://ourworldindata.org/)
            """
            )
        
    elif biblio == 'Publications, articles et études consultées' :
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