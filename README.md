## **decp-qualite** : Evaluation de la qualité des Données Essentielles de la Commande Publique (DECP).

![Actions badge](https://github.com/139bercy/decp-qualite/actions/workflows/ci.yaml/badge.svg)
![Actions badge](https://github.com/139bercy/decp-qualite/actions/workflows/cd.yaml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Ce projet permet d'auditer la qualité des données essentielles de la commande publique consolidées sur data.gouv.fr. Les résultats sont affichés dans une application Web interactive.

Pré-requis :
* [pipenv](https://pipenv-fork.readthedocs.io/en/latest/)
* [python 3.8](https://www.python.org/downloads/release/python-3810/)

### Utilisateur

Installer les dépendances  :
```shell
pipenv install --python 3.8
```

Utiliser l'interface en ligne de commande  :
```
pipenv run python . [-h] {download,audit,web} ...

positional arguments:
  {download,audit,web}
    download            télécharger la donnée consolidée (.json depuis data.gouv.fr)
    audit               auditer la qualité de données et stocker les résultats
    web                 lancer l'application web de présentation des résultats

optional arguments:
  -h, --help            show this help message and exit
```

### Développeur

Installer les dépendances, y compris celles de développement  :
```shell
pipenv install --dev --python 3.8
```

(Optionnel) Installer le crochet de pre-commit et mettre à jour les versions :
```shell
pre-commit install
pre-commit autoupdate
```

### Fonctionnement

| GitHub Actions workflow | GitHub Actions artifacts store | Streamlit servers |
|:---:|:---:|:---:|
| Télécharge la donnée <br> Audite la qualité <br> → | <br><br>Stocke les résultats | <br><br><br>← <br>Exécute l'application Web | 