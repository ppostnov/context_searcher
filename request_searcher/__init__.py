from request_searcher.candidates_parser import WebParser
from request_searcher.request_definer import RequestDefiner
from request_searcher.candidates_searcher import CandidatesSearcher
from request_searcher.similarity import TextComparor

from urllib.parse import urlparse


class RequestSearcher():
    SEARCHER_API_KEY = '9B865C39F952484AAE51D0283C79C735'

    def __init__(self):
        self.request_definer = RequestDefiner()
        self.candidates_searcher = CandidatesSearcher(self.SEARCHER_API_KEY)
        self.parser = WebParser()

    def define_request(self, req_list: list, req_len: int=None):
        return self.request_definer.data_object(req_list=req_list, 
                                                req_len=req_len)

    def search_candidates(self, query: str):
        return self.candidates_searcher.request(keywords=query)

    def parse_candidate(self, url: str):
        return self.parser.parse(url=url)

    def compare_text(self):
        pass

    def search(self, req_list: list, req_len: int=1):
        """
        UNFINISHED!!!
        """
        candidates = []
        requests = self.define_request(req_list, req_len)
        for request in requests.get("requests"):
            candidates += self.search_candidates(request).get('candidates')
        links = [candidate.get('link') 
                    for candidate in candidates]
        links = set(links)
        parsed = [self.parse_candidate(link) for link in links]
        print(parsed)

        pass