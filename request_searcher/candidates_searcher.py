import requests
from serpwow.google_search_results import GoogleSearchResults
import json


class CandidatesSearcher(object):
    """
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.engines = ["yandex", "google"]

    def serpwow_request(self, keywords: str, engine: str) -> dict:
        """
        """
        serpwow = GoogleSearchResults(self.api_key)
        params = {
            "q": keywords,
            "engine": engine
        }                                                 
        return serpwow.get_json(params)
    
    def parser(self, data: dict) -> list:
        """
        """
        results = list()
        for result in data["organic_results"]:
            results.append(
                    {
                        "domain": result["domain"],
                        "link": result["link"],
                        "title": result["title"],
                        "engine": data["search_parameters"]["engine"]
                    }
                )
        return results

    def request(self, keywords: str) -> dict:
        """
        """
        output = list()
        for engine in self.engines:
            data = self.serpwow_request(keywords, engine)
            output.extend(self.parser(data))

        candidates = {
            "query": keywords,
            "candidates": output
        }        
        return candidates