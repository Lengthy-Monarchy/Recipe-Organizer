import click
from model_modules import Category, Recipe, Ingredient, session

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
@click.option('--name', prompt='Recipe Name', help='Name of the recipe')
@click.option('--instructions', prompt='Instructions', help='Instructions for preparing the recipe')
@click.option('--category', prompt='Category', help='Category of the recipe')
def add_recipe(name, instructions, category):
    """Add a new recipe to the collection."""
    # Get or create category
    category_obj, _ = get_or_create(session, Category, name=category)

    # Create recipe
    recipe = Recipe(name=name, instructions=instructions, category=category_obj)
    session.add(recipe)
    session.commit()
    click.echo(f"Recipe '{name}' added successfully!")

@cli.command()
@click.argument('ingredient')
@click.argument('recipe_name')
def add_ingredient(ingredient, recipe_name):
    """Add an ingredient to an existing recipe."""
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()
    if recipe:
        # Add ingredient to the recipe
        ingredient_obj = Ingredient(name=ingredient, recipe=recipe)
        session.add(ingredient_obj)
        session.commit()
        click.echo(f"Ingredient '{ingredient}' added to '{recipe_name}' recipe successfully!")
    else:
        click.echo(f"Recipe '{recipe_name}' not found!")

@cli.command()
@click.argument('search_query')
def search(search_query):
    """Search for recipes by ingredients or categories."""
    # Search for recipes by name, ingredients, or category
    recipes = (
        session.query(Recipe)
        .filter(Recipe.name.like(f'%{search_query}%') |
                Recipe.category.has(Category.name.like(f'%{search_query}%')) |
                Recipe.ingredients.any(Ingredient.name.like(f'%{search_query}%')))
        .all()
    )

    if recipes:
        click.echo("Matching Recipes:")
        for recipe in recipes:
            click.echo(f"- {recipe.name} ({recipe.category.name})")
    else:
        click.echo("No matching recipes found.")

@cli.command()
@click.argument('recipe_name')
def view(recipe_name):
    """View detailed information about a recipe."""
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()
    if recipe:
        click.echo(f"Recipe Name: {recipe.name}")
        click.echo(f"Category: {recipe.category.name}")
        click.echo("Ingredients:")
        for ingredient in recipe.ingredients:
            click.echo(f"- {ingredient.name}")
        click.echo(f"Instructions:\n{recipe.instructions}")
        click.echo(f"Average Rating: {recipe.average_rating}")
    else:
        click.echo(f"Recipe '{recipe_name}' not found!")

@cli.command()
@click.argument('recipe_name') 
def delete(recipe_name):
    """Delete a recipe."""
    recipe = session.query(Recipe).filter_by(name=recipe_name).first()
    if recipe:
        session.delete(recipe)
        session.commit()
        click.echo(f"Recipe '{recipe_name}' deleted successfully!")
    else:
        click.echo(f"Recipe '{recipe_name}' not found!")

# Display menu and keep the application running
while True:
    click.echo("Select an option:")
    click.echo("1. Add Recipe")
    click.echo("2. Add Ingredient to Recipe")
    click.echo("3. Search for Recipes")
    click.echo("4. View Recipe Details")
    click.echo("5. Delete Recipe")
    click.echo("6. Exit")

    choice = click.prompt("Enter your choice", type=int)

    if choice == 1:
        add_recipe()
    elif choice == 2:
        add_ingredient()
    elif choice == 3:
        search()
    elif choice == 4:
        view()
    elif choice == 5:
        delete()
    elif choice == 6:
        click.echo("Exiting...")  # Provide a message before exiting
        break
    else:
        click.echo("Invalid choice. Please enter a valid option.")
