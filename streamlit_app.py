"""Ce fichier sert au déploiement sur streamlit.io. Il permet de lancer
l'application Web depuis la racine du projet avec le CLI Streamlit (streamlit run)
"""

from decp_qualite import web

web.app.run()
