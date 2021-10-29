"""Ce fichier sert au déploiement sur streamlit.io. Il permet de lancer
l'application Web depuis la racine du projet avec le CLI Streamlit (streamlit run)
"""

from qualite_decp import web

web.app.run()
