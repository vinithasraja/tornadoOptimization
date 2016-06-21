from tornado.web import RequestHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import SQLALCHEMY_DATABASE_URI


class BaseRequestHandler(RequestHandler):

    @property
    def db(self):
        """A way to access your database!"""
        if not hasattr(self, '_dbsession'):
            engine = create_engine(SQLALCHEMY_DATABASE_URI,
                           convert_unicode=True,
                           echo=False)
            Session = sessionmaker(bind=engine)
            self._dbsession = Session()
        return self._dbsession
