import json
import os
from typing import Dict, List, Tuple
import requests
from lxml import html
from tqdm import tqdm

# The api key is public so it does not need to be hidden in a .env file
BASE_URL = "http://rpi.apis.acalog.com/v1/"
# It is ok to publish this key because I found it online already public
DEFAULT_QUERY_PARAMS = "?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml"
CHUNK_SIZE = 500


filepath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
root = os.path.dirname(filepath)
# Opens the subjects.JSON and returns a list of subject code
def get_subjs():
    subjs = []
    f = open(root + '/frontend/src/data/subjs.json', 'r') #make sure to close at end of file
    tmp = json.load(f)
    for subj in tmp:
        subjs.append(subj)
    f.close()
    return subjs

subjs = get_subjs()

def get_courses():
    f = open(root + '/frontend/src/data/courses.json','r')
    ret = json.load(f)
    f.close()
    return ret

course_dict = get_courses()

def clean_list(s: str) -> str:
    return "".join([x for x in s if x.isalnum() or x.isspace()])

# returns the list of catalogs with the newest one being first
# each catalog is a tuple (year, catalog_id) ex: ('2020-2021', 21)
def get_catalogs() -> List[Tuple[str, int]]:
    catalogs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getCatalogs"
        ).text.encode("utf8")
    )
    catalogs = catalogs_xml.xpath("//catalogs/catalog")

    ret: List[Tuple[str, int]] = []
    # For each catalog get its year and id and add that as as tuples to ret
    for catalog in catalogs:
        catalog_id: int = catalog.xpath("@id")[0].split("acalog-catalog-")[1]
        catalog_year: str = catalog.xpath(".//title/text()")[0].split(
            "Rensselaer Catalog "
        )[1]
        ret.append((catalog_year, catalog_id))

    # sort so that the newest catalog is always first
    ret.sort(key=lambda tup: tup[0], reverse=True)
    return ret