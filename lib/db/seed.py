from model_modules import Category, Recipe, Ingredient, Instruction, Base, session, engine

Base.metadata.create_all(bind=engine)

def seed_database():
    # Seed categories
    categories = ["Breakfast", "Lunch", "Dinner", "Dessert", "Snack"]
    for category_name in categories:
        category = Category(name=category_name)
        session.add(category)
    session.commit()

    # Seed recipes
    recipes_data = {
        "Pancakes": {
            "category": "Breakfast",
            "instructions": [
                "Mix flour, eggs, milk, sugar, baking powder, and salt in a bowl.",
                "Heat a lightly oiled griddle or frying pan over medium-high heat.",
                "Pour or scoop the batter onto the griddle, using approximately 1/4 cup for each pancake.",
                "Brown on both sides and serve hot."
            ],
            "ingredients": ["Flour", "Eggs", "Milk", "Butter", "Sugar", "Baking powder", "Salt"]
        },
        "Spaghetti": {
            "category": "Dinner",
            "instructions": [
                "Bring a large pot of lightly salted water to a boil.",
                "Cook spaghetti in the boiling water, stirring occasionally until cooked through but firm to the bite, about 12 minutes; drain.",
                "Heat olive oil in a large skillet over medium heat; cook and stir garlic until lightly browned, about 1 minute.",
                "Add ground beef, onion, salt, and black pepper; cook and stir until browned and crumbly, 5 to 7 minutes.",
                "Pour diced tomatoes and tomato sauce into the skillet; season with sugar, Italian seasoning, basil, salt, and pepper.",
                "Simmer sauce for 10 minutes; add spaghetti and cook, stirring occasionally, until heated through and flavors are blended, about 10 minutes more."
            ],
            "ingredients": ["Spaghetti pasta", "Tomato sauce", "Ground beef", "Onion", "Garlic", "Olive oil", "Salt", "Pepper"]
        }
    }

    for recipe_name, recipe_data in recipes_data.items():
        category = session.query(Category).filter_by(name=recipe_data["category"]).first()
        if category:
            recipe = Recipe(name=recipe_name, category=category)
            session.add(recipe)
            session.commit()

            # Seed instructions
            instructions = recipe_data["instructions"]
            for idx, instruction_desc in enumerate(instructions, start=1):
                instruction = Instruction(step=idx, description=instruction_desc, recipe=recipe)
                session.add(instruction)
            session.commit()

            # Seed ingredients
            ingredients = recipe_data["ingredients"]
            for ingredient_name in ingredients:
                ingredient = Ingredient(name=ingredient_name, recipe=recipe)
                session.add(ingredient)
            session.commit()

if __name__ == "__main__":
    seed_database()
