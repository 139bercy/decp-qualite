## **decp-qualite** : Evaluation de la qualité des Données Essentielles de la Commande Publique (DECP).

![Actions badge](https://github.com/139bercy/decp-qualite/actions/workflows/tests.yaml/badge.svg)
![Actions badge](https://github.com/139bercy/decp-qualite/actions/workflows/run.yaml/badge.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Ce projet permet d'auditer la qualité des données essentielles de la commande publique consolidées sur [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/donnees-essentielles-de-la-commande-publique-fichiers-consolides/). Les résultats sont affichés dans une application Web interactive.

Pré-requis :
* [pipenv](https://pipenv-fork.readthedocs.io/en/latest/)
* [python 3.8](https://www.python.org/downloads/release/python-3810/)

### Utilisation

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

Pour la commande `web` les variables d'environnements `GITHUB_USERNAME` et `GITHUB_TOKEN` doivent être définies. Le jeton d'accès doit avoir au moins le scope `public_repo` (accès aux projets publics).

```shell
# macOS ou Linux
export GITHUB_USERNAME="<Nom d'utilisateur GitHub>"
export GITHUB_TOKEN="<Jeton d'accès>"
# Windows
SET GITHUB_USERNAME=<Nom d'utilisateur GitHub>
SET GITHUB_TOKEN=<Jeton d'accès>
# PowerShell
$Env:GITHUB_USERNAME="<Nom d'utilisateur GitHub>"
$Env:GITHUB_TOKEN="<Jeton d'accès>"
```

### Guide du développeur

#### Mise en place de l'environnement et *workflow*

Installer les dépendances, y compris celles de développement  :
```shell
pipenv install --dev --python 3.8
```

(Optionnel) Installer le crochet de pre-commit et mettre à jour les versions :
```shell
pre-commit install
pre-commit autoupdate
```

Un [*workflow*](.github/workflows/tests.yaml) se déclenche à chaque *push* sur la branche *main*. Il est composé de deux *jobs* :
* `pylint-score` vérifie la conformité du code au standard PEP-8, à l'aide du module *pylint*. Le *job* échoue si le score de conformité est inférieur à 8/10.
* `pipfile-lock-check` vérifie que les dépendances du projet sont correctement vérouillées dans le fichier *Pipfile.lock*. Il s'agit d'une pratique recommandée dans la documentation de l'outil *pipenv*. Le *job* échoue si ce n'est pas le cas.

#### Configurations, hypothèses et valeurs par défauts

Les hypothèses  et seuils utilisées pour l'audit de qualité, principaux textes de l'application Web, et URL des jeux de données utilisées sont répertoriés dans le fichier de configuration [`decp_qualite/conf.yaml`](decp_qualite/conf.yaml)

#### Ajouter une mesure de qualité

Pour créer un nouvel indicateur de qualité, les 4 étapes suivantes doivent être exécutées :

* La nouvelle mesure doit être définie comme une nouvelle classe héritant de la classe `Measure` dans le fichier [`decp_qualite/audit/measures.py`](decp_qualite/audit/measures.py).
* La nouvelle mesure doit ensuite être rattachée à la classe `AuditResultsOneSource` dans le fichier [`decp_qualite/audit/audit_results_one_source.py`](decp_qualite/audit/audit_results_one_source.py).
* Les valeurs de la mesure pour le jeu de données doivent être calculées dans la fonction `audit_source_quality` dans le fichier [`decp_qualite/audit/app.py`](decp_qualite/audit/app.py).
* Enfin, l'affichage de la mesure sur le tableau de bord doit être implémenté dans la fonction `details_container` dans le fichier [`decp_qualite/web/build.py`](decp_qualite/web/build.py).


### Fonctionnement opérationnel

Deux systèmes fonctionnent en parallèle. Ils utilisent tous les deux la branche *main* du projet.

* Un [*workflow*](.github/workflows/run.yaml) automatisé analyse chaque 1er du mois la qualité de données en exécutant les commandes `download` puis `audit`. Ce workflow s'exécute sur le service GitHub Actions. Trois *artifacts* au format JSON sont générés par ce *workflow* puis stockés par GitHub :
  * Le fichier original des DECP consolidées, issu de la commande `download`
  * Le fichier de synthèse des résultats de l'analyse de qualité par source, issu de la commande `audit`, au format JSON
  * Le fichier de détail par marché de l'analyse de qualité, issu de la commande `audit`

* L'application Web de présentation des résultats est hébergée sur le service streamlit.io. Elle peut aussi être exécutée ssur un poste avec la commande `web`. L'utilisateur sélectionne une date courante et une date de comparaison, et l'application récupère les résultats d'audit (stockés sous forme d'*artifacts*) correspondant à ces dates pour les afficher sur la page.
