#!/bin/sh
seq 1 300000 | while read id; do echo "http://allrecipes.com/recipe/${id}"; done | sort >/tmp/wget.urls
seq 0 39 | parallel -j40 -- sh download.sh "{}" 40 /tmp/wget.urls
find $(pwd)/pages/ -printf "%P\n" | sort -h | while read html; do echo "file://$(pwd)/pages/${html}"; done | parallel python3 scrape.py >allrecipes.json
jq -r '.photo_url' <allrecipes.json | sort -u >/tmp/photos.urls
seq 0 39 | parallel -j40 -- sh download-photo.sh "{}" 40 /tmp/photos.urls
