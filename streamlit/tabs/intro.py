import streamlit as st


title = "UnhapPy Earth"
sidebar_name = "Introduction"


def run():

    # TODO: choose between one of these GIFs
    st.image("streamlit/assets/starving_polar_bear.jpg")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/2.gif")
    # st.image("https://dst-studio-template.s3.eu-west-3.amazonaws.com/3.gif")
    
    st.title(title)

    st.markdown("---")
    
    st.header("Analyse du réchauffement climatique")
    
    st.subheader("Contexte")
    st.markdown("""
                En quelques décennies à peine, la question du réchauffement climatique est devenue un sujet majeur, inquiétant pour l'avenir de la planète et de sa biodiversité, y compris l'espèce humaine. Pourtant il fait débat, oppose experts et climato-sceptiques, à l'heure même où les manifestations et les conséquences de ce changement sont chaque jour plus flagrantes.
                Ce projet nous a amenés à utiliser la plupart des compétences acquises au cours de notre formation :
                Acquisition et manipulation de jeux de données ;
                ​​Production de visualisations graphiques afin de "faire parler" ces données, et éventuellement, susciter des intuitions ;
                Construction d’algorithmes de régression et de prédiction.
                Le réchauffement climatique est incroyablement coûteux : humainement, socialement, géopolitiquement, financièrement et économiquement. Sur la dernière décennie, le coût du réchauffement climatique estimé par un rapport des Nations Unies datant de Avril 2022 est de 140 Milliards par an, et devrait atteindre 2000 Milliards d’ici 2030 – voir l’article. Anticiper et mieux comprendre ses conséquences, donc le coût économique, devient donc une priorité pour beaucoup d’entreprises et d’organisations.
                Nous voulons savoir si, grâce à la Data Analyse, nous étions en mesure d’apporter des conclusions se rapprochant de celles données par les experts en climatologie. Nous voulons mettre à disposition du public un moyen simple et vérifiable, au travers de sources factuelles et ouvertes, de constater le réchauffement climatique. 
                """)
        
    st.subheader("Objectifs")
    st.markdown("""
                Notre objectif est de proposer, à l'aide de données fiables et librement accessibles, une analyse du réchauffement climatique, en répondant aux problématiques suivantes :
                1. Pouvons-nous confirmer grâce aux données le phénomène de changement climatique ? Le réchauffement est-il réellement observable ?
                2. Quand le phénomène apparaît-il ? De manière soudaine ou graduelle ? Au même moment sur l’ensemble du globe ?
                3. Son évolution est-elle uniforme à travers le monde ou certaines zones sont-elles plus impactées que d’autres ?
                4. D'après la grande majorité des experts en climatologie, les émissions de CO2 dans l'atmosphère seraient, parmi l’ensemble des gaz à effet de serre, la principale cause du réchauffement de la planète. Quel degré de corrélation existe-t-il entre les émissions de CO2 et l’évolution des températures ?
                5. Des événements historiques ont-ils eu un impact sur l'évolution de la température ?
                6. Quelles sont nos prédictions de températures sur les prochaines années ?
                7. Par cette Data Analyse, parvenons nous à des conclusions similaires à celles des scientifiques - climatologues ?
                
                Nous avons tous entendu parler du réchauffement climatique, de ses détracteurs et des débats sur son existence. A l’heure où ses conséquences (sécheresses, pluies torrentielles à répétition) se font de plus en plus sentir, nous avons souhaité identifier les éléments factuels disponibles et faire notre propre analyse, sans avoir pour aucun d’entre nous de connaissance préalable en climatologie. Nous espérons qu’en produisant un travail reproductible et librement accessible ces informations pourront être réutilisées par d’autres personnes curieuses et non spécialistes.
                Nous avons lu nombre d’articles et de publications disponibles sur internet. Ceux-ci nous ont permis de mieux comprendre pourquoi et comment sont ainsi construits les jeux de données étudiés, ainsi que les enjeux relatifs aux problématiques citées.
        
                """)
    
    st.subheader("Classification du problème") 
    st.markdown("""
Grâce aux outils classiques de Data Analyse et de Dataviz, nous allons explorer, nettoyer, fusionner, visualiser et analyser nos données, et ainsi pouvoir répondre à nos problématiques 1, 2, 3.
Deux algorithmes de machine learning nous permettront de répondre aux problématiques 4 et 6 : 
* Une régression linéaire afin d’étudier la relation entre les quantités de CO2 émises et l’évolution des températures. Celle-ci permet d’estimer si deux variables évoluent ensemble, et sera ensuite évaluée par une métrique de performance.
* Un modèle prédictif afin de proposer une prévision de l’évolution des températures.

Enfin, c’est plutôt un travail de recherche qui nous aidera à répondre à la problématique n°5, et plus globalement, à nous assurer de l’adéquation de nos résultats avec les recherches courantes (point n°7). 

<br />
""", unsafe_allow_html=True)

    st.markdown("""
----

Crédit image : Andreas Weith, [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0), via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Endangered_arctic_-_starving_polar_bear.jpg).
                """)
            
            
