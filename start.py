#! /usr/bin/env python

# -*- coding: utf-8 -*-

import json
from text import FuzzyMatching

# doc0 = "stop pr service job"
# doc1 = "build job"
# doc2 = "get pr service status"
# doc3 = "I love Shanghai"
# doc4 = "build"

text = "get build status"
TEMPLATE_FILE = "text/templates.json"

def test_matching():
    with open(TEMPLATE_FILE, "r") as f:
        template_data = json.load(f)
    templates_build = template_data["templates_build"]
    templates_status = template_data["templates_status"]

    fuzzy_matching = FuzzyMatching(templates_build, templates_status, text)
    result = fuzzy_matching.text_analyzed()
    if result == 'build':
        print('build job!')
    elif result == 'status':
        print('retrieve status!')
    else:
        print('no')


if __name__ == "__main__":
    test_matching()

