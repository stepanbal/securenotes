# Securenotes

Securenotes is a webapp which manage your notes and let to encode and decode it. It also supports the ability of registering users and using
of the application by different users. In addition, each of them will have their own notes and categories.

### Dependencies
- Python 3.8
- Django 2.2.12
- cryptography 2.9.2
- psycopg2-binary 2.8.5

**Also I used:**
- pipenv
- docker 19.03.8
- docker-compose 1.25.0
- postgresql

### Installing

To install app you have to clone code to your computer and build the docker images. You need docker and docker-compose
been installed on your computer. Run next commands:
```
docker-compose build
docker-compose up -d
```
Then you should open your browser and go to [localhost:9000](http://localhost:9000)
