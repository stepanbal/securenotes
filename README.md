# Securenotes

Securenotes is a webapp which manage your notes and let to encode and decode it.
It also supports the ability of registering users and using the application by different users.
Each of them will have their own notes and categories.

App lets you to create categories, rename and delete them. You can create notes in categories.
Both secret and not secret. If you create secret note, you should type password (it may be different for each note
and it is not the same you chose when registering).

Your secret text is encoding by SHA256 algorithm and saving in database. When you want to read or edit it,
you should type password again. Don't forget your secret password for the note.
It is not stored in the database, so it cannot be restored.
Also you can edit your notes. In this case, the time of the last editing will be automatically updated.
Of course notes can also be deleted.

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
