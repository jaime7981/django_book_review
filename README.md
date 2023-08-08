# Django Book Review

## Run Project
You can run the proyect installing the necesary dependencies or you can run a dockerized version of it bu just running 


### Dockerized version

You should set up an .env file defining database variables like db name or user, etc.

Example:

```
SECRET_KEY = "django-insecure-6@npg*5m+3q(*k!^hqxy6ep4@eh4iagi(*ikj$2*0e_=_c*9f+"
DB_PASSWD = "Soft@Arch123"
DB_USER = "softarch"
DB_NAME = "softarch_db"
```

Run containers:

`docker-compose up --build`

You could encounter an error when running the container where the database is not ready when django is trying to start. Just start again the django container whenever the database is ready to accept conections.

To populate the database you can enter the django container and run
`python seed_data.py`


## Report

In this project we used django as backend and postgres as a database.
The process of developing were easy beacause we were familiarized with the framework, also we had a dockerized template of the stack.

The easiest part gere generating the models for the application, beacause the entities and fields were well defined in the assignment.

The most difficult part were learing a scaffold module to generate the CRUD pages.
