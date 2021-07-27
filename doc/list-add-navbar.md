# Barre de navigation

En tant qu'administrateur il peut naviguer dans les différentes pages de l'interface graphique ou aussi en entrant directement les bonnes URLs.

Le menu est composé de trois partie, le logo de l’application, le différentes rebriques et le bouton de déconnexion.

Comme page l’utilisateur a la possibilité de basculer entre les trois rebrique disponible :

·    Liste des projets : permet d’afficher la liste des projets ajouter et de les gérer.

·    Ajout de projet : permet l’ajout d’un nouveau projet par l’administrateur

·    Paramétrage : permet le paramétrage de notre application

L’administrateur peux aussi naviguer directement avec le lien hyper texte suivant : 

·    Liste des projets :      http://WWW.XXX.YYY.ZZZZ:PPPP/projects ou [http://WWW.XXX.YYY.ZZZZ:PPPP/](http://WWW.XXX.YYY.ZZZZ:PPPP/projects)

·    Ajout de projet :        http://WWW.XXX.YYY.ZZZZ:PPPP/addproject

·    Paramétrage de l’app : http://WWW.XXX.YYY.ZZZZ:PPPP/param

Le logo est cliquable, ce dernier nous redirige vers la page d’accueil « Liste des projets » 

 

![img](img/navbar.png)

Figure 1 Barre de navigation de l'application

 

# Page d’ajout d’un projet

La Page d’ajout d’un projet, nous comme son nom l’indique à ajouter des projets selon deux propriétés qui sont « Nom du projet » et « URL du dépôt Git »

Le nom du projet doit être composée uniquement de chiffre, de lettre, d’espace, Under score et des tirés. Ce dernier doit aussi avoir une longueur maximale de 30 caractères avec un caractère minimal. Un test de redondance est disponible aussi sur ce champ.

Le champ « URL du projet Git » et soumis à plusieurs contrôles :

·    Contrôle de format des liens des dépôt Git

·    Teste de redondance

·    Test d’existence du dépôt git (si ce dernier est inaccessible il sera rejeté)

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

 

 
