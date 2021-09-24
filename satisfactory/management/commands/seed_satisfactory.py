from satisfactory.models import *
from django.core.management.base import BaseCommand
import random

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
    MachineType.objects.all().delete()
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

    # Create MachineType
    MachineType.objects.bulk_create([
        MachineType(name='Smelter', key='smelter'),
        MachineType(name='Constructor', key='constructor'),
        MachineType(name='Assembler', key='assembler'),
        MachineType(name='Manufacturer', key='manufacturer'),
        MachineType(name='Water extractor', key='water_extractor'),
    ])

    # Add Node types
    NodeType.objects.bulk_create([
        NodeType(key='iron', name='Iron', type='Node'),
        NodeType(key='copper', name='Copper', type='Node'),
        NodeType(key='limestone', name='Limestone', type='Node'),
    ])

    Recipe.objects.bulk_create([
        Recipe(key='iron_plate', name='Iron Plate', machine=MachineType('constructor')),
        Recipe(key='iron_ingot', name='Iron Ingot', machine=MachineType('smelter')),
        Recipe(key='reinforced_iron_plate', name='Reinforced Iron Plate', machine=MachineType('assembler')),
        Recipe(key='screw', name='Screw', machine=MachineType('constructor')),
    ])

    # Add products
    Product.objects.bulk_create([
        Product(key='iron_ore', name='Iron Ore'),
        Product(key='iron_ingot', name='Iron Ingot'),
        Product(key='iron_plate', name='Iron Plate', default_recipe=Recipe('iron_plate')),
        Product(key='iron_rod', name='Iron Rod'),
        Product(key='wire', name='Wire'),
        Product(key='cable', name='Cable'),
        Product(key='copper_sheet', name='Copper Sheet'),
        Product(key='copper_ore', name='Copper Ore'),
        Product(key='concrete', name='Concrete'),
        Product(key='reinforced_iron_plate', name='Reinforced Iron Plate'),
        Product(key='screw', name='Screw'),
    ])

    RecipeInput.objects.bulk_create([
        RecipeInput(recipe=Recipe('iron_ingot'), product=Product('iron_ore'), amount=30),
        RecipeInput(recipe=Recipe('iron_plate'), product=Product('iron_ingot'), amount=30),
        RecipeInput(recipe=Recipe('reinforced_iron_plate'), product=Product('iron_plate'), amount=30),
        RecipeInput(recipe=Recipe('reinforced_iron_plate'), product=Product('screw'), amount=60),
        RecipeInput(recipe=Recipe('screw'), product=Product('screw'), amount=30),
    ])

    RecipeOutput.objects.bulk_create([
        RecipeOutput(recipe=Recipe('iron_ingot'), product=Product('iron_ingot'), amount=30),
        RecipeOutput(recipe=Recipe('iron_plate'), product=Product('iron_plate'), amount=20),
        RecipeOutput(recipe=Recipe('reinforced_iron_plate'), product=Product('reinforced_iron_plate'), amount=5),
        RecipeOutput(recipe=Recipe('screw'), product=Product('screw'), amount=20),
    ])

    ##################################################################

