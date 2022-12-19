***Revue sur le contenu*** 

La branche contient 7 répertoires dont un contenant la documentation des étapes du projet et les autres contenantt :

- Un ou plusieurs scripts Python permettant la configuration et/ou le chargement du container portant le nom de ce répertoire.
- Un fichier "requirements.txt" contenant les dépendances nécessaires pour la bonne exécution de ces scripts.
- Un Dockerfile créant une image Python qui exécute les scripts de configuration et/ou de chargement des containers.
- Dans certains cas, des fichiers complémentaires facilitant le paramètrage et/ou l'exploitation des containers construits.


***Les répertoires sont:*** 

a. doc: fichier de documentation concernant l'architecture de stockage adoptée

b. Elasticsearch: pour créer 3 indexes ElasticSearch et les remplir 

* Créer 3 indexes : flights, airports, companies
* Charger journalièrement les données relatives aux vols enregistrés la veille dans l'indexe flights
* Charger un dashboard préconçu permettant d'analyser les données des 3 indexes dans Kibana

b-bis: Kibana: pour analyser les données contenues dans les indexes d'Elasticsearch

c. MongoDB: pour créer et charger la base de données MongoDB à partir de scrapping api OpenSky

d. mysql :

* Créer et charger la base de données Mysql. Ce dossier contient les scripts du scrapping HTML des données des aéroports.
* Les données sont extrtaites de ce site: https://www.world-airport-codes.com

e. Dash : 

* Pour lancer Dash : http://localhost:8050/

![dash](https://user-images.githubusercontent.com/47364591/208427261-6d9d9a29-2586-4be7-b9a5-bac606417935.png)


f. Logstash

* Créer un pipeline pour charger mensuellement la table aéroports contenue dans la base de données du container MySQL vers l'indexe airports
* Créer un pipeline pour charger mensuellement la table compagnies contenue dans la base de données du container MySQL vers l'indexe companies

g. Airflow: Pour automatiser l'extraction des données et le chargement dans les bases: mysql, elastic-search et mongo-db. Il s'agit d'automatiser la partie ETL (Extract Transform Load) et de définir un DAG (Directed Acyclic Graph) pour chaque base.

- Pour lancer Airflow: http://localhost:8080/ (user: airflow, password: airflow).

- Les Dags dans Airflow:

1.  Le dag mysql séxécute une fois par mois: 


![image](https://user-images.githubusercontent.com/85707067/206479594-9f6d25fc-f4ba-4337-849c-ec127c77ebbd.png)

2.  Le dag ElasticSearch s'éxécute tous les jours à 8h du matin:


![image](https://user-images.githubusercontent.com/85707067/206481204-9cc19408-9ce3-49e9-bea3-ebb7585c2585.png)


3.  Le dag MongoDB, s'éxécute toute les 45 seconces:


![image](https://user-images.githubusercontent.com/85707067/206481297-4d865462-3f11-4657-968c-45ef3fa3e4cc.png)


***Docker-compose.yaml:***

Le Docker-compose.yaml gère et regroupe toute les images des services. Les images sont:

1. mongo: image de la base de données mongoDB
2. mongo_load: image python qui charge mongoDB
3. mongoexpress: image. RQ: Les services mongo_load et mongoexpress dépendent du service mongo.
4. elasticsearch: image de la base de données Elasticsearch
5. es_load: image python qui permet de charger Elasticsearch.
6. kibana: image de l'interface utilisateur qui nous permet de visualiser les données Elasticsearch
7. RQ: Le lancement des services es_load et kibana dépendent du service Elasticsearch.
8. mysql : image de la base de données mysql. dans le volume, on a définit le schema.sql pour créer la base et les deux tables. 
9. python-mysql: image python qui permet de scrapper les données et les charger dans mysql. 
10. logstash: image Logstash qui copie les données de MySQL à Elasticsearch
11. Dash:
  
  Le volume dans docker-compose est dynamique et géré entièrement par docker. C'est pour quoi on a définit le service  "volumes".

***Commandes utiles:***

- Pour lancer docker-compose.yml:

```bash
# lancement airflow init
docker-compose up airflow-init

# lancement des différents services
docker-compose up
```
- pour sélectionner le service à lancer à partir de docker compose:

```bash
# Nom du service ??
sudo docker compose up <nom_service>
```
                 
***Pour lancer les images:***

- Exécuter la commande: $ sudo docker compose up 
- Pour lancer mongoDB: http://127.0.0.1:8081/ 
- Pour lance Elasticsearch http://localhost:5601/ --> devtools --> Exécuter les requetes "POST flights/_count" , "GET /flights/_search"
- Pour inspecter les données mysql: installer un client en local (dbeaver par expl) et tester. 






