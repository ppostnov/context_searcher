from request_searcher.candidates_parser import WebParser
from request_searcher.request_definer import RequestDefiner
from request_searcher.candidates_searcher import CandidatesSearcher
from request_searcher.similarity import TextComparor
from tools.var_tools import list_of_dicts_to_csv
from tools.var_tools import read_text_file

from urllib.parse import urlparse
import os


class RequestSearcher():
    SEARCHER_API_KEY = "4358ADF7C4004B4DBA7C47988473BEB3"
    IGNORE_HOSTS = r'metadata\ignore_hosts.txt'

    def __init__(self):
        self.request_definer = RequestDefiner()
        self.candidates_searcher = CandidatesSearcher(self.SEARCHER_API_KEY)
        self.parser = WebParser()
        self.restricted_domains = self.get_restricted_domains()

    def links_to_domains(self, links: list) -> list:
        """
        Converts a list of full links 
        into a list of domains with scheme
        """
        domains = []
        for link in links:
            uri = urlparse(link)
            if not self.is_restricted_domain(uri):
                domains.append(f"{uri.scheme}://{uri.netloc}/")
        return domains

    def get_restricted_domains(self) -> list:
        """ignore_hosts.txt to list"""
        domains = read_text_file(self.IGNORE_HOSTS).split(',')
        return [domain.strip() for domain in domains]

    def is_restricted_domain(self, uri: urlparse) -> bool:
        """Checks if provided URI is restricted"""
        for domain in self.restricted_domains:
            if domain in uri.netloc.split('.'):
                return True
        return False


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
        domains = self.links_to_domains(links)
        domains = set(domains)
        parsed = [self.parse_candidate(domain) for domain in domains]
        list_of_dicts_to_csv(parsed)

        pass