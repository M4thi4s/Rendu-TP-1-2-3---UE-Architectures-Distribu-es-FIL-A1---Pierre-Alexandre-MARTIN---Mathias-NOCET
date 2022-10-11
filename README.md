# Rendus des TP Rest, GRPC et GraphQL

## Pour lancer les différents TP sans docker, il faut :
1. Ouvrir 4 terminal dans le dossier du TP</br>
2. Ouvrir les dossiers User, Movie, Client & Showtime</br>
3. Installer les dépendances à l'aide de la commande : pip3 install -r requirements.txt</br>
4. Lancer les 4 micros-service dans l'ordre suivant : Times, Movie, Booking & User</br>

## Et avec docker :
Docker permet de lancer et mettre à jour tous les serveurs en meme temps
1. Se placer dans le dossier du TP _(`cd ./UE-AD-A1-GRAPHQL`)_
2. Lancer un build du docker-compose _(`docker-compose build`)_
3. Deployer le docker-compose _(`docker-compose up -d`)_
4. Lancer le docker-compose _(`docker-compose start`)_

## Pour tester : 
- Le TP REST peut être testé en mettant les fichiers YAML dans Postman
- Le TP GRPC possède un dossier contenant les fichiers de tests intitulés Client
- L'interface graphQL du service Movie du TP 4 est accessible à l'url 127.0.0.1:3200/graphql

### Auteurs : Pierre-Alexandre MARTIN - Mathias NOCET
### Date : 11 oct. 2022