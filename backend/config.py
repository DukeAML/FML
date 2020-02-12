import os
from unipath import Path

basedir = os.path.abspath(os.path.dirname(__file__))
BASEDIR = Path(__file__).parent

class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False