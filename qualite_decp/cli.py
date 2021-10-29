import argparse

import audit
import download
import web


def command_download(args=None):
    """Télécharge la donnée consolidée (.json depuis data.gouv.fr)."""
    download.run()


def command_audit(args=None):
    """Audite la donnée consolidée et stocke les résultats."""
    audit.run(rows=args.row)


def command_web(args=None):
    """Lance l'application web de présentation des résultats"""
    web.app.run()


def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    download = subparser.add_parser(
        "download", help="télécharger la donnée consolidée (.json depuis data.gouv.fr)"
    )
    audit = subparser.add_parser(
        "audit", help="auditer la qualité de données et stocker les résultats"
    )
    audit.add_argument(
        "--rows",
        required=False,
        help="nombre de lignes desquelles auditer la qualité",
        type=int,
    )
    web = subparser.add_parser(
        "web", help="lancer l'application web de présentation des résultats"
    )
    return parser


def run(args=None):
    """Point d'entrée du CLI.

    Args:
        args : Liste d'arguments envoyée par la ligne de commande.
    """
    parser = get_parser()
    args = parser.parse_args(args)
    if args.command == "download":
        command_download(args)
    elif args.command == "audit":
        command_audit(args)
    elif args.command == "web":
        command_web(args)
