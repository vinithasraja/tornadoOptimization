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

    bad_toppings = relationship('BadTopping', backref='taco')
    good_toppings = relationship('GoodTopping', backref='taco')

    @property
    def db(self):
        return inspect(self).session

    def toppings(self):
        bad_toppings = self.db.query(BadTopping).filter_by(taco_id=self.id)
        good_toppings = self.db.query(GoodTopping).filter_by(taco_id=self.id)

        return list(bad_toppings) + list(good_toppings)

    def ingredients(self):
        # get ingredients from all toppings
        toppings = self.toppings()
        ingredients_list = []
        for topping in toppings:
            ingredients_list += [ingredient for ingredient in topping.ingredients]
        return ingredients_list

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

    __mapper_args__ = {
        'polymorphic_identity': 'taco'
    }


class GoodTopping(Base):
    __tablename__ = 'waketesting_good_toppings'
    __table_args__ = {}

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    created = Column(types.DateTime, default=datetime.utcnow)
    name = Column(types.String)
    taco_id = Column(types.Integer, ForeignKey('waketesting_tacos.id'))
    # signifies if this is a good topping or not
    is_good = Column(types.Boolean, default=True)

    ingredients = relationship('Ingredient', backref='good_topping')

    __mapper_args__ = {
        'polymorphic_identity': 'good_topping'
    }


class BadTopping(Base):
    __tablename__ = 'waketesting_bad_toppings'
    __table_args__ = {}

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    created = Column(types.DateTime, default=datetime.utcnow)
    name = Column(types.String)
    taco_id = Column(types.Integer, ForeignKey('waketesting_tacos.id'))
    # signifies if this is a good topping or not
    is_good = Column(types.Boolean, default=False)

    ingredients = relationship('Ingredient', backref='bad_topping')

    __mapper_args__ = {
        'polymorphic_identity': 'bad_topping'
    }


class Ingredient(Base):
    __tablename__ = 'waketesting_ingredients'
    __table_args__ = (
        {}
    )

    id = Column(types.Integer, primary_key=True, autoincrement=True)
    created = Column(types.DateTime, default=datetime.utcnow)
    name = Column(types.String)
    good_topping_id = Column(types.Integer, ForeignKey('waketesting_good_toppings.id'), nullable=True)
    bad_topping_id = Column(types.Integer, ForeignKey('waketesting_bad_toppings.id'), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'ingredient'
    }

    # you can only have either a good or a bad topping fk at a time

    @validates('good_topping')
    def validate_good_topping(self, key, address):
        if address and self.bad_topping:
            raise HTTPError(500, reason="ingredient can only belong to one topping!")

    @validates('bad_topping')
    def validate_bad_topping(self, key, address):
        if address and self.good_topping:
            raise HTTPError(500, reason="ingredient can only belong to one topping!")
