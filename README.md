# JO-Parser
Fatigué des publications importantes noyées au milieu des arrêtés fixant les quotas de pêche pour la sole en mer baltique ? Voilà un script qui récupère le Journal Officiel du jour, en extrait les éléments "importants" correspondants à des mots-clés prédéfinis, et envoie un rapport via telegram.

# Installation

## Pré-requis

Ce script est conçu pour Python 3+.

Il est nécessaire d'avoir installé et configuré le module telegram-send (https://pypi.python.org/pypi/telegram-send#installation).

## Mise en place

1. Modifiez la liste "keywords =" pour y inclure les mots-clés ou phrases qui vous intéressent, en respectant le format suivant : keywords = ['mot-clé A', 'mot-clé 2', "mot-clé 3'].

2. Vérifiez la bonne exécution du script.

3. Planifiez ensuite l'exécution quotidienne du script avec le planificateur de tâches Windows ou une tâche Cron sous Linux.

# Carnet de développement

L'idée de départ était d'effectuer automatiquement un tri dans les entrées du Journal Officiel, pour n'en retirer que les éléments considérés comme intéressants (dans mon cas, les créations de traitements de données à caractère personnel, les arrêtés relatifs à la mise à disposition de données, etc...). Idéalement, le programme devait diffuser le condensé d'éléments retenus sous la forme d'un rapport envoyé par mail quotidiennement.

La première difficulté a été de trouver comment obtenir de manière fiable le JO chaque jour. Légifrance ne met pas de fil RSS à disposition, et n'offre pas de lien apparent renvoyant vers le dernier JO. La seule possibilité en matière de veille semblait donc de s'inscrire à la newsletter quotidienne. Mais se servir du mail envoyé par Légifrance comme base pour le parsing est bien plus complexe, d'autant plus que le mail envoyé n'est pas entièrement conforme au standard MIME (rendant l'utilisation du module mail-parser de python pénible).

Il se trouve que légifrance propose toutefois d'accéder aux trois derniers JO (https://www.legifrance.gouv.fr/initRechJO.do), par des liens avec suffixe .do, ce qui indique que légifrance s'appuie sur Struts et des servlets java. Et donc il suffit de prendre l'URL suivante : https://www.legifrance.gouv.fr/affichJO.do?idJO=. Celle-ci est en principe suivie de l'ID d'un JO spécifique mais cela n'est pas nécessaire et laisser "idJO" sans paramètre renvoie directement au dernier JO publié. L'adresse peut donc être hardcodée dans le script, en principe elle ne devrait pas bouger sauf refonte de légifrance.

L'étape suivante a été de trouver comment récupérer la source de la page, la traiter pour ne garder en mémoire qu'un arbre HTML propre, et récupérer tous les intitulés des publications. Une combinaison des modules requets, lxml et re fait cela très bien (cf. la section récpuration et parsing du code).

Plutôt que d'envoyer un mail, l'utilisation du module telegram-send permet de connecter le script à un bot telegram, lequel se charge d'envoyer le rapport final quotidiennement sur un groupe ou une chaîne telegram (ce qui permet à plusieurs personnes de profiter du rapport sans avoir à faire tourner le script chez eux).

Après quelques essais, les fonctionnalités de base sont opérationnelles et le parsing suffisament robuste, mais la qualité du rapport dépend fortement des mots-clés choisis. Le mot "traitement" seul renvoie beaucoup de faux positifs ("Arrêté du 1er mars 2018 autorisant l'ouverture au titre de l'année 2018 d'un examen professionnalisé réservé pour le recrutement de secrétaires administratifs affectés au **traitement** de l'information en qualité de programmeur relevant du ministère de la justice"), il faut donc affiner les expressions ("création d'un traitement").

# Fonctionnalités à ajouter

* Faire en sorte que les titres des publications intéressantes soient envoyées avec l'URL correspondante (tuple? set?).
* Rajouter un prompt afin qu'au premier lancement, le script demande quels mots-clés doivent être utilisés, plutôt que de hardcoder ces derniers.
* Ajouter un module d'envoi de mail comme alternative à Telegram.
* Figer le code et transformer le script en exécutable avec PyInstaller.
