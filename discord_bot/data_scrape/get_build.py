from bs4 import BeautifulSoup

"""
INPUT: Four soup objects containing all information about champion build
OUTPUT: a list of dictionaries consisting of all the items that is recommended.
DESCRIPTION: get the recommended build of the champion
"""
def get_build(core, fourth, fifth, sixth) -> list:
    items = []
    soups = [core, fourth, fifth, sixth]
    for soup in soups:
        item_blocks = soup.find_all(contains_background_image)
        item_group = list(map(convert_to_dict, item_blocks))
        items.append(item_group)
    return items

def contains_background_image(block):
    return block.has_attr('style') and "background-image" in block['style']

def convert_to_dict(element):
    element = str(element)
    sheet = element[element.find("https") : (element.find("webp") + 4)]
    string_position = element[element.find("background-position:") + 20 : element.find("zoom") - 1].split(" ")
    position = [abs(int(position[0:-2])) for position in string_position]
    return {"sheet": sheet, "position": position}

