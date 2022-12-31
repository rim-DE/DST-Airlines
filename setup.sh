
#creation des dossiers
mkdir -p airflow/logs airflow/plugins

#lancement airflow init
docker-compose up airflow-init

# lancement des différents services
docker-compose up

