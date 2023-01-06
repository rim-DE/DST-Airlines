#installation du client docker: portainer
docker volume create portainer_data
docker run -d -p 8000:8000 -p 9000:9000 --name=portainer --restart=always -v /var/run/docker.sock:/var/run/docker.sock -v portainer_data:/data portainer/portainer-ce

#creation des dossiers
#mkdir -p airflow/logs airflow/plugins

#lancement airflow init
docker-compose up airflow-init

# lancement des différents services
docker-compose up

