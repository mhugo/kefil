Kefil est un logiciel d'encaissement de commandes alimentaires.

Il s'agit d'une application web avec un frontal en HTML et Javascript. Une partie backend est écrite en Python (flask) avec une petite base de données SQLite.

## Modèle de données

Parmi les entités manipulées par le logiciel:
- les "commandes" qui ont:
  - un numéro
  - une liste d'"articles" avec une quantité associée à chacun
  - une date et heure de paiement
  - la somme payée dans chacun des modes de paiement (ce qui permet un panachage des modes de paiement pour une même commande)
  - la somme de l'éventuelle remise associée
- la liste des articles qu'il est possible de commander est configurable dans une table: le nom et le prix de chaque article est paramétrable

La base stocke également une liste de "bons de réduction" qui ont chacun:
- un identifiant unique sur 5 lettres et chiffres,
- une description
- un état booléen: utilisé ou non
- si utilisé, la commande dans laquelle il a été utilisé

## Interface utilisateur

L'interface utilisateur présente plusieurs écrans ou onglets.

### Écran principal

L'écran principal présente la liste des articles qu'il est possible de commander. Chaque article est représenté par un bouton carré de taille importante pour permettre une sélection aisée par le caissier. Chaque click sur un article ajoute un exemplaire de cet article à la commande en cours.

À chaque sélection d'un article, la liste des articles de la commande se met à jour ainsi que la somme totale dûe.

Sous la zone de sélection des articles, plusieurs boutons permettent de choisir le mode de paiement:
- espèces
- carte bancaire
- cashless (système de badge utilisé sur les festivals)

Un click sur "espèces" ouvre une nouvelle fenêtre modale qui permet de préciser la somme donnée par le client et de calculer automatiquement la somme à rendre. Une fois le paiement validé, le reste à payer est nul et la commande peut être validée.

Un click sur "carte bancaire" ou "cashless" valide directement le paiement en précisant le mode. La gestion du mode de paiement physique (terminal de paiement) est indépendante du logiciel et doit être faite par le caissier.

Une bouton supplémentaire "remise" permet de saisir une remise à la commande.

Une fois la commande validée, elle est enregistrée dans l'historique et l'écran présente une commande vierge pour le prochain client.

### Historique

L'écran "historique" reprend la partie "commande" de l'écran principal, mais en lecture seule.

La liste des commandes est présentée dans la partie basse et une sélection d'une commande fait apparaître le détail d'une commande passée.

Il est impossible de modifier une commande passée.

### Bilan

Un écran "bilan" permet de résumer les commandes de la journée:
- nombre de commandes
- nombre d'articles vendus
- somme totale vendue

