from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import SQLALCHEMY_DATABASE_URI
from models import Base, Taco, GoodTopping, BadTopping, Ingredient

import random
import string

TACO_NAMES = [
    'awesome',
    'great',
    'superb',
    'magical',
    'delicious',
    'wonderous'
]

GOOD_TOPPING_NAMES = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z'
]

BAD_TOPPING_NAMES = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h',
    'i',
    'j',
    'k',
    'l',
    'm',
    'n',
    'o',
    'p',
    'q',
    'r',
    's',
    't',
    'u',
    'v',
    'w',
    'x',
    'y',
    'z'
]

if __name__ == '__main__':
    # links to your db and builds the models for you
    engine = create_engine(SQLALCHEMY_DATABASE_URI,
                           convert_unicode=True,
                           echo=False)
    # make your models!
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    db = Session()

    """
    There are 500 tacos total
    Each taco has toppings which are made up of ingredients
    Each topping can have up to 20 ingredients
    """

    for taco_num in range(500):
        taco_num_str = str(taco_num)
        print "Making taco " + taco_num_str
        taco = Taco(name=random.choice(TACO_NAMES) + taco_num_str)
        db.add(taco)
        # flush is necessary so we can assign the toppings to the ingredient
        db.flush()

        # we need different kinds of toppings!
        for topping in random.sample(GOOD_TOPPING_NAMES, random.randint(1, 26)):
            good_topping = GoodTopping(taco_id=taco.id, name=topping)
            db.add(good_topping)
            # flush is necessary so we can assign the toppings to the ingredient
            # db.commit()
            db.flush()

            # now we need ingredients!
            for i in range(random.randint(1, 20)):
                # an ingredient is a random string of 15 chars
                name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
                ingredient = Ingredient(good_topping_id=good_topping.id, name=name)
                db.add(ingredient)

        for topping in random.sample(BAD_TOPPING_NAMES, random.randint(1, 26)):
            bad_topping = BadTopping(taco_id=taco.id, name=topping)
            db.add(bad_topping)
            # flush is necessary so we can assign the toppings to the ingredient
            db.flush()

            # now we need ingredients!
            for i in range(random.randint(1, 20)):
                # an ingredient is a random string of 15 chars
                name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
                ingredient = Ingredient(bad_topping_id=bad_topping.id, name=name)
                db.add(ingredient)

    db.commit()
