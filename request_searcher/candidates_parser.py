import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError


class WebParser():
    """Resource parser"""
    def __init__(self):
        #input attributes
        self.offer_id = ''
        self.url = ''

        #intermediate attributes
        self.host_url = ''
        self.contact_link = ''

        #output attributes
        self.phones = []
        self.emailes = []
        self.title = ''
        self.inn = ''
        self.clean_html = ''
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br'
        }

    def clean_url(self, url: str):
        parsed = urllib.parse.urlparse(url)
        return f'{parsed.scheme}://{parsed.netloc}/'

    def get_host(self, url: str):
        parsed = urllib.parse.urlparse(url).netloc.split('.')
        host = parsed[0] if parsed[0] != 'www' else parsed[1]
        return host

    def get_html(self, url: str):
        try:
            response = requests.get(url, headers=self.headers)
        except requests.ConnectionError:
            return ''
        if response.status_code == 200:
            return response.text
        else:
            return ''

    def get_soup(self, html: str, parser: str='html.parser'):
        try:
            soup = BeautifulSoup(html, parser)
        except:
            soup = None
        return soup

    def clear_html(self, raw_html: str): 
        try:
            clean = self.get_soup(raw_html, "lxml").text
            return clean if clean else ''
        except:
            return ''

    @staticmethod
    def clean_text(text: str):
        patterns = [(r"[\n\.\,\d]", " "),
                    (r"\t|[\n\s\_]{2,}", "")]
        for pattern in patterns:
            text = re.sub(pattern[0], pattern[1], text)
        return text

    @staticmethod
    def clean_phonenum(phone: str, country: str="RU"):
        try:
            phonenum = phonenumbers.parse(phone, country)
            if phonenumbers.is_valid_number(phonenum):
                formatted = phonenumbers.format_number(phonenum, phonenumbers.PhoneNumberFormat.E164)
                return formatted
            else:
                return None
        except:
            return None

    @staticmethod
    def clean_email(email: str):
        try:
            valid = validate_email(email)
            email = valid.email
            return email
        except EmailNotValidError:
            return None

    @staticmethod
    def find_regex(text: str, regex: str):
        """RegEx executor plus dedup"""
        found = re.findall(regex, text)
        dedup = []
        [dedup.append(item) for item in found if item not in dedup]
        return dedup

    def find_phone(self, text: str):
        pattern = r"(\+?[7|8]?\s?\(?\d{3}\)?\s?\d{3}[\s|\-]?\d{2}[\s|\-]?\d{2})"
        phones = self.find_regex(text, pattern)
        format_phones = []
        for phone in phones:
            clean_phone = self.clean_phonenum(phone)
            if clean_phone:
                if clean_phone not in format_phones:
                    format_phones.append(clean_phone)
        return format_phones

    def find_email(self, text: str):
        pattern = r"[\w|\d|\-]+\@.{,20}\.\w{2,10}"
        emails = self.find_regex(text, pattern)
        valid_emails = []
        for email in emails:
            valid_email = self.clean_email(email)
            if valid_email:
                if valid_email not in valid_emails:
                    valid_emails.append(valid_email)
        return valid_emails

    def find_company_name(self, raw_html: str):
        soup = self.get_soup(raw_html)
        try:
            title = soup.head.title
            return title.text
        except:
            return ''

    def find_inn(self, raw_html: str):
        soup = self.get_soup(raw_html)
        try:
            inn = soup.find(string=re.compile("ИНН"))
            if inn:
                pure_inn = self.find_regex(inn, r'\d{10}')
            return pure_inn[0] if pure_inn else ''
        except:
            return ''

    def find_contact_page(self, raw_html: str):
        lookup = ['contact', 'contacts', 'kontakt']
        soup = self.get_soup(raw_html)
        contact = ''
        try:
            raw_links = soup.find_all('a')
            links = [link.get('href') for link in raw_links]
            if links:
                for link in links:
                    if link:
                        for item in lookup:
                            if item in link and not contact:
                                contact = link       
                if contact:
                    if self.host_url not in contact:
                        contact = urllib.parse.urljoin(self.host_url, contact)
        except:
            contact = ''
        return contact

    def look_for_contact_info(self, clean_html: str='', raw_html=''):
        self.phones = self.find_phone(clean_html)
        self.emails = self.find_email(clean_html)
        self.inn = self.find_inn(raw_html)
        
    def serialize_output(self):
        output = {
            "url": self.host_url, #str
            "name": self.title, #str
            "phone": ';'.join(self.phones), #list
            "email": ';'.join(self.emails), #list
            "inn": self.inn, #str
            "contacts": self.contact_link, #str
            "description": self.clean_text(self.clean_html)[:4000] #str
        }
        return output

    def parse(self, url: str):
        self.url = url
        self.host_url = self.clean_url(self.url)
        raw_html = self.get_html(self.url)
        self.clean_html = self.clear_html(raw_html)
        self.title = self.find_company_name(self.get_html(self.host_url))

        self.contact_link = self.find_contact_page(raw_html)
        if self.contact_link:
            contact_html = self.get_html(self.contact_link)
            clean_contact_html = self.clear_html(contact_html)
        else:
            contact_html = ''
            clean_contact_html = ''
        self.look_for_contact_info(clean_html=self.clean_html+clean_contact_html, 
                                    raw_html=raw_html+contact_html)

        return self.serialize_output()

    