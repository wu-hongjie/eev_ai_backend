# eev_ai_backend
EEV AI backend system

# OS
Ubuntu 20.04.5 LTS

# Ptyhon environment
Python 3.8  

# Create python virtual environment
`python3 -m venv venv`  
`source venv/bin/activate`


# Install Python packages
`pip install -r requirements.txt`

# Using docker ( require: install docker and docker compose)
```
    $ docker-compose build
    $ docker-compose up -d
    $ docker exec -it eev_db bash
    $ mysql -uroot -p
    $ create user 'eev'@'*' identified by 'password'
    $ grant all on eev.* to 'eev'@'*'

```
Add to .env: 
```
    DB_ENGINE='django.db.backends.mysql'
    DB_NAME='eev'
    DB_USER='eev'
    DB_PASSWORD='password'
    DB_HOST='eev_db'
    DB_PORT='3306'
```
Run migration:
```
    $ docker exec -it eev_app bash
    $ python manage.py migrate
```

Localization:
```
$ cd [eev_ai_backend]/backend
$ django-admin makemessages -l ja
$ django-admin compilemessages 
```
