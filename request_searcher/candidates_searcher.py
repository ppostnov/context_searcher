import requests
from serpwow.google_search_results import GoogleSearchResults
import json

# create the serpwow object, passing in our API key
serpwow = GoogleSearchResults("9B865C39F952484AAE51D0283C79C735")

# set up a dict for the search parameters
params = {
    "q" : "разработка прототипа приложения",
    "engine" : "yandex"
}

# retrieve the search results as JSON
result = serpwow.get_json(params)

# pretty-print the result
print(json.dumps(result, indent=2, sort_keys=True))


# class CandidatesSearcher(object):
