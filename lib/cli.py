import click
from model_modules import Category, Recipe, Ingredient, session
from model_modules.instruction import Instruction
# Define get_or_create function
def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance, False
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance, True

@click.group()
def cli():
    """Welcome to Recipe Organizer CLI Application!"""

@cli.command()
def add_recipe():
    """Add a new recipe to the collection."""
    click.echo("Adding a new recipe...")
    name = click.prompt("Enter the recipe name", type=str)
    category = click.prompt("Enter the category", type=str)
    
    # Get or create category
    category_obj, _ = get_or_create(session, Category, name=category)

    # Create recipe
    recipe = Recipe(name=name, category=category_obj)
    session.add(recipe)
    session.commit()

    # Adding instructions
    click.echo(f"Adding instructions for '{name}':")
    instructions = []
    while True:
        click.echo("Select an option:")
        click.echo("1. Add Instruction")
        click.echo("2. Save Instructions")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            instruction_text = click.prompt("Enter instruction")
            instructions.append(instruction_text)
        elif choice == 2:
            for idx, instruction_text in enumerate(instructions, start=1):
                instruction = Instruction(step=idx, description=instruction_text, recipe=recipe)
                session.add(instruction)
            session.commit()
            click.echo("Instructions saved successfully!")
            break
        else:
            click.echo("Invalid choice. Please enter a valid option.")

    # Adding ingredients
    click.echo(f"Adding ingredients for '{name}':")
    ingredients = []
    while True:
        click.echo("Select an option:")
        click.echo("1. Add Ingredient")
        click.echo("2. Save Ingredients")

        choice = click.prompt("Enter your choice", type=int)

        if choice == 1:
            ingredient_name = click.prompt("Enter ingredient name")
            ingredients.append(ingredient_name)
        elif choice == 2:
            for ingredient_name in ingredients:
                ingredient = Ingredient(name=ingredient_name, recipe=recipe)
                session.add(ingredient)
            session.commit()
            click.echo("Ingredients saved successfully!")
            break
        else:
            click.echo("Invalid choice. Please enter a valid option.")

    click.echo(f"Recipe '{name}' added successfully!")

@cli.command()
def search():
    """Search for recipes by ingredients or categories."""
    query = click.prompt("Enter your search query", type=str)
    # Search for recipes by name, ingredients, or category
    recipes = (
        session.query(Recipe)
        .filter(Recipe.name.like(f'%{query}%') |
                Recipe.category.has(Category.name.like(f'%{query}%')) |
                Recipe.ingredients.any(Ingredient.name.like(f'%{query}%')))
        .all()
    )

    if recipes:
        click.echo("Matching Recipes:")
        for recipe in recipes:
            click.echo(f"- {recipe.name} ({recipe.category.name})")
    else:
        click.echo("No matching recipes found.")
@cli.command()
def exit():
    """Exit the application."""
    click.echo("Exiting...")
    raise SystemExit

# Display menu and keep the application running
while True:
    click.echo("Select an option:")
    click.echo("1. Add Recipe")
    click.echo("2. Search for Recipes")
    click.echo("3. Exit")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        add_recipe()
    elif choice == 2:
        search()
    elif choice == 3:
        exit()
    else:
        click.echo("Invalid choice. Please enter a valid option.")
