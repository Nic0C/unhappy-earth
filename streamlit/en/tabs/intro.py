import streamlit as st


title = "UnhapPy Earth"
sidebar_name = "Introduction"


def run():

    st.image("streamlit/assets/starving_polar_bear.jpg")

    st.title(title)

    st.markdown("---")
    
    st.header("Analyse du réchauffement climatique")
    
# Contexte :

    st.subheader("Contexte / Définition")
    
    st.markdown(
        """
        En quelques décennies à peine, **la question du réchauffement climatique est devenue un sujet majeur**, inquiétant 
        pour l'avenir de la planète et de sa biodiversité, y compris l'espèce humaine. **Pourtant il fait encore débat**, oppose 
        experts et climato-sceptiques, **à l'heure même où ses manifestations et ses conséquences** (sécheresses et pluies torrentielles,
        à répétition, montée du niveau des eaux) **sont chaque jour plus flagrantes**. En voici une définition simple, proposée par la
        plateforme média [Youmatter](https://youmatter.world/fr/) :
            
        **Le réchauffement climatique est un phénomène global de transformation du climat caractérisé par une augmentation
        générale des températures moyennes (notamment liée aux activités humaines, rejettant quantité de Gaz à Effet de Serre), et qui
        modifie durablement les équilibres météorologiques et les écosystèmes.**
        
        Par ailleurs, un [rapport des Nations Unies publié en Avril 2022](https://www.nationalgeographic.fr/environnement/2017/09/le-veritable-cout-du-changement-climatique)
        l'affirme : **le réchauffement climatique est incroyablement coûteux** : humainement, socialement, géopolitiquement,
        financièrement et économiquement.
        
        **Anticiper et mieux comprendre ses conséquences devient donc une priorité** pour beaucoup d’entreprises et d’organisations.
        """
        )

# Objectifs :
        
    st.subheader("Objectifs")
    
    st.markdown(
        """
        A travers ce projet, nous avons souhaité **identifier les éléments factuels disponibles et faire notre propre analyse**, sans
        connaissances préalable en climatologie. Notre objectif est de **mettre à disposition d'un public curieux et non-spécialiste**,
        à l'aide de données fiables et librement accessibles, **une analyse du réchauffement climatique**.
        
        Nous répondrons aux problématiques suivantes :
        1. **Les données disponibles permettent-elles de confirmer le phénomène de changement climatique ? Le réchauffement est-il
           réellement observable ? Dans le temps et dans l'espace, comment apparaît-il ?**
        2. **Quel degré de corrélation existe-t-il entre les émissions de $CO_2$ et l’évolution des températures ?**
        3. **Quelles sont nos prédictions de températures pour les prochaines décennies ?**
        """
        )
    
# Classification
        
    st.subheader("Classification du problème") 
    
    st.markdown(
        """
        Ces questions de recherche nous amèneront à utiliser la plupart des compétences acquises au cours de notre formation :

        1. Grâce aux outils de **Data Analyse** et de **Dataviz**, nous allons **acquérir, explorer, nettoyer, fusionner, visualiser et 
            analyser** nos données.
        2. Les **tests statistiques**, ainsi que les **régressions linéaire et polynomiale**, évaluées par des métriques de performance,
            nous permettront d'**établir** et d'**analyser ces degrés de corrélations**.
        3. Grâce au **machine learning**, nous construirons un **modèle prédictif d’évolution des températures**.
        
        Enfin, c’est par un **travail de recherche** que nous nous assurerons de **l’adéquation de nos résultats avec ceux des
        études courantes**. 
        """
        )

    st.markdown(
        """
        <br />
        
        ----
        
        Crédit image : Andreas Weith, [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0),
        via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Endangered_arctic_-_starving_polar_bear.jpg).
        """,
        unsafe_allow_html=True
        )
            
            
