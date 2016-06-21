import os

import tornado.ioloop
import tornado.web
import tornado.options

from handlers import MainHandler
from settings import SQLALCHEMY_DATABASE_URI

if __name__ == "__main__":
    # define your db, then referenced later in your handler as self.db
    tornado.options.define("db_path", default=SQLALCHEMY_DATABASE_URI, type=str)
    # define your endpoint (just / is all that's needed)
    app = tornado.web.Application([
        # where handlers go
        (r"/", MainHandler),
        # where static files are sourced
        # this is too fancy...but maybe you want to use it? ;)
        # (r"/static/", tornado.web.StaticFileHandler, {'path': SOME_PATH_HERE}),
    ], static_path='static', debug=True, autoreload=True)
    # listen on port 8888, so to go to this server open localhost:8888
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
