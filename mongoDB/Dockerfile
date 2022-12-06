#Préciser l'image de base
FROM python:3

#spécifier où on va copier les sources à l'intérieur du container
WORKDIR /usr/src/app

#copier le contenu du requirements.txt
COPY requirements.txt ./

#installer le contenu du requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#copier le contenu du dossier courant (les autres scripts python)   dans le conatainer
COPY . .

#Définir la commande à exécuter (le point d'entrée) au lancement du container
CMD [ "python", "./init.py"]