from tornado.web import HTTPError
from datetime import datetime, date, timedelta
from sqlalchemy import Column, types, ForeignKey, UniqueConstraint, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm.query import Query
from sqlalchemy.engine.result import RowProxy

Base = declarative_base()


class Taco(Base):
    __tablename__ = 'waketesting_tacos'
    __table_args__ = {}

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    name = Column(types.String, unique=True, index=True)
    created = Column(types.DateTime, default=datetime.utcnow)
    toppings = relationship('Topping', backref='taco')
    #Merging the toppings table
    # bad_toppings = relationship('BadTopping', backref='taco')
    # good_toppings = relationship('GoodTopping', backref='taco')

    @property
    def db(self):
        return inspect(self).session

    def toppings(self, good=True):
        is_good = True if good else False
        toppings = self.db.query(Topping).filter_by(taco_id=self.id, is_good=is_good)
        toppings_list= []

        for g in toppings:
            ingredient_dict = {}
            ingredients_name = [ingredient.name for ingredient in g.ingredients]
            toppings_list.append({
                'topping_name': g.name,
                'ingredients': ingredients_name
            })

        return toppings_list

    # def toppings(self):
    #     bad_toppings = self.db.query(BadTopping).filter_by(taco_id=self.id)
    #     good_toppings = self.db.query(GoodTopping).filter_by(taco_id=self.id)

    #     return list(bad_toppings) + list(good_toppings)

    # def ingredients(self):
    #     # get ingredients from all toppings
    #     toppings = self.toppings()
    #     ingredients_list = []
    #     for topping in toppings:
    #         ingredients_list += [ingredient for ingredient in topping.ingredients]
    #     return ingredients_list

#Planning to use ingredient sum for printing statistics
        def ingredient_sum(self):
        total_sum = 0
        total_toppings = self.toppings()
        for topping in total_toppings:
            if topping.is_good:
                ingredients = self.db.query(Ingredient).filter_by(good_topping_id=topping.id).all()
                for ingredient in ingredients:
                    total_sum += 1
            else:
                ingredients = self.db.query(Ingredient).filter_by(bad_topping_id=topping.id).all()
                for ingredient in ingredients:
                    total_sum += 1
        return total_sum

class Topping(Base):
    __tablename__ = 'waketesting_toppings'
    __table_args__ = {}

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    created = Column(types.DateTime, default=datetime.utcnow)
    name = Column(types.String)
    taco_id = Column(types.Integer, ForeignKey('waketesting_tacos.id'))
    # signifies if this is a good topping or not
    is_good = Column(types.Boolean, default=True)

    ingredients = relationship('Ingredient', backref='topping')

    __mapper_args__ = {
        'polymorphic_identity': 'topping'
    }

class Ingredient(Base):
    __tablename__ = 'waketesting_ingredients'
    __table_args__ = (
        {}
    )

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    created = Column(types.DateTime, default=datetime.utcnow)
    name = Column(types.String)
    topping_id = Column(types.Integer, ForeignKey('waketesting_toppings.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'ingredient'
    }

    # you can only have either a good or a bad topping fk at a time
    #Not required as the topping table is merged
    @validates('good_topping')
    def validate_good_topping(self, key, address):
        if address and self.bad_topping:
            raise HTTPError(500, reason="ingredient can only belong to one topping!")

    @validates('bad_topping')
    def validate_bad_topping(self, key, address):
        if address and self.good_topping:
            raise HTTPError(500, reason="ingredient can only belong to one topping!")

