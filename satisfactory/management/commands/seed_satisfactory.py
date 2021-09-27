from satisfactory.models import *
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError, DataError
import random
import json

# python manage.py seed --mode=refresh

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")
        parser.add_argument('--update', type=str, help="Satisfactory version")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'], options['update'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    Buildable.objects.all().delete()
    Product.objects.all().delete()
    NodeType.objects.all().delete()
    Recipe.objects.all().delete()


def run_seed(self, mode, version):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    satisfactory_version = version or 'u4'

    #
    # Creating items
    #
    #
    f = open(f'./satisfactory/management/commands/items_{satisfactory_version}.json',)
    items = json.load(f)
    for item in items:
        print(f"Item {item.get('displayName')} is being added")
        # Setting the stack_size variable to None if some weird error exposes
        try:
            stack_size = int(item.get('stackSize'))
        except:
            stack_size = None

        # Try creating object, fail if already exists
        try:
            Product.objects.create(
                version=satisfactory_version,
                displayname=item['displayName'],
                image_link=item.get('image'),
                description=item['description'],
                tier=item.get('researchTier') or None,
                blueprint_path=item.get('blueprintPath'),
                stack_size=stack_size,
                sink_value=None if not item.get('sink_value') else int(item.get('sink_value').replace(' ', ''))
            )
        except IntegrityError:
            print(f"{item.get('displayName')} already exists")
            pass

    #
    # Creating buildings
    #
    f = open(f'./satisfactory/management/commands/buildings_{satisfactory_version}.json',)
    buildings = json.load(f)
    for building in buildings:
        print(f"Building {building.get('displayName')} is being added")
        # If there is already an object present in database, skip the line
        try:
            saved_building = Buildable.objects.get(version=satisfactory_version, displayname=building.get('displaynname'))
            continue
        except:
            pass

        # Set height variable (dealing with different formats in JSON file)
        try:
            height = None if '\u2013' in building['size_height'] else float(building['size_height'].replace(' m', ''))
        except:
            height = None
        try:
            length = None if '\u2013' in building['size_length'] else float(building['size_length'].replace(' m', ''))
        except:
            length = None

        # Try creating object or fail if object already exists
        try:
            buildable = Buildable.objects.create(
                version=satisfactory_version,
                displayname=building.get('displayName'),
                image_link=building.get('image'),
                description=building.get('description'),
                tier=building.get('researchTier'),
                category=building.get('category'),
                subcategory=building.get('subCategory') or None,
                power_usage=None if not building.get('powerUsage') else None if '-' in building.get('powerUsage') else float(building.get('powerUsage').replace(' MW', '')),
                overclockable=(True if building.get('overclockable') == 'Yes' else False),
                inputs_conveyer=1,
                outputs_conveyer=1,
                inputs_pipeline=0,
                outputs_pipeline=0,
                size_width=None if not building.get('size_width') else float(building.get('size_width').replace(' m', '')),
                size_length=length,
                size_height=height
            )

            # Get all ingredients from JSON line and add them as related objects
            for column in building:
                if column.startswith('ingredient'):
                    value = building.get(column)
                    productname = value.split('×  ')[1].strip()
                    amount = value.split('×  ')[0].strip()
                    try:
                        product = Product.objects.get(version=satisfactory_version, displayname=productname)
                    except ObjectDoesNotExist:
                        product = Product.objects.create(version=satisfactory_version, displayname=productname)
                    buildable.ingredients.add(
                        product,
                        through_defaults={'amount': amount}
                    )
        except IntegrityError:
            print(building.get('displayName'), 'bestond al')
            pass

    #
    # Create recipes (depends on buildings and products)
    #
    f = open(f'./satisfactory/management/commands/recipes_{satisfactory_version}.json',)
    recipes = json.load(f)
    for recipe in recipes:
        recipe['machine'] = recipe.get('machine').replace(' × ', '')
        print(f'Recipe {recipe.get("recipename")} is being added')
        try:
            created_recipe = Recipe.objects.create(
                version=satisfactory_version,
                displayname=recipe.get('recipename'),
                type='alternate' if recipe.get('alternate') else 'default', 
                machine=Buildable.objects.get(displayname=(recipe.get('machine'))),
                machine_seconds=recipe.get('machine_seconds')
            )
        except IntegrityError:
            continue
        except DataError:
            print('Recipe cannot be created, something is wrong with data', recipe)

        # Creating related entries for product (ingredients). First try to GET a product. If not exists, create it.
        for ingredient in recipe.get('inputs'):
            productname = ingredient.get('product').replace('\xa0', '')
            try:
                product_object = Product.objects.get(version=satisfactory_version, displayname=productname)
            except ObjectDoesNotExist:
                print('--> Product input bestaat niet - ' + productname)
                product_object = Product.objects.create(version=satisfactory_version, displayname=productname)
            created_recipe.ingredients.add(
                product_object,
                through_defaults={'amount': ingredient.get('amount'), 'amount_min': ingredient.get('recipe_min')}
            )
        
        # Creating related entries for product (output). First try to GET a product. If not exists, create it.
        for product in recipe.get('outputs'):
            productname = product.get('product').replace('\xa0', '')
            try:
                product_object = Product.objects.get(version=satisfactory_version, displayname=productname)
            except ObjectDoesNotExist:
                print('--> Product output bestaat niet - ' + productname)
                product_object = Product.objects.create(version=satisfactory_version, displayname=productname)
            created_recipe.products.add(
                product_object,
                through_defaults={'amount': product.get('amount'), 'amount_min': product.get('recipe_min'), 'mj': product.get('mj')}
            )
            if created_recipe.type == 'default':
                created_recipe.default_recipe_products.add(
                    Product.objects.get(version=satisfactory_version, displayname=productname)
                )

