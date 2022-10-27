import json
import aiohttp
import re
import asyncio
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests




def pog_scraper():
    f = open('courses.json','r')
    f1 = json.load(f)
    for course in f1:
        instructorStorage = []
        year = "202209"
        page = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse"
        webpage_response = requests.get(page + '?term_in=' + year + '&subj_in=' + f1[course]["subj"] + '&crse_in=' + f1[course]["ID"] + '&schd_in=L')
        webpage = webpage_response.content
        soup = BeautifulSoup(webpage, "html.parser")
        times = soup.findAll("table", {
            "class": "datadisplaytable",
            "summary": "This table lists the scheduled meeting times and assigned instructors for this class..",
        })
        for time in times:
            split_up = [x.text for x in time.findAll("td")]
            instructor = split_up[6].split('(')[0]
            instructor = re.sub(' +', ' ', instructor).strip()
            if instructor != "TBA":
                instructorStorage.append(instructor)
        res = [*set(instructorStorage)]
        print(res)
        
       

if __name__ == "__main__":
    # instructorStorage = []
    # year = "202209"
    # page = "https://sis.rpi.edu/rss/bwckctlg.p_disp_listcrse"
    # webpage_response = requests.get(page + '?term_in=' + year + '&subj_in=' + "MATH" + '&crse_in=' + "1010" + '&schd_in=L')
    # webpage = webpage_response.content
    # soup = BeautifulSoup(webpage, "html.parser")
    # times = soup.findAll("table", {
    #         "class": "datadisplaytable",
    #         "summary": "This table lists the scheduled meeting times and assigned instructors for this class..",
    #     })
    # for time in times:
    #         split_up = [x.text for x in time.findAll("td")]
    #         instructor = split_up[6].split('(')[0]
    #         instructor = re.sub(' +', ' ', instructor).strip()
    #         if instructor != "TBA":
    #             instructorStorage.append(instructor)
    # res = [*set(instructorStorage)]
    # print(res)
    pog_scraper()

