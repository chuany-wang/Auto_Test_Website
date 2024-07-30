import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.orm import declarative_base
from common.read_data import read_conf

Base = declarative_base()


class InitSqlalchemy:
    def __init__(self):
        envir = sys.platform.lower()
        db_config = read_conf(value='DB')

        if envir == 'win32':
            self.db_string = db_config.get('TEST')
        elif envir == 'linux':
            self.db_string = db_config.get('PRO')

        self.engine = create_engine(self.db_string)
        self.Session = sessionmaker(bind=self.engine)

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def session(self):
        with self.session_scope() as session:
            return session


db = InitSqlalchemy().session()
