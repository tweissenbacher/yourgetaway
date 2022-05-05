basedir = path.abspath(path.dirname(__file__))
DB_NAME = "database.sqlite"
DB_ABS_PATH = path.join(basedir, 'data', DB_NAME)

db = SQLAlchemy()
