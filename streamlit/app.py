from collections import OrderedDict

import streamlit as st

# TODO : change TITLE, TEAM_MEMBERS and PROMOTION values in config.py.
import config

# TODO : you can (and should) rename and add tabs in the ./tabs folder, and import them here.
from tabs import intro, donnees, existence, correlation, prediction, conclusion


st.set_page_config(
    page_title=config.TITLE,
    page_icon="https://datascientest.com/wp-content/uploads/2020/03/cropped-favicon-datascientest-1-32x32.png",
)

with open("streamlit/style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)


# TODO: add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :
TABS = OrderedDict(
    [
        (intro.sidebar_name, intro),
        (donnees.sidebar_name, donnees),
        (existence.sidebar_name, existence),
        (correlation.sidebar_name, correlation),
        (prediction.sidebar_name, prediction),
        (conclusion.sidebar_name, conclusion),
    ]
)


def run():
    
    st.sidebar.image(
        "streamlit/assets/Unhappy_earth.png",
        width=250,
        )
    
    tab_name = st.sidebar.radio("", list(TABS.keys()), 0)
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"## {config.PROMOTION}")

    st.sidebar.markdown("### Team members:")
    for member in config.TEAM_MEMBERS:
        st.sidebar.markdown(member.sidebar_markdown(), unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        ----
        
        Crédit image :
        earth PNG Designed By IMZOMBIEASU from [Pngtree.com](https://pngtree.com/freepng/waste-water-and-exhaust-gas-and-unhappy-earth-clipart_6072655.html)
        """,
        unsafe_allow_html=True
        )
    
    tab = TABS[tab_name]

    tab.run()


if __name__ == "__main__":
    run()
