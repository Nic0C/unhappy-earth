import streamlit as st


title = "UnhapPy Earth"
sidebar_name = "Introduction"


def run():

    st.image("streamlit/en/assets/starving_polar_bear.jpg")

    st.title(title)

    st.markdown("---")
    
    st.header("Global Warming Analysis")
    
# Contexte :

    st.subheader("Context / Definition")
    
    st.markdown(
        """
        In just a few decades, **the question of global warming has become a major subject**, worrying
        for the future of the planet and its biodiversity, including the human species. **Yet it is still debated**, opposes
        experts and climate sceptics, **at the very time when its manifestations and consequences** (droughts and torrential rains,
        repeatedly, rising water levels) **are more flagrant every day**. Here is a simple definition, proposed by the
        media platform [Youmatter](https://youmatter.world/fr/):
           
        **Global warming is a global phenomenon of climate transformation characterized by an increase
        general average temperatures (in particular linked to human activities, releasing quantities of greenhouse gases), and which
        permanently alters meteorological balances and ecosystems.**
       
        In addition, a [United Nations report published in April 2022](https://www.nationalgeographic.fr/environnement/2017/09/le-veritable-cout-du-changement-climatique)
        asserts: **global warming is incredibly costly**: humanly, socially, geopolitically,
        financially and economically.
       
        **Anticipating and better understanding its consequences is therefore becoming a priority** for many companies and organizations.
        """
        )

# Objectifs :
        
    st.subheader("Goals")
    
    st.markdown(
        """
        Through this project, we wanted to **identify the factual elements available and make our own analysis**, without
         prior knowledge of climatology. Our objective is to **make available to a curious and non-specialist public**,
         using reliable and freely accessible data, **an analysis of global warming**.
        
         We will answer the following questions:
         1. **Do the available data confirm the phenomenon of climate change? Is warming
            actually observable? In time and space, how does it appear?**
         2. **What degree of correlation is there between the emissions of $CO_2$ and the evolution of temperatures?**
         3. **What are our temperature predictions for the next few decades?**
        """
        )
    
# Classification
        
    st.subheader("Problem classification") 
    
    st.markdown(
        """
        These research questions will lead us to use most of the skills acquired during our training:

         1. Thanks to the tools of **Data Analysis** and **Dataviz**, we will **acquire, explore, clean, merge, visualize and
             analyze** our data.
         2. **Statistical tests**, as well as **linear and polynomial regressions**, evaluated by performance metrics,
             will allow us to **establish** and **analyze these degrees of correlation**.
         3. Thanks to **machine learning**, we will build a **predictive model of temperature evolution**.
        
         Finally, it is through **research work** that we will ensure **the adequacy of our results with those of the
         current studies**.
        """
        )

    st.markdown(
        """
        <br />
        
        ----
        
        Image credit: Andreas Weith, [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0),
        via [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:Endangered_arctic_-_starving_polar_bear.jpg).
        """,
        unsafe_allow_html=True
        )
            
            
