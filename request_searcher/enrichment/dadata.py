import requests
import json


class DaDataEnricher():
    """Uses dadata.ru API to get company info by its INN"""
    def __init__(self, token: str):
        self.query_url = 'https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party'
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {token}"
        }
        self.offer_id = ''
        self.company_name = ''
        self.manager = ''
        self.manager_position = ''
        self.capital = ''
        self.address = ''
        self.inn = ''
        self.ogrn = ''
        self.okato = ''

    def load(self, inn: int):
        data = {'query': str(inn)}
        try:
            resp = requests.post(self.query_url, headers=self.headers, json=data)
            resp.raise_for_status
            return json.loads(resp.text)
        except Exception as exc:
            print('connection issue')

            return None

    def parse_response(self, data: dict):
        suggestions = data['suggestions']
        if suggestions:
            data_prep = suggestions[0]
            try:
                self.company_name = data_prep['value']
            except:
                self.company_name = ''
            try:
                self.manager = data_prep['data']['management']['name']
            except:
                self.manager = ''
            try:
                self.manager_position = data_prep['data']['management']['post']
            except:
                self.manager_position = ''            
            try:
                self.capital = data_prep['data']['capital']['value']
            except:
                self.capital = ''                  
            try:
                self.address = data_prep['data']['address']['value']
            except:
                self.address = ''                              
            try:
                self.inn = data_prep['data']['inn']
            except:
                self.inn = ''     
            try:
                self.ogrn = data_prep['data']['ogrn']
            except:
                self.ogrn = ''                  
            try:
                self.okato = data_prep['data']['okato']
            except:
                self.okato = ''                   
            

    def serialize(self):
        """All attribute types are str"""
        data = {
            "company_name": self.company_name,
            "manager": self.manager,
            "manager_position": self.manager_position,
            "capital": self.capital,
            "address": self.address,
            "inn": self.inn,
            "ogrn": self.ogrn,
            "okato": self.okato
        }
        return data

    def query(self, inn: int):
        loaded = self.load(inn)
        if loaded:
            self.parse_response(loaded)
        return self.serialize()
