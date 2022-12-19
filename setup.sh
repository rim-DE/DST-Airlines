# exemple de fichier de setup
# creation des dossiers
mkdir airflow/logs airflow/plugins

# lancement airflow init
docker-compose up airflow-init

# lancement des différents services
docker-compose up