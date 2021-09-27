from satisfactory.models import *
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json

# python manage.py seed --mode=refresh

class Command(BaseCommand):
    help = "Get satisfactory buildings and create JSON file"

    def add_arguments(self, parser):
        parser.add_argument('--update', type=str, help="Satisfactory version")

    def handle(self, *args, **options):
        self.stdout.write('Get data')
        run_command(self, options['update'])
        self.stdout.write('done.')

def run_command(self, version):
    """ 

    """

    satisfactory_version = version or 'u4'
    filename = f'./satisfactory/management/commands/buildings_{satisfactory_version}.json'
    print(f'Data will be saved to {filename}')

    page = requests.get('https://satisfactory.fandom.com/wiki/Category:Buildings')
    buildings_soup = BeautifulSoup(page.content, "html.parser")

    building_pages = buildings_soup.find(id="mw-pages")
    building_pages_links = building_pages.find_all('a')
    i = 0
    buildings = []
    for link in building_pages_links:
        i = i + 1
        print(link.get_text() + ' - ' + link.get('href'))
        if '/' in link.get_text().lower().replace('/wiki/', ''):
            print('---> Building is being skipped because the language it not english')
            continue
        page = requests.get('https://satisfactory.fandom.com/' + link.get('href'))
        building_page = BeautifulSoup(page.content, "html.parser")
        infobox = building_page.find("aside", {"class": "portable-infobox"})
        if infobox is None:
            continue
        building = {}
        def has_data_source(tag):
            return tag.has_attr('data-source')
        for item in infobox.find_all(has_data_source):
            if item.get('data-source') == 'image':
                value = item.find_next("img").get('src')
            elif item.get('data-source') is None:
                continue
            elif item.find('div') is not None:
                value = item.find('div').get_text()
            else:
                value = item.get_text()
            building[item.get('data-source')] = value
        buildings.append(building)

    with open(filename, 'w') as outfile:
        json.dump(buildings, outfile)