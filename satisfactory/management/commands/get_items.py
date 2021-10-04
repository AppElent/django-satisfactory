from satisfactory.models import *
from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
import json
from itertools import product
import re

def table_to_2d(table_tag):
    rowspans = []  # track pending rowspans
    rows = table_tag.find_all('tr')

    # first scan, see how many columns we need
    colcount = 0
    for r, row in enumerate(rows):
        cells = row.find_all(['td', 'th'], recursive=False)
        # count columns (including spanned).
        # add active rowspans from preceding rows
        # we *ignore* the colspan value on the last cell, to prevent
        # creating 'phantom' columns with no actual cells, only extended
        # colspans. This is achieved by hardcoding the last cell width as 1. 
        # a colspan of 0 means “fill until the end” but can really only apply
        # to the last cell; ignore it elsewhere. 
        colcount = max(
            colcount,
            sum(int(c.get('colspan', 1)) or 1 for c in cells[:-1]) + len(cells[-1:]) + len(rowspans))
        # update rowspan bookkeeping; 0 is a span to the bottom. 
        rowspans += [int(c.get('rowspan', 1)) or len(rows) - r for c in cells]
        rowspans = [s - 1 for s in rowspans if s > 1]

    # it doesn't matter if there are still rowspan numbers 'active'; no extra
    # rows to show in the table means the larger than 1 rowspan numbers in the
    # last table row are ignored.

    # build an empty matrix for all possible cells
    table = [[None] * colcount for row in rows]

    # fill matrix from row data
    rowspans = {}  # track pending rowspans, column number mapping to count
    for row, row_elem in enumerate(rows):
        span_offset = 0  # how many columns are skipped due to row and colspans 
        for col, cell in enumerate(row_elem.find_all(['td', 'th'], recursive=False)):
            # adjust for preceding row and colspans
            col += span_offset
            while rowspans.get(col, 0):
                span_offset += 1
                col += 1

            # fill table data
            rowspan = rowspans[col] = int(cell.get('rowspan', 1)) or len(rows) - row
            colspan = int(cell.get('colspan', 1)) or colcount - col
            # next column is offset by the colspan
            span_offset += colspan - 1
            value = cell.get_text()
            for drow, dcol in product(range(rowspan), range(colspan)):
                try:
                    table[row + drow][col + dcol] = value
                    rowspans[col + dcol] = rowspan
                except IndexError:
                    # rowspan or colspan outside the confines of the table
                    pass

        # update rowspan bookkeeping
        rowspans = {c: s - 1 for c, s in rowspans.items() if s > 1}

    return table

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
    filename_items = f'./satisfactory/management/commands/items_{satisfactory_version}.json'
    filename_recipes = f'./satisfactory/management/commands/recipes_{satisfactory_version}.json'
    print(f'Data will be saved to {filename_items, filename_recipes}')

    page = requests.get('https://satisfactory.fandom.com/wiki/Category:Items')
    pagesoup = BeautifulSoup(page.content, "html.parser")

    pagediv = pagesoup.find(id="mw-pages")
    links = pagediv.find_all('a')
    item_list = []
    recipe_list = []
    for link in links:
        print(link.get_text() + ' - ' + link.get('href'))
        if '/' in link.get_text().lower().replace('/wiki/', '') or '\%EC\%B' in link.get_text().lower():
            print('---> Skipping item because language is not english')
            continue
        page = requests.get('https://satisfactory.fandom.com/' + link.get('href'))
        soup_page = BeautifulSoup(page.content, "html.parser")
        infobox = soup_page.find("aside", {"class": "portable-infobox"})
        if infobox is None:
            continue
        single_item = {}

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
            single_item[item.get('data-source')] = value
            #print(item.get('data-source') + ': ' + value)
        sink_value = infobox.find('a', {"href": "/wiki/AWESOME_Sink"})
        if sink_value is not None:
            single_item['sink_value'] = sink_value.parent.find_next('div').get_text()
        item_list.append(single_item)


        # Get recipes
        if link.get_text() in ['Cup', 'Quantum Computer', 'Superposition Oscillator', 'SAM Ore']:
            print('---> Item wil be skipped, has no crafting table, so no recipes will be saed')
            continue
        obtaining = soup_page.find(id="Obtaining")
        if obtaining is None:
            continue
        crafting = obtaining.find_next(id="Crafting")
        if crafting is None:
            continue
        craftingtable = crafting.find_next("table")
        try:
            recipes = table_to_2d(craftingtable)
        except Exception as e:
            print(f"--->Item {single_item['displayName']} heeft geen recepten of is niet goed gegaan", e)
            continue
        columns = len(recipes[0])
        
        for recipe in recipes[1:]:
            current_column = 1
            inputs = []
            outputs = []
            recipe_object = {}
            recipe_object['recipename'] = recipe[0].replace('Alternate', '').replace(': ', '')
            recipe
            already_found = next((x for x in recipe_list if x.get('recipename') == recipe_object['recipename']), None)
            if already_found:
                print(f"---> Recipe {already_found['recipename']} is already present")
                continue
            recipe_object['alternate'] = True if recipe[0].endswith('Alternate') else False
            previous_column = ''
            for recipecolumn in recipe[1:]:
                column_name = recipes[0][current_column]
                current_column = current_column + 1
                if recipecolumn == previous_column:
                    continue
                elif column_name == "Building":
                    recipemachine = recipecolumn
                    first_digit = re.search(r"\d", recipecolumn).start()
                    recipemachine = recipecolumn[0:first_digit].replace('×', '').strip()
                    recipe_sec = int(recipecolumn[first_digit:].replace(' sec', '').replace(' × ', ''))
                elif column_name == 'Prerequisites':
                    recipe_object['prerequisites'] = recipecolumn
                elif recipecolumn == '\xa0':
                    pass
                elif column_name == "Ingredients":
                    recipeinput = recipecolumn.split(' × ')
                    try:
                        first_digit = re.search(r"\d", recipeinput[1]).start()
                        recipe_min = float(recipeinput[1][first_digit:].split(' / min')[0])
                        productname = recipeinput[1].replace(f"{str(recipe_min).replace('.0', '')} / min", '')
                    except:
                        recipe_min = None
                        productname = recipeinput[1]
                    productname = productname.replace("\u00a0", "")
                    inputs.append({"product": productname, "amount": float(recipeinput[0]), "recipe_min": recipe_min})
                elif column_name == "Products":
                    recipeinput = recipecolumn.split(' × ')
                    try:
                        match = re.search(r'/ min(.*) MJ', recipeinput[1])
                        if not match:
                            recipe_mj = None
                        else:
                            recipe_mj = float(re.search(r'/ min(.*) MJ', recipeinput[1]).group(1))
                        first_digit = re.search(r"\d", recipeinput[1]).start()
                        recipe_min = float(recipeinput[1][first_digit:].split(' / min')[0])
                        if recipe_mj is None:
                            productname = recipeinput[1].replace(f"{str(recipe_min).replace('.0', '')} / min", '')
                        else:
                            productname = recipeinput[1].replace(f"{str(recipe_min).replace('.0', '')} / min{str(recipe_mj).replace('.0', '')} MJ/item", '')
                    except:
                        recipe_min = None
                        recipe_mj = None
                        productname = recipeinput[1]
                    productname = productname.replace("\u00a0", "")
                    outputs.append({"product": productname, "amount": float(recipeinput[0]), "recipe_min": recipe_min, "mj": recipe_mj})
                previous_column = recipecolumn
            recipe_object['inputs'] = inputs
            recipe_object['outputs'] = outputs
            recipe_object['machine'] = recipemachine
            recipe_object['machine_seconds'] = recipe_sec
            print(f"---> Recipe {recipe_object['recipename']} is added to the list")
            recipe_list.append(recipe_object)




    with open(filename_items, 'w') as outfile:
        json.dump(item_list, outfile)
    with open(filename_recipes, 'w') as outfile:
        json.dump(recipe_list, outfile)