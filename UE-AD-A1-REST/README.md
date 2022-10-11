# Les instructions de lancements se situe dans la racine du dépot
Ce readme abordera uniquement notre réponse à l'énoncé du TP

## TP vert : 
Nous avons réalisé l'interface présenté sur le schéma.</br>
Nous avons intégré dans User 2 routes appelant Booking & Movie :</br>

bookinglist : retourne la liste des ID des films réservés par l'ID d'utilisateur envoyé en paramètre.</br>
    => Appel à booking</br>
</br>
get_user_movies : retourne la liste détaillé des films réservés par l'ID d'utilisateur envoyé en paramètre.</br>
    => Appel à booking & showtime</br>

## TP bleu : 
Nous avons mis à jours tous nos services afin qu'ils renvoient la liste des API qui leur sont accessibles et qu'ils retournent leur spécification.</br>
De cette manière nous avons éssayé de nous rappocher au maximum d'un service RestFULL.

## TP rouge : 

Le micro-service Movie a été relié à l'API imdb-api.</br>
Cela nous permet de faire fonctionner notre API avec les 250 premiers films du moment.

### Auteurs : Pierre-Alexandre MARTIN - Mathias NOCET
### Date : 11 oct. 2022