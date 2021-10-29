import yaml
import munch

# Charge les entrées du fichier de configuration et les 
# place dans un objet python nommé 'conf' utilisé dans le reste du projet
with open('qualite_decp/conf.yaml', encoding="utf-8") as f:
    conf_dict = yaml.safe_load(f)
conf = munch.DefaultMunch.fromDict(conf_dict)
