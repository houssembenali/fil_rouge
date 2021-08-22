# Barre de navigation

En tant qu'administrateur il peut naviguer dans les différentes pages de l'interface graphique ou aussi en entrant directement les bonnes URLs.

Le menu est composé de trois partie, le logo de l’application, le différentes rebriques et le bouton de déconnexion.

Comme page l’utilisateur a la possibilité de basculer entre les trois rebrique disponible :

* Liste des projets : permet d’afficher la liste des projets ajouter et de les gérer.

* Ajout de projet : permet l’ajout d’un nouveau projet par l’administrateur

* Paramétrage : permet le paramétrage de notre application

L’administrateur peux aussi naviguer directement avec le lien hyper texte suivant : 

* Liste des projets :      http://WWW.XXX.YYY.ZZZZ:PPPP/projects ou [http://WWW.XXX.YYY.ZZZZ:PPPP/](http://WWW.XXX.YYY.ZZZZ:PPPP/projects)

* Ajout de projet :        http://WWW.XXX.YYY.ZZZZ:PPPP/addproject

* Paramétrage de l’app : http://WWW.XXX.YYY.ZZZZ:PPPP/param

Le logo est cliquable, ce dernier nous redirige vers la page d’accueil « Liste des projets » 

 

![img](img/navbar.png)

Figure 1 Barre de navigation de l'application

 

# Page d’ajout d’un projet

La Page d’ajout d’un projet, nous comme son nom l’indique à ajouter des projets selon deux propriétés qui sont « Nom du projet » et « URL du dépôt Git »

Le nom du projet doit être composée uniquement de chiffre, de lettre, d’espace, Under score et des tirés. Ce dernier doit aussi avoir une longueur maximale de 30 caractères avec un caractère minimal. Un test de redondance est disponible aussi sur ce champ.

Le champ « URL du projet Git » et soumis à plusieurs contrôles :

* Contrôle de format des liens des dépôt Git

* Teste de redondance

* Test d’existence du dépôt git (si ce dernier est inaccessible il sera rejeté)

Pour les dépôts privé la clé secrète API générer du projet sera intégrer directement dans le lien GIT comme l’exemple ci-dessous.

https://api_private_key:x-oauth-basic@github.com/user/repo.git

Lors de l’enregistrement avec sucée d’un projet un message informatif sera afficher pour notifier l’administrateur tout en redirigeant ce dernier vers la page de liste des projets.

Top of Form

 

 

![img](img/add.png)

Figure 2 Page d'ajout d'un projet

 

# Page liste des projets

La page de liste des projets (choisi comme page d’accueil) nous permet de gérer tous les projets déjà enregistrer en affichant le nom et le lien git de chacun avec un lien cliquable vers le dépôt git.

Cette page permet nous permet de supprimer ou publier un projet.

![img](img/list.png)

Figure 3 Page d'accueil (liste des projets)

## Suppression des projets
La suppression des projet ce fait directement a partir de la page de liste, chaque projet ayant sa propre bouton de suppression. 
Pour respecter les règles de l'expression utilisateur (UX/UI) nous avons personnaliser le bouton de suppression en couleur rouge et une icone corbeille.

![img](img/delete.png)

Figure 4 Page d'accueil (bouton suppression de projet)

On cliquant sur le bouton suppression et petite fenêtres pop-up va s'afficher pour demander a l'utilisateur de confirmer son choix de suppression on affichant le nom du projet séléctionner.
L'utilisateur peux cliquer sur le bouton de confirmation de suppression en rouge, dans ce cas le projet va êtres définitivement supprimer.
Sinon, l'utilisateur peux annuler cette demande on cliquant sur le bouton annuler en gris.

![img](img/confirm-del.PNG)

Figure 5 Fenêtre de pop-up de confirmation de suppression

Pour finir si l'étape de suppression est effectuer avec sucée, une alerte afficher en vert va attester le bon déroulement de la demande de suppression on redirigeant l'utilisateur vers la page accueil (liste des projets).
Le cas contraire, une alerte en rouge va notifier l'utilisateur qu'une erreur a intercepter la suppression on redirigeant ce dernier vers la page accueil (liste des projets).

![img](img/del-ok.PNG)
Figure 6 Alerte de suppression avec sucée

![img](img/notok-del.PNG)
Figure 7 Alerte de suppression avec erreur

## Publication des projets
Notre application permet aussi d'héberger des site web statique dans le cloud on lui donnant uniquement le repository git.
Dans cette étape, l'application va scanner tous les repository sélectionner et extraire tous fichier mark down existant, ensuite l'application va convertir ces dernier en fichier Web HTML.
En fin, il vont êtres héberger automatiquement dans le cloud tous on respectant les nom des fichier et tous l'arborescence des dossiers et sous-dossier du repository git.

La publication se fait a travers la page accueil (liste des projet), on cliquant uniquement sur le bouton vert "publier" avec l'icone indiquant l'étape de publication.

![img](img/publish.png)
Figure 7 Bouton de publication de projet

On cliquant sur le bouton de publication, l'application va afficher une fenêtres pop-up pour confirmer la publication de ce dernier.
L'utilisateur a la possibilité d'ajouter une table de matière au début de  chaque fichier générer, on cliquant ou non sur la case a coché afficher dans la fenêtre.
En fin, l'utilisateur peux confirmer sa publication du projet on cliquant sur le bouton vert "publier" pour commencer l'étape de publication ou annuler se dernier via le bouton "annuler" en gris 

![img](img/confirm-publish.PNG)
Figure 7 Bouton de publication de projet

Après quelques seconde de la confirmation, pendant que l'application scanne, converti et héberge les fichier du repository, l'application va afficher, si c'est ok, une alerte en vert tout on redirigeant l'utilisateur vers la page liste des projets, on indiquant que la publication est effectuer avec sucée.

![img](img/publish-ok.PNG)
Figure 7 Alerte de publication avec sucée

Si le cas échéant, une alerte en rouge va êtres afficher pour indiquer qu'il y a eu une erreur lors de la publication.

![img](img/notok-publish.PNG)
Figure 7 Alerte de publication avec erreur


# Page Paramétrage Cloud

La page paramétrage cloud permet de définir le nom du bucket via l'IHM en respectant les critères définis par aws à savoir :

* Les noms de buckets doivent comporter entre 3 et 63 caractères.

* Les noms de compartiment ne peuvent être constitués que de lettres minuscules, de chiffres, de points (.) et de tirets (-).

* Les noms de buckets doivent commencer et se terminer par une lettre ou un chiffre.

![img](img/param-bucket.PNG)

 
