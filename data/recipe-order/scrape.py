#!/usr/bin/python3
import json
import os
import sys
import time
import urllib
from recipe_scraper.recipe_scrapers import scrap_me, AllRecipes

# give the url as a string, it can be url from any site listed below
url = sys.argv[1] if len(sys.argv) > 1 else 'http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx'

try:
    #scrap_me = scrap_me(url)
    scrap_me = AllRecipes(url)
    scrape_time = time.time()

    is_file = url.startswith("file://")
    if is_file:
        filename = url[len("file://"):]
        scrape_time = os.path.getmtime(filename)
        url = "http://allrecipes.com/Recipe/{}/".format(url.split("/")[-1].split(".")[0])

    out = {
        "url": url,
        "title": scrap_me.title(),
        "ingredients": scrap_me.ingredients(),
        "instructions": [instruction for instruction in scrap_me.instructions().split("\n") if instruction != ''],
        "footnotes": [footnote for footnote in scrap_me.footnotes().split("\n") if footnote != ''],
        "total_time_minutes": scrap_me.total_time(),
        "cook_time_minutes": scrap_me.cook_time(),
        "prep_time_minutes": scrap_me.prep_time(),
        "photo_url": scrap_me.photo_url(),
        "rating_stars": scrap_me.rating_stars(),
        "review_count": scrap_me.review_count(),
        "error": False,
        "time_scraped": int(scrape_time),
        "author": scrap_me.submitter(),
        "description": scrap_me.submitter_description(),
    }
except urllib.error.HTTPError:
    out = {
        "url": url,
        "error": True,
        "time_scraped": int(time.time()),
    }
except ConnectionResetError:
    sys.exit(1)

#print(url)
print(json.dumps(out, sort_keys=True))
