# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__) # create application instance
app.config.from_object(__name__) # load config from this file

# Load default config and override config from an envirionment variable

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, 'iat222_finalproject.db'),
    SECRET_KEY = 'development key',
    USERNAME = 'admin',
    PASSWORD = 'default'
))
app.config.from_envvar('IAT222_FINALPROJECT_SETTINGS', silent=True)

def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv
