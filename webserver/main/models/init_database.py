import os
from sqlalchemy import text

from main.config import get_config_by_name

global db_session, dbBase, db, engine

pg_user = get_config_by_name('PG_USER')
pg_password = get_config_by_name('PG_PASSWORD')
pg_host = get_config_by_name('PG_HOST')
pg_port = get_config_by_name('PG_PORT')
pg_database = get_config_by_name('PG_DATABASE')
db_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_database}"
pool_size = get_config_by_name('SQLALCHEMY_POOL_SIZE')

if os.getenv('FLASK_SERVER', 'True') == 'True':
    from flask_sqlalchemy import SQLAlchemy
    from main.flask_app import app

    app.debug = get_config_by_name('DEBUG')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_string
    app.config['SQLALCHEMY_POOL_SIZE'] = pool_size
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    db_session = db.session
    dbBase = db.Model
else:
    from sqlalchemy import orm
    from sqlalchemy.ext.declarative import declarative_base
    import sqlalchemy as sa

    dbBase = declarative_base()
    engine = sa.create_engine(db_string)
    dbBase.metadata.bind = engine
    db_session = orm.scoped_session(orm.sessionmaker())(bind=engine)


def execute_raw_query(sql_str):
    sql = text(sql_str)
    if os.getenv('FLASK_SERVER', 'True') == 'True':
        return db.engine.execute(sql)
    else:
        return engine.execute(sql)


def init_database(initialization_done=True):
    if not initialization_done:
        if os.getenv('FLASK_SERVER', 'True') == 'True':
            db.create_all()
        else:
            dbBase.metadata.create_all()


def delete_tables():
    if os.getenv('FLASK_SERVER', 'True') == 'True':
        db.drop_all()
    else:
        dbBase.metadata.drop_all()
