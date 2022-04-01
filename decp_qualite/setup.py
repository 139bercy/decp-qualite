from distutils.core import setup

setup(
    name="decp_qualite",
    version="0.1",
    description="Evaluation de la qualité des Données Essentielles de la Commande Publique (DECP).",
    py_modules=[
        "audit",
        "download",
        "web",
    ],
)
