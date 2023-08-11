# Django Book Review

## Run Project
You can run the project by installing the necesary dependencies and running it in your local machine or you can run a dockerized version of it by following the instructions below.

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
```bash
docker-compose up --build
```

### M1 Mac
If it doesn't work on M1 Mac, try to run the following command:
```bash
DOCKER_DEFAULT_PLATFORM=linux/amd64 docker-compose build
```

You could encounter an error when running the container where the database is not ready when django is trying to start. Just start again the django container whenever the database is ready to accept conections.

To populate the database you can run this script into the django_book_review containers terminal

```bash
python seed_data.py
```
## Report

In this project we used django as backend, which uses python and postgres as a database.

The process of developing were easy beacause we were very familiarized with the framework, also we had a dockerized template of the stack, so installing dependencies and running the app for development was an easy task.

Since we used django, it has a module which handles the connection of the database, so we only had to add the dependencies into the requirements.txt file and add the credentials to the django settings for the database.

The easiest part gere generating the models for the application, beacause the entities and fields were well defined in the assignment and django has good management for managing the models in the database.

The most difficult part were learing how to use the scaffold module to generate the CRUD pages and urls, but once we manage to setup the module we start working much faster, it save us a lot of time because we didn't had to setup the urls for each model in django urls file, we just made the templates to override the default ones.

To do the specific queries for the data tables, we used django backend to do the queries, which are very powerfull and weren't too difficult use and we just had to display the data as a table in the fronted.

The most time-consuming task were refactoring the search page to implement pagination beacause I've done it based on post requests and I had to change the logic to use get requests and manually filter it with the page number selected.
