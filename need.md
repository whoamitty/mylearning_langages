# Ce fichier explique ce d'ont j'ai besoin pour exploiter ma base de donnée

## `*_to*.csv`   
une commande qui envois dans la langue cible  
les nouvelles definitions trouvés d'un mot  
dans les fichier `*_to*.csv`  
du dossier mylearning_langages/ 

Voici ceux que j'ai pour l'instant:  
english/american-english_tofr.csv  
french/french_toen.csv


exemple de contenu:  
easygoing, insouciant, facile à vivre  
eat, manger, prendre, finir,  
eatable,  


ex: trans -enfr eat prendre manger finir  


## word_increment.csv
si un mot ajouté l'as déjà été une fois,  
on incrémente dans word_increment.csv son nombre de fois ajouté  
english/word_increment.csv  
french/word_increment.csv  

et en l'ajoutant si ce n'est que la première fois avec une initialisation à 1  
exemple de contenu pour word_increment.csv :  
easygoing, 1  
eat, 3  
eatable, 4


Et si il y es déjà, on ne l'ajoute bien-sûr pas dans:  
english/american-english_tofr.csv  
french/french_toen.csv


## topwords
les fichier topwords  
devrons contenire les mots les plus utilisés de la langue source  
par les natifs  
Je ne les ai pas encore récupérés  

## quotes
Les fichiers quotes  
devrons contenire les expréssions les plus utilisés de la langue  
par les natifs  
Je ne les ai pas encore récupérés  


Pour le moment, je n'utilise pas topwords et quotes  
ça sera dans un second temps  