
## Installation 
```
pip install Flask-Migrate
pip install flask-login
pip install -U Flask-SQLAlchemy
pip install flask_bcrypt
pip install flask_wtf
pip install email_validator

```

## Création de la base de données

```
../webapp/src$ flask db init
../webapp/src$ flask db migrate -m "Users table."  
../webapp/src$ flask db upgrade 

```

## Run app 

```
../webapp/src$ export FLASK_APP=modules && export FLASK_DEBUG=1
../webapp/src$ export FLASK_DEBUG=1
../webapp/src$ flask run
```