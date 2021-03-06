### Catégories d'indicateurs

Les indicateurs calculés s'inscrivent dans 6 catégories :

* **Singularité** : Les données recueillies sont-elles redondantes? 
* **Validité** : Les données recueillies sont-elles suffisamment à jour? 
* **Complétude** : Toutes les données nécessaires à la prise de décision sont-elles disponibles? 
* **Conformité** : Quelles sont les données saisies, stockées ou affichées dans un format non standard?
* **Exactitude** : Les données recueillies sont-elles conformes à la réalité?
* **Cohérence** : Les données recueillies présentent-elles des contradictions? 


### Indicateurs

Le score de qualité de chaque catégorie est calculé à partir de un ou plusieurs indicateurs :

| Indicateur                                                          |  Catégorie  |         Unité         | Méthode de calcul                                                                                                                                                         |
|---------------------------------------------------------------------|:-----------:|:---------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Identifiants non uniques**                                            | Singularité | % de lignes en défaut | Une ligne est considérée en défaut si l'identifiant du marché (uid) n'est pas unique.                                                                                     |
| **Lignes dupliquées**                                                   | Singularité | % de lignes en défaut | Une ligne est considérée en défaut si une autre ligne possède les mêmes valeurs sur un sous-ensemble de données (sous-ensemble documenté dans la [configuration](https://github.com/139bercy/decp-qualite/blob/main/decp_qualite/conf.yaml)).                                                          |
| **Jours depuis la dernière publication**                                |   Validité  |         jours         | Cet indicateur est égal au nombre de jours entre la dernière publication et aujourd'hui. Il est limité à 100 jours.                                                       |
| **Dépassement du délai entre notification et publicatio**n              |   Validité  | % de lignes en défaut | Une ligne est considérée en défaut si l'écart entre notification et publication est supérieur au délai réglementaire. Ce délai est [défini à 2 mois](https://www.economie.gouv.fr/files/files/directions_services/daj/marches_publics/ouverture-donnees/Fiche_Open_data.pdf).                                                     |
| **Données manquantes**                                                  |  Complétude | % de lignes en défaut | Une ligne est considérée en défaut si au moins une donnée est manquante.                                                                                                  |
| **Caractères mal encodés**                                             |  Conformité | % de lignes en défaut | Une ligne est considérée en défaut si au moins une donnée parmi un sous-ensemble possède des caractères non encodés avec utf-8 (sous-ensemble documenté dans la [configuration](https://github.com/139bercy/decp-qualite/blob/main/decp_qualite/conf.yaml))                                           |
| **Formats ou types non respectés**                                      |  Conformité | % de lignes en défaut | Une ligne est considérée en défaut si au moins une donnée n'a pas le format attendu. Les formats attendus sont définis [ici](https://schema.data.gouv.fr/schemas/139bercy/format-commande-publique/latest/marches.json).                                                                                      |
| **Valeurs invalides**                                                   |  Conformité | % de lignes en défaut | Une ligne est considérée en défaut si au moins une donnée a une valeur qui ne fait pas partie des valeurs autorisées. Les valeurs autorisées sont définies [ici](https://schema.data.gouv.fr/schemas/139bercy/format-commande-publique/latest/marches.json).                                                     |
| **Valeurs/montants aberrants**                                          |  Exactitude | % de lignes en défaut | Une ligne est considérée en défaut si le montant ou la valeur est hors d'une zone définie (zone documentée dans la [configuration](https://github.com/139bercy/decp-qualite/blob/main/decp_qualite/conf.yaml) : 200€ - 999 999 999€)                                                                                |
| **Valeurs extrêmes**                                                    |  Exactitude | % de lignes en défaut | Une ligne est considére en défaut si au moins une donnée parmi un sous-ensemble a une valeur trop éloignée de la moyenne (éloignement défini en nombre de déviation standard dans la [configuration](https://github.com/139bercy/decp-qualite/blob/main/decp_qualite/conf.yaml)).                                                 |
| **Incohérence temporelles entre notification/signature et publication** |  Cohérence  | % de lignes en défaut | Une ligne est considérée en défaut si la date de publication est antérieure à la date de notification ou signature.                                                       |
| **Incohérences entre montant et durée**                                 |  Cohérence  | % de lignes en défaut | Une ligne est considérée en défaut si le montant apparaît comme peu probable par rapport à la durée : <br/> - montant / durée < 100 <br/> - montant / durée < 1000 et montant < 200000 <br/> - durée=360, 365, ou 366 et montant < 10000000 <br/> - durée > 120 et montant < 2000000 |