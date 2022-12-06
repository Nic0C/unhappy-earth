"""

Config file for Streamlit App

"""

from member import Member


TITLE = "UnhapPy Earth"

TEAM_MEMBERS = [
    Member(name = "Olga Fedorova", 
           linkedin_url = "https://www.linkedin.com/in/olga-fedorova-665a4b63/", 
           github_url = "https://github.com/OlgaFedorovaKukk"),
    Member(name = "Boris Baldassari", 
           linkedin_url = "https://www.linkedin.com/in/borisbaldassari/", 
           github_url = "https://github.com/borisbaldassari"),
    Member(name = "Nicolas Cristiano", 
           linkedin_url="https://www.linkedin.com/in/nicolas-cristiano-7b8a23171/", 
           github_url="https://github.com/Nic0C")]

PROMOTION = "Promotion Continue Data Analyst - Mars 2022"
