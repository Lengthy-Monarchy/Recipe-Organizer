# from .session_file import session
# from lib.model_modules.models import Category, Recipe, Ingredient
from model_modules import Category, Recipe, Ingredient, Base, session, engine
Base.metadata.create_all(bind=engine)
def seed_database():
    # Seed categories
    breakfast = Category(name="Breakfast")
    lunch = Category(name="Lunch")
    dinner = Category(name="Dinner")
    dessert = Category(name="Dessert")
    snack = Category(name="Snack")

    session.add_all([breakfast, lunch, dinner, dessert])
    session.commit()

    # Seed recipes
    pancakes = Recipe(name="Pancakes", instructions="Instructions for making pancakes", category=breakfast)
    spaghetti = Recipe(name="Spaghetti", instructions="Instructions for making spaghetti", category=dinner)

    session.add_all([pancakes, spaghetti])
    session.commit()

    # Seed ingredients
    pancakes_ingredients = [
        Ingredient(name="Flour", recipe=pancakes),
        Ingredient(name="Eggs", recipe=pancakes),
        Ingredient(name="Milk", recipe=pancakes),
        Ingredient(name="Butter", recipe=pancakes),
        Ingredient(name="Sugar", recipe=pancakes),
        Ingredient(name="Baking powder", recipe=pancakes),
        Ingredient(name="Salt", recipe=pancakes)
    ]

    spaghetti_ingredients = [
        Ingredient(name="Spaghetti pasta", recipe=spaghetti),
        Ingredient(name="Tomato sauce", recipe=spaghetti),
        Ingredient(name="Ground beef", recipe=spaghetti),
        Ingredient(name="Onion", recipe=spaghetti),
        Ingredient(name="Garlic", recipe=spaghetti),
        Ingredient(name="Olive oil", recipe=spaghetti),
        Ingredient(name="Salt", recipe=spaghetti),
        Ingredient(name="Pepper", recipe=spaghetti)
    ]

    session.add_all(pancakes_ingredients)
    session.add_all(spaghetti_ingredients)
    session.commit()

if __name__ == "__main__":
    seed_database()
