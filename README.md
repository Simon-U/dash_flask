# Example Dashboard protected by Flask

## Getting started

1. Clone the Repo. `git clone git@github.com:Simon-U/dash_example.git`
2. Move into the folder `cd dash_example`
3. Make a virtual enviroment `python3 -m venv env`
4. Activate the enviroment. On linux `source env/bin/activate`
5. Install the packages `pip install -r requirements.txt`
6. Start the application `gunicorn wsgi:app`
7. Stop the server with Ctrl + C
8. Start again `gunicorn -w 2 wsgi:app`

The restart currently needs to be done to first initialise the database. If multiple workers are started directly, they collide while initialising the database.

