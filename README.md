# tornadoOptimization
Optimization to display bunch of tacos with toppings and ingredients using Tornado and Postgress

#### Project description

Verify that everything is up to specs and improve on it as follows:

In your database you have a bunch of tacos, which have toppings, which in turn have ingredients.
We need that data displayed to the user somehow!
This is an application that displays the data to the user. However, there has to be a way to make it look better...
This is an application that nobody would ever use, so it's your job to make it better!
Fix up the frontend, backend, db schema, build_models.py, whatever you're best at!
You can delete all the data in the db and recreate it (via editing build_models.py) but you need to make sure you keep within the specs below.
There's more to do than time allows, so prioritize what you are best at and tackle that first
Bonus points for following Python/JS/HTML best practices (hint: you might enounter some existing stuff that needs fixing up!)

There are 500 tacos total
Each taco has toppings which are made up of ingredients
There are 26 good toppings and 26 bad toppings
Each taco can have up to 26 good and up to 26 bad toppings
Each topping can have up to 20 ingredients

##### Constraints

1. Page loads in < 1 sec
2. You need to use Tornado with Postgres
3. You need to display at least 200 tacos on the page at all times
4. The ingredients of each taco need to be accessible somehow on the page
5. We want to display the total ingredient count of every taco
6. We want to display the total topping count of every taco
7. We want to signify somehow that taco data goes together
8. We want to display if a topping is bad or not somehow



