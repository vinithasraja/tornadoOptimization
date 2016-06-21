from base import BaseRequestHandler

import models

class MainHandler(BaseRequestHandler):
    def get(self):
        tacos = self.db.query(models.Taco).limit(3).all()
        kwargs = {
            'tacos': tacos
        }
        self.render("index.html", title="Wake Testing Project", **kwargs)
