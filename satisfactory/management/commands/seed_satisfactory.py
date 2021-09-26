from satisfactory.models import *
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
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

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    Buildable.objects.all().delete()
    Product.objects.all().delete()
    NodeType.objects.all().delete()
    Recipe.objects.all().delete()


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    f = open('./satisfactory/seeds/items.json',)
    items = json.load(f)
    for item in items:
        try:
            stack_size = int(item.get('stackSize'))
        except:
            stack_size = None
        try:
            Product.objects.create(
                version="u4",
                displayname=item['displayName'],
                image_link=item.get('image'),
                description=item['description'],
                tier=item.get('researchTier') or None,
                blueprint_path=item.get('blueprintPath'),
                stack_size=stack_size,
                sink_value=None if not item.get('sink_value') else int(item.get('sink_value').replace(' ', ''))
            )
        except IntegrityError:
            print(item, 'bestond al')
            pass

    f = open('./satisfactory/seeds/buildings.json',)
    buildings = json.load(f)
    for building in buildings:
        try:
            saved_building = Buildable.objects.get(version="u4", displayname=building.get('displaynname'))
            continue
        except:
            pass
        try:
            height = None if '\u2013' in building['size_length'] else float(building['size_length'].replace(' m', ''))
        except:
            height = None
        try:
            Buildable.objects.create(
                version="u4",
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
                size_length=None if not building.get('size_length') else None if '\u2013' in building['size_length'] else float(building['size_length'].replace(' m', '')),
                size_height=height
            )
        except IntegrityError:
            print(building, 'bestond al')
            pass



    f = open('./satisfactory/seeds/recipes.json',)
    recipes = json.load(f)
    for recipe in recipes:
        print(recipe)
        recipe['machine'] = recipe.get('machine').replace(' × ', '')
        try:
            created_recipe = Recipe.objects.create(
                version="u4",
                displayname=recipe.get('recipename'),
                type='alternate' if recipe.get('alternate') else 'default', 
                machine=Buildable.objects.get(displayname=(recipe.get('machine'))),
                machine_seconds=recipe.get('machine_seconds')
            )
        except IntegrityError:
            print(recipe, 'bestond al')
            continue
        for ingredient in recipe.get('inputs'):
            productname = ingredient.get('product').replace('\xa0', '')
            try:
                created_recipe.ingredients.add(
                    Product.objects.get(version="u4", displayname=productname),
                    through_defaults={'amount': ingredient.get('amount'), 'amount_min': ingredient.get('recipe_min')}
                )
            except ObjectDoesNotExist:
                print('Product input bestaat niet - ' + productname)
        for product in recipe.get('outputs'):
            productname = product.get('product').replace('\xa0', '')
            try:
                created_recipe.products.add(
                    Product.objects.get(version="u4", displayname=productname),
                    through_defaults={'amount': product.get('amount'), 'amount_min': product.get('recipe_min'), 'mj': product.get('mj')}
                )
            except ObjectDoesNotExist:
                print('Product output bestaat niet - ' + productname)
                continue
            if created_recipe.type == 'default':
                created_recipe.default_recipe_products.add(
                    Product.objects.get(version="u4", displayname=productname)
                )




    # # Add Node types
    # NodeType.objects.bulk_create([
    #     NodeType(key='iron', name='Iron', type='Node'),
    #     NodeType(key='copper', name='Copper', type='Node'),
    #     NodeType(key='limestone', name='Limestone', type='Node'),
    # ])

    # Recipe.objects.bulk_create([
    #     Recipe(key='iron_plate', name='Iron Plate', machine=MachineType('constructor')),
    #     Recipe(key='iron_ingot', name='Iron Ingot', machine=MachineType('smelter')),
    #     Recipe(key='reinforced_iron_plate', name='Reinforced Iron Plate', machine=MachineType('assembler')),
    #     Recipe(key='screw', name='Screw', machine=MachineType('constructor')),
    # ])

    # # Add products
    # Product.objects.bulk_create([
    #     Product(key='iron_ore', name='Iron Ore'),
    #     Product(key='iron_ingot', name='Iron Ingot'),
    #     Product(key='iron_plate', name='Iron Plate', default_recipe=Recipe('iron_plate')),
    #     Product(key='iron_rod', name='Iron Rod'),
    #     Product(key='wire', name='Wire'),
    #     Product(key='cable', name='Cable'),
    #     Product(key='copper_sheet', name='Copper Sheet'),
    #     Product(key='copper_ore', name='Copper Ore'),
    #     Product(key='concrete', name='Concrete'),
    #     Product(key='reinforced_iron_plate', name='Reinforced Iron Plate'),
    #     Product(key='screw', name='Screw'),
    # ])

    # RecipeInput.objects.bulk_create([
    #     RecipeInput(recipe=Recipe('iron_ingot'), product=Product('iron_ore'), amount=30),
    #     RecipeInput(recipe=Recipe('iron_plate'), product=Product('iron_ingot'), amount=30),
    #     RecipeInput(recipe=Recipe('reinforced_iron_plate'), product=Product('iron_plate'), amount=30),
    #     RecipeInput(recipe=Recipe('reinforced_iron_plate'), product=Product('screw'), amount=60),
    #     RecipeInput(recipe=Recipe('screw'), product=Product('screw'), amount=30),
    # ])

    # RecipeOutput.objects.bulk_create([
    #     RecipeOutput(recipe=Recipe('iron_ingot'), product=Product('iron_ingot'), amount=30),
    #     RecipeOutput(recipe=Recipe('iron_plate'), product=Product('iron_plate'), amount=20),
    #     RecipeOutput(recipe=Recipe('reinforced_iron_plate'), product=Product('reinforced_iron_plate'), amount=5),
    #     RecipeOutput(recipe=Recipe('screw'), product=Product('screw'), amount=20),
    # ])

    ##################################################################
