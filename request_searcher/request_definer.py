import pymorphy2
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
from nltk.corpus import stopwords
import string
import re
import itertools
nltk.download('stopwords')


class RequestDefiner:
    """
    class for request creator and enricher
    """

    def __init__(self):

        # Analizer for tokenizing and lemmitizing
        self.morph = pymorphy2.MorphAnalyzer()
        # Stopwords for data cleaning
        self.stop_words = set(stopwords.words('russian'))
        # Punctuation for data cleaning
        self.punctuations = list(string.punctuation)

        # REQUEST OBJECT CREATION (see below)
        #self.data_object()

    def set_request_string(self, req_str: str = ''):
        # Full text of RZHD request
        self.req_str = req_str

    def set_request_keyword(self, req_list: list = []):
        # Full text of RZHD request
        self.req_list = req_list

    def define_fulltext(self):
        """
        method: return full-text or merge it from keyword list
        raises exception if no full text or keywords list are added
        """

        if self.req_str:
            return self.req_str
        elif self.req_list:
            full_text = ''
            for i in self.req_list:
                if isinstance(i, list):
                    full_text = full_text + " " + ' '.join(i)
                else:
                    full_text = full_text + " " + str(i)

            return full_text
        else:
            raise Exception('Request is empty')

    def define_tokens(self):
        """
        method: return word-tokens for full-text or keywords list
        raises exception if no full text or keywords list are added
        """

        if self.req_str:
            #remove https and non digit_alphabet symbols
            text = re.sub(r'http\S+', '', self.req_str)
            text = re.sub(r'[\W_]+', ' ', text)
            #perform tokenizing
            word_tokens = word_tokenize(text, language="russian")
            #remove stopwords and punctuations
            word_tokens = [w for w in word_tokens if not w in self.stop_words]
            word_tokens = [w for w in word_tokens if not w in self.punctuations]
            return word_tokens
        elif self.req_list:
            word_tokens = []
            for i in self.req_list:
                #add token from keywords list
                if isinstance(i, list):
                    for j in i:
                        # add token from sublist
                        word_tokens.append(j)
                else:
                    word_tokens.append(i)

            return word_tokens
        else:
            raise Exception('Request is empty')

    def define_lemmatized(self):
        """
        method: return lemmitized word-tokens
        """

        morphed = []
        if self.tokens:
            # lemmatize every token
            for i in self.tokens:
                morphed.append(self.morph.parse(i)[0].normal_form)

        return morphed

    def request_list(self):
        """
        method: return several options or texts for requests based on keywords list
        """

        if self.req_list:
            request_collection = []

            # prepare keywords list
            for i in self.req_list:
                if isinstance(i, list):
                    request_collection.append(i)
                else:
                    request_collection.append([i])

            # create all combinations of keywords
            request_collection = list(itertools.product(*request_collection))

            # create list of lines for request
            request = []
            for item in request_collection:
                line = ' '.join(item)
                request.append(line)

        elif self.req_str:
            request = [self.req_str]
        else:
            raise Exception('Request is empty')

        return request


    def request_enricher(self):
        """
        method: enriches requests list to obtain more results
        """
        # TODO
        pass
        return []


    def data_object(self, req_str: str = '', req_list: list = []):

        """
        method: create json-like dictionary with request info:

        tags - TBD: tags of request
        tokens - tokenized fulltext or keywords
        lemmatized_tokens - lemmatized tokenized fulltext or keywords
        request_description - TBD: some metainfo of request
        full_text - fulltext without changes or concanated keywords list
        requests - variants of text requests for search Engines

        """

        # Full text of RZHD request
        self.req_str = req_str
        # List of Keywords defined manually
        self.req_list = req_list


        self.full_text = self.define_fulltext()
        self.tokens = self.define_tokens()
        self.tags = []
        self.lemmatized_tokens = self.define_lemmatized()
        self.requests = self.request_list()

        self.obj_dict = {
            "tags": self.tags,
            "tokens": self.tokens,
            "lemmatized_tokens": self.lemmatized_tokens,
            "request_description": '',
            "full_text": self.full_text,
            "requests": self.requests

        }

        return self.obj_dict

    