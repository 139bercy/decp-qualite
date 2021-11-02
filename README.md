## **decp-qualite** : Evaluation de la qualité des Données Essentielles de la Commande Publique (DECP).


![Actions badge](https://github.com/139bercy/decp-qualite/actions/workflows/ci.yaml/badge.svg)
![Actions badge](https://github.com/139bercy/decp-qualite/actions/workflows/cd.yaml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Prérequis :
* pipenv
* Python 3.8

Installer les dépendances  :
```shell
pipenv install
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