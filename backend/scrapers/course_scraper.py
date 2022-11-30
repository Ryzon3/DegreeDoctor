# This scraper is mainly sourced from the QUACs team and
# is a modified version of their catalog scraper

from typing import Dict, List, Tuple
import requests
from lxml import html
from tqdm import tqdm
import json
import unicodedata
from degree_util import subjs, root, get_catalogs, clean_str, norm_str, trim_space

# The api key is public so it does not need to be hidden in a .env file
BASE_URL = "http://rpi.apis.acalog.com/v1/"
# It is ok to publish this key because I found it online already public
DEFAULT_QUERY_PARAMS = "?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml"
CHUNK_SIZE = 500

# Returns a list of course ids for a given catalog
def get_course_ids(catalog_id: str) -> List[str]:
    courses_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}search/courses{DEFAULT_QUERY_PARAMS}&method=listing&options[limit]=0&catalog={catalog_id}"
        ).text.encode("utf8")
    )
    return courses_xml.xpath("//id/text()")

# Finds and returns a cleaned up description of the course
def get_catalog_description(fields, course_name):
    found_name = False
    # The description is always the next full field after the course name field
    # Itearte through the fields until we find the course name field and then return the next filled field
    for field in fields:
        if found_name == False:
            name = field.xpath(".//*/text()")
            if name and name[0] == course_name:
                found_name = True
        else:
            description = field.xpath(".//*/text()")
            if description:
                clean_description = " ".join(" ".join(description).split())
                clean_description = clean_str(clean_description)
                # Short descriptions are usually false positives
                if clean_description.startswith("Prerequisite"):
                    return ""
                elif len(clean_description) > 10:
                    return clean_description.encode("ascii", "ignore").strip().decode().strip()

    return ""
# function should return an object where object = 
# ["required" = [Calc1, Calc2...], "One of" = [[Option 1, Option 2], [Option 1, Option 2]]]
def checkreq(list):
    for subj in subjs:
        if list.find(subj + ' ') != -1:
            if list.find(subj + ' ') + 5 < len(list):
                if list[list.find(subj)+5].isdigit():
                    return True
    return False

# splits requirements for parsing
def split_req(str):
    reqset = str.split(" AND ")
    final = []
    for req in reqset:
        new = req.split(" OR ")
        for n in new:
            if not checkreq(n):
                new.remove(n)
        final.append(new)
    return final

# uses unicodedata to normalize str and then splits pre-requirements into
# 'required' and 'one_of'
def get_prereq(str): 
    str = norm_str(str)
    reqs = []
    one_of = []
    reqset = split_req(str)
    for req in reqset:
        tmp = []
        if len(req) > 1:
            for r in req:
                tmp.extend(courses_from_string(r))
            one_of.append(tmp)
        else:
            reqs.extend(courses_from_string(''.join(req)))
    return { "required" : reqs, "one_of" : one_of }

# returns the range of credits of a given course while checking for edge cases
def get_credit(str):
    credit = []
    low = 0
    high = 0
    if str.isdigit():
        # Case "4", etc.
        credit.append(int(str))
    elif str.find(" to ") != -1 or str.find("-") != -1 or str.find(" or ") != -1: 
        if (str[:1].isdigit() and str[len(str)-1:].isdigit()):
            # Stress checking is in format "1 ( to ,-, or ) 4" or similar format
            low = int(str[:1])
            high = int(str[len(str)-1:])
        elif str.find("1") != -1 and str.find("4") != -1: 
            # Case where formatting is slightly off like "1/4 credit"
            low = 1
            high = 4
        for x in range(low,high+1):
            credit.append(x)
    elif str[:1].isdigit(): 
        # Edge cases like "4 (course...", "3 credits each semester"
        credit.append(int(str[:1]))
    else: 
        # Edge cases like "Arranged.", "Variable."
        credit.append(str)
    return credit

 # REFACTOR (Clean up instead of searching from all subj)
 # gets the courses in a given string
def courses_from_string(inp):
    crses = set()
    for subj in subjs:
        sp = inp.split(subj)
        if len(sp) > 1: 
            for item in sp: 
                if item[1:5].isdigit():
                    crses.add(subj + '-' + item[1:5])
    return list(crses)

def get_course_data(course_ids: List[str], catalog_id) -> Dict:
    data = {}
    # Break the courses into chunks of CHUNK_SIZE to make the api happy
    course_chunks = [
        course_ids[i : i + CHUNK_SIZE] for i in range(0, len(course_ids), CHUNK_SIZE)
    ]
    subj_input = []
    f = open(root + '/frontend/src/data/input.json', 'r')
    f = json.load(f)
    for subj in f:
        subj_input.append(subj)

    for chunk in course_chunks:
        ids = "".join([f"&ids[]={id}" for id in chunk])
        url = f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getItems&options[full]=1&catalog={catalog_id}&type=courses{ids}"

        courses_xml = html.fromstring(requests.get(url).text.encode("utf8"))
        courses = courses_xml.xpath("//courses/course[not(@child-of)]")
        for course in courses:
            subj = course.xpath("./content/prefix/text()")[0].strip()
            if not (subj in subj_input):
                continue
            ID = course.xpath("./content/code/text()")[0].strip()
            if ID[0] == '6' or ID[0] == '9':
                continue
            course_name = clean_str(trim_space(norm_str(course.xpath("./content/name/text()")[0].strip())))
            fields = course.xpath("./content/field")
            year = ""
            semesters = []
            cross_listed = {}
            prereqs = []
            credit = []
            professors = []

            
            base = int(fields[0].get('type')[-3:])
            for field in fields:
                field_text = field.xpath("./descendant-or-self::*/text()")
                if len(field_text) > 0:
                    field_text = field_text[0].strip()
                    if field.get('type')[-3:] == str(base - 4): 
                        credit = get_credit(field_text)
                    elif field.get('type')[-3:] == str(base - 8):
                        if len(field_text) > 0:
                            crs = courses_from_string(field.text_content().upper())
                            for item in crs:
                                if item.find(subj + '-' + str(ID)) == -1:
                                    cross_listed[subj] = str(ID)
                    elif field.get('type')[-3:] == str(base - 11):
                        if "fall" in field_text.lower():
                            semesters.append("fall")
                        if "spring" in field_text.lower():
                            semesters.append("spring")
                        if "summer" in field_text.lower():
                            semesters.append("summer")
                        if "even" in field_text.lower():
                            year = "even"
                        if "odd" in field_text.lower():
                            year = "odd"
                        if "instructor" in field_text.lower():
                            year = "UIA"
                        if len(year) == 0:
                            year = "all"
                    elif field.get('type')[-3:] == str(base - 13):
                        field_text = field.text_content()
                        if len(field_text) > 0:
                            prereqs = get_prereq(field_text.upper())

            data[course_name] = {
                "name": course_name,
                "subject": subj,
                "ID": ID,
                "description": get_catalog_description(fields, course_name),
                "credits" : credit,
                "prerequisites": prereqs,
                "crosslisted": cross_listed,
                "offered": {
                    "year" : year,
                    "semesters" : semesters,
                },
                "properties": {
                    "CI": False,
                    "MR": False
                },
                "professors": professors
            }

    return data

def scrape_courses():
    print("Starting courses scraping")
    catalogs = get_catalogs()

    catalogs = catalogs[:4]
    catalogs.reverse()
    courses_per_year = {}
    for index, (year, catalog_id) in enumerate(tqdm(catalogs)):
        course_ids = get_course_ids(catalog_id)
        data = get_course_data(course_ids, catalog_id)
        courses_per_year.update(data)
    # Serializing json
    json_object = json.dumps(courses_per_year,sort_keys=True, indent=2, ensure_ascii=False)
 
    # Writing to sample.json
    with open(root + "/frontend/src/data/courses.json", "w") as outfile:
        outfile.write(json_object)
        print("Finished courses scraping")
    
    return courses_per_year

if __name__ == "__main__":
    scrape_courses()