import yaml
import munch

with open('qualite_decp/conf.yaml', encoding="utf-8") as f:
    conf_dict = yaml.safe_load(f)
conf = munch.DefaultMunch.fromDict(conf_dict)