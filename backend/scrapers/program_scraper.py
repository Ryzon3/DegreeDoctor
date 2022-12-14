from typing import Dict, List, Tuple
import requests
from lxml import html
from tqdm import tqdm
import json
import unicodedata
from degree_util import subjs, course_dict, filepath, get_catalogs, root
from collections import OrderedDict

# The api key is public so it does not need to be hidden in a .env file
BASE_URL = "http://rpi.apis.acalog.com/v1/"
# It is ok to publish this key because I found it online already public
DEFAULT_QUERY_PARAMS = "?key=3eef8a28f26fb2bcc514e6f1938929a1f9317628&format=xml"
CHUNK_SIZE = 500

# Returns a list of program ids for a given catalog
def get_program_ids(catalog_id: str) -> List[str]:
    programs_xml = html.fromstring(
        requests.get(
            f"{BASE_URL}search/programs{DEFAULT_QUERY_PARAMS}&method=listing&options[limit]=0&catalog={catalog_id}"
        ).text.encode("utf8")
    )
    return programs_xml.xpath('//result[type="Baccalaureate"]/id/text()')

# <<< need rework for programs >>>
def course_from_string(inp, subjs):
    for subj in subjs:
        fnd = inp.find(subj)
        if fnd != -1:
            if inp[fnd+8].isdigit() or inp[fnd+8] == "X":
                if inp[fnd+5] != '6':
                    return inp[fnd:fnd+4] + inp[fnd+5:fnd+9]

# Normalize a string, using unicode data. Remove all weird whitespace tag 
def norm_str(str):
    return unicodedata.normalize("NFKD",str).strip()

# Take a list of list and remove empty list elements
def striplist(lstr): 
    return list(filter(None, lstr))

# splits content and normalizes the string using the token 'Credit Hours'
def split_content(str):
    ret = []
    while (str.find("Credit Hours") != -1):
        tmp = str.find("Credit Hours") + 16
        ret.append(norm_str(str[:tmp]))
        str = str[tmp:]
    return ret

# removes footnote tags 
def rem_footnote(str):
    while (str.find("(See footnote") != -1):
        str = str[:str.find("(See footnote")] + str[str.find("(See footnote") + 22:]
    return str

# removes special message for arch semester
def rem_arch(str):
    s = "ExceptionProcess."
    if (str.find(s) != -1):
        str = str[str.find(s) + len(s):]
    return str

# removes all unneccesary data in strings
def rem_all(str):
    return rem_footnote(rem_arch(str))

# parses the template for visual purposes in the JSON 
def parse_template(semesters): 
    sems = OrderedDict()
    curr_year = 1
    first_sem_in_year = True
    extra = []
    for item in semesters:
        template_str = str(curr_year) + "-" 
        # Extra content 
        if curr_year > 4:
            extra.extend(item)
            continue
        # Year 1,2 and 4
        if curr_year != 3:
            if first_sem_in_year:
                template_str += "Fall"
            elif not first_sem_in_year:
                template_str += "Spring"
                curr_year += 1
            first_sem_in_year = not first_sem_in_year
        else:
            if first_sem_in_year:
                template_str += "Summer"
            elif not first_sem_in_year:
                template_str += "Fall or Spring"
                curr_year += 1
            first_sem_in_year = not first_sem_in_year 
        sems[template_str] = item
    sems["Extra"] = extra
    return sems

# gets the subj string from a given string
def get_subj(str):
    for subj in subjs: 
        fnd = str.find(subj)
        if fnd != -1:
            return str[fnd:fnd+4]
    return ""

# hardcoded replacement for certain strings UPDATE/FIX Later (if its possible to like... not hardcode this)
def replace_subj(str):
    if str == "CS" or str == "Computer Science":
        return "CSCI"
    if str == "Mathematics":
        return "MATH"
    return str

# seperates classes that may be stacked together and finds elective classes' department codes
def get_elec(str):
    ret = []
    spltstr = str.split(" or ")
    for s in spltstr:
        fnd_e = s.find("Elective")
        fnd_o = s.find("Option")
        if fnd_e != -1:
            ret.append(replace_subj(s[0:fnd_e-1]))
        if fnd_o != -1:
            ret.append(replace_subj(s[0:fnd_o-1]))
    return ret

# seperates the class name from the subj code for parsing
def seperate_class(str):
    fnd = str.find(" - ")
    if fnd != -1:
        return str[fnd+3:]
    return str

# seperates class strings into seperates if there exists
# more than one option
def seperate_class_list(inp):
    ret = []
    tmp = inp.split(" or ")
    for t in tmp:
        ret.extend(t.split(" Or "))
    return ret

# removes ' or ' from lists for duplicate classes
def remove_or_from_list(inp):
    ret = []
    for i in inp:
        tmp = [seperate_class_list(c) for c in i]
        ret.append(tmp)
    return ret

# adds classes and credits for a given set and dictionary,
# (it is messy because we have to deal with duplicate strings 
# which may not be equal but have same classes and are therefore 
# very hard to parse properly without extra logic)
def add_classes_and_credits(str,ret_set,ret_dict):
    if (len(get_subj(str)) > 0):
        ret_set.add(seperate_class(str))
    else:
        tmp = get_elec(str)
        for t in tmp:
            if ret_dict.get(t) != None:
                ret_dict[t] += 4
            else: 
                ret_dict[t] = 4
    return (ret_set,ret_dict)

# looks through course.json and returns credit amounts for classes
# returns a list of objects ranging from usually 1 to 4/6 credit #'s
def get_credits(inp):
    if course_dict.get(inp) == None:
        return ""
    return course_dict[inp]['credits']

# takes in a requirement dict and returns total sum of credits
def generate_credits(inp):
    total = 0
    for key in inp.keys():
        total += inp[key]
    return total

# generates the credit requirements for classes for the programs.json file
def generate_requirements(inp):

    # we must handle duplicates seperately as parsing is problematic
    ret = {}
    duplicates = {}
    named_classes = set()

    # remove the 'extra' part for parsing
    inp = inp[:8]
    # prepares input by splitting multiple classes into their own sections
    inp = remove_or_from_list(inp)

    # logic for each sem/class
    for sem in inp:
        for item in sem:
            # if size is more than one, this is a duplicate class and must
            # be handled seperately
            if (len(item) > 1):
                for i in item:
                    (named_classes,duplicates) = add_classes_and_credits(i,named_classes,duplicates)
            else: 
                (named_classes,ret) = add_classes_and_credits(item[0],named_classes,ret)

    # duplicates show up twice on catalog so we must halve values and use a set for
    # named classes such that we do not double count
    duplicates = {key: int(value / 2) for key, value in duplicates.items()}

    # add our duplicates to our main requirements
    for key in duplicates.keys():
        if ret.get(key) != None:
            ret[key] += duplicates[key]
        else:
            ret[key] = duplicates[key]

    # look up credit totals for each named class and add
    for key in named_classes:
        tmp = list(get_credits(key))
        if (len(tmp) > 1):
            ret[key] = tmp[1:][0]
        elif (len(tmp) == 1):
            ret[key] = tmp[0]
    
    return ret

# takes in xml file of of one semester of courses
# input:  core.xpath("../cores/core/children/core")  
def parse_semester(inp):
    ret = []
    for classes in inp:
        title =classes.xpath("./title")
        title = title[0].text_content().strip()
        
        # logic for 'extra' content
        if title.count("Fall") == 0 and title.count("Spring") == 0 and title.count("Arch") == 0:
            content = classes.xpath("./content")
            content_txt = content[0].text_content().strip()
            
            ret.append([title, norm_str(content_txt)])

        else:
            sem = []
            # Parsing electives include: Free electives, Hass electives, Capstones
            electives = classes.xpath("./content")
            for c in electives:
                tmp = split_content(rem_all(c.text_content()))
                sem.extend(tmp)
                    
            # Parsing Major course
            block = classes.xpath("./courses")
            for b in block: 

                # content is main classes, adhoc sometimes has important content
                # that needs to be filtered
                content = b.xpath("./include")
                adhoc = b.xpath("./adhoc/content")
                extra = ""
                s = ""
                
                for a in adhoc: 
                    if (len(rem_all(a.text_content())) > 0):
                        extra += rem_all(a.text_content())

                # logic for adding extra content to end of normal parse        
                for c in content:
                    if (len(c.text_content()) > 0):
                        s = norm_str(c.text_content())
                        if (len(extra) > 0):
                            if (extra[0] == " "):
                                s += extra
                            else:
                                s += " " + extra
                        sem.append(s)

            course_list = striplist(sem)
            if (len(course_list) > 0):
                ret.append(course_list)
    return ret

def parse_courses(core, name, year):
    # Get an array of all semesters and parse them
    semester_list = core.xpath("./children/core")
    courses = parse_semester(semester_list)
    return courses

def get_program_data(pathway_ids: List[str], catalog_id, year) -> Dict:
    data = {}
    ids = "".join([f"&ids[]={path}" for path in pathway_ids])
    url = f"{BASE_URL}content{DEFAULT_QUERY_PARAMS}&method=getItems&options[full]=1&catalog={catalog_id}&type=programs{ids}"
    pathways_xml = html.fromstring(requests.get(url).text.encode("utf8"))

    pathways = pathways_xml.xpath("//programs/program[not(@child-of)]");
    # For every Major degree
    for pathway in pathways:
        courses = []
        name = pathway.xpath("./title/text()")[0].strip()

        # For now only parse CS
        # if (name != "Computer Science"):
        #     continue
        
        # Get program description
        desc = ""
        if len(pathway.xpath("./content/p/text()")) >= 1:
            desc = pathway.xpath("./content/p/text()")[0].strip()
            desc = ' '.join(desc.split())
        
        # Get the list of years in the program
        cores = pathway.xpath("./cores/core")

        # Parse each school year for courses
        for core in cores:
            courses.extend(parse_courses(core, name, year))
        
        requirements = generate_requirements(courses)
        credit = generate_credits(requirements)
        template = parse_template(courses)
        data[name] = {
                "name": name,
                "description": desc,
                "credits": credit,
                "requirements" : requirements,
                "template": template
            }

    return data

def scrape_pathways():
    print("Starting pathway scraping")
    num_catalog = 1
    catalogs = get_catalogs()
    # take the most recent num_catalog catalogs
    catalogs = catalogs[:num_catalog]

    # Scraping catalogs
    programs_per_year = {}
    for index, (year, catalog_id) in enumerate(tqdm(catalogs)):
        # print(year)
        program_ids = get_program_ids(catalog_id)
        # scraing the program (degree)
        data = get_program_data(program_ids, catalog_id, year)
        programs_per_year[year] = data
    print("Finished program scraping")

    # create JSON obj and write it to file
    json_object = json.dumps(programs_per_year, indent=4)
    with open(root + "/frontend/src/data/programs.json", "w") as outfile:
        outfile.write(json_object)
    return programs_per_year

if __name__ == "__main__":
    scrape_pathways()