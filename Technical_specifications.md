# Spécifications techniques de l'application GitHub Holder

## Préambule

Ce document de spécifications comporte l'ensemble des informations techniques sur la paramétrisation du serveur Nexus, du Jenkins, des processus d'intégration continue, de livraison continue, de déploiement continu, la paramétrisation des différentes composantes du compte Amazon Web Service (AWS) sur lequel l'application est hébergée, ainsi que les pages html des sites créés pour les clients, et enfin sur le fonctionnement technique de la récupération, du sotckage et de la conversion des fichiers markdown des clients en fichiers html.

## Serveur Nexus

Un serveur Nexus hébergé sur AWS est mis en place pour stocker l'ensemble des livraisons effectuées dans le cadre du développement de l'application.

Il est atteignable à l'adresse https://192.168.20.12:8081 à toute heure de la journée.

### Description du contenu du serveur

Un repository a été configuré pour contenir les livrables de l'application, nommé "projet-fil-rouge". Ce repository contient des sous-repositories, nommés XX.YY.ZZ (ou XX = major version, YY = minor version, ZZ = build version, de l'application), à raison d'un par version de l'application. Ces repositories contiennent eux-mêmes des archives zip stockant les livrables de l'application, nommés projet-XX.YY.ZZ.zip (où XX = major version, YY = minor version, ZZ = build version, de l'application).

Les archives contiennent:
- un dossier /app/ contenant l'ensemble des sources de l'application à date de la livraison de la version correspondante. 
- un dossier /doc/ contenant l'ensemble de la documentation fonctionnelle et technique de l'application à date de la livraion de la version correspondante (inclu le présent document).
- un dossier /tests/ contenant l'ensemble des rapports de tests joués sur la version de l'application livrée.
- un procès verbal de livraison (PV de livraison).
- un bordereau de livraison (BL).

### Accès au repository "projet-fil-rouge"

L'accès à cette partie du serveur Nexus est autorisée aux personnes suivantes:
- développeurs de l'application, en poste sur le projet à date.
- Project Owner de l'application, en poste à date.
- Scrum Master de l'équipe de developpement, en poste à date.
- Personnels du client propriétaire de l'application, autorisés par le client à date.


## Serveur Jenkins

Un serveur Jenkins hébergé sur AWS est mis en place pour piloter les différentes étapes de CI/CD sur le projet.

Il est atteignable à l'adresse https://192.168.20.10:8080 à toute heure de la journée.

### Configuration de Jenkins

Trois jobs différents sont configurés sur le Jenkins: 

- le premier se charge de faire tourner les tests de qualité de code et les tests unitaires à chaque push sur la branche "dev", de sorte à pouvoir tracer au plus tôt des problèmes bas niveau et mineurs.
- le second se charge de faire tourner l'ensemble des tests à chaque push sur une branche commençant par le préfixe "release-", qui permet de réaliser des tests extensifs sur les release candidates. Dans le cas où tous les tests passent le job se charge de merger la branche release dans les branches "main" et "dev". Il effectue également un tag sur GitHub.
- le troisième se charge à chaque push sur main de constituer une archive zip qui est envoyée sur le serveur Nexus, de construire une image Docker de l'application et de la pousser sur DockerHub, de déployer à l'aide de Kubernetes l'image Docker de l'application en production sur AWS.

Les trois jobs sont configurés en pipeline. Les scripts de pipeline sont stockés et travaillés sur des Jenkinsfile présent dans le dépot GitHub de l'application.

### Outils

#### Gradle

La version 7.0 de Gradle est installée. Elle est installée d'un part à l'installation de la VM Linux qui sert de support au serveur Jenkins, et d'autre part elle est configurée dans la section "Configuration globale des outils" sur l'interface Jenkins.

### Accès au serveur Jenkins

L'accès à cette partie du serveur Nexus est autorisée aux personnes suivantes:
- développeurs de l'application, en poste sur le projet à date.
- Project Owner de l'application, en poste à date.
- Scrum Master de l'équipe de developpement, en poste à date.