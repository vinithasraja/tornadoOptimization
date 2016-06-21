from base import BaseRequestHandler

import models
import json

class MainHandler(BaseRequestHandler):
    def get(self):
        tacos = self.db.query(models.Taco).limit(200).all()
        kwargs = {
            'tacos': tacos
        }
        self.render("static/taco.html", title="Wake Testing Project", tacos=tacos)


class TacoHandler(BaseRequestHandler):
    def get(self, tacoid):
        tacos = self.db.query(models.Taco).filter_by(id=tacoid).one()
        good_toppings = tacos.toppings(good=True)
        bad_toppings = tacos.toppings(good=False)
        taco_toppings = {
          'good_toppings': good_toppings,
          'bad_toppings': bad_toppings,
          'name': tacos.name
        }
        self.write(json.dumps(taco_toppings))
