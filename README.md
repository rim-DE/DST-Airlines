***Revue sur le contenu*** 

La branche contient 3 répertoires. Chaque répertoire contient :

- Les scripts python permettant la création et le chargement de la base.
- "requirements.txt": contenant les dépendances nécessaires pour exécuter  les scripts
- un docker file: pour créer une image python. Elle permet d'installer les requirements et builder les scripts 


***Les répertoires sont:*** 

a. doc: fichier de documentation concernant l'architecture de stockage adoptée

b. Elasticsearch: Pour créer et charger la base de données ElasticSearch à partir de scrapping api OpenSky

c. MongoDB: pour créer et charger la base de données MongoDB à partir de scrapping api OpenSky

d. Mysq_folder :

* Créer et charger la base de données Mysql. C dossier contient les scripts du scrapping HTML des données des aéroports.
* Les données sont extrtaites de ce site: https://www.world-airport-codes.com/alphabetical/airport-code/a.html?page=1
                 
e. Docker-compose.yml : gère et regroupe toute les images des services. Les images sont:

1. mongo: image de la base de données mongoDB
2. mongo_load: image python qui charge mongoDB
3. mongoexpress: image. RQ: Les services mongo_load et mongoexpress dépendent du service mongo.
4. elasticsearch: image de la base de données Elasticsearch
5. es_load: image python qui permet de charger Elasticsearch.
6. kibana: image de l'interface utilisateur qui nous permet de visualiser les données Elasticsearch
7. RQ: Le lancement des services es_load et kibana dépendent du service Elasticsearch.
8. mysql : image de la base de données mysql. dans le volume, on a définit le schema.sql pour créer la base et les deux tables. 
9. python-mysql: image python qui permet de scrapper les données et les charger dans mysql. 
  
  Le volume dans docker-compose est dynamique et géré entièrement par docker. C'est pour quoi on a définit le service  "volumes".


***Commandes utiles:***

- Pour lancer docker-compose.yml:
$ sudo docker compose up
- pour sélectionner le service à lancer à partir de docker compose:
$ sudo docker compose up <nom_service>
                 
***Pour lancer les images:***

- Exécuter la commande: $ sudo docker compose up 
- Pour lancer mongoDB: http://127.0.0.1:8081/ 
- Pour lance Elasticsearch http://localhost:5601/ --> devtools --> Exécuter les requetes "POST flights/_count" , "GET /flights/_search"
- Pour inspecter les données mysql: installer un client en local (dbeaver par expl) et tester. 



***Airflow pour l'ordonnancement des tâches:***

***Les Dags dans Airflow:***
- mysql: 


![image](https://user-images.githubusercontent.com/85707067/206479594-9f6d25fc-f4ba-4337-849c-ec127c77ebbd.png)

- ElasticSearch:


![image](https://user-images.githubusercontent.com/85707067/206480492-462ae158-32e0-4075-96b0-866ca8ee9606.png)

- MongoDB:


![image](https://user-images.githubusercontent.com/85707067/206480647-22ee2e0b-5482-4ba0-a379-54a57b2b3898.png)

