import csv
import os
from typing import List
from unidecode import unidecode

def list_of_dicts_to_csv(dictionary: dict, path: str=r'output', 
                                filename: str='output.csv'):
    """Writes a list of dicts into a csv file"""
    rootfolder = os.path.join(os.getcwd(), path)
    fullpath = os.path.join(rootfolder, filename)
    keys = dictionary[0].keys()
    with open(fullpath, 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(dictionary)

def read_text_file(filepath: str) -> str:
    """Reads plane text from a text file"""
    file = open(filepath, 'r')
    return file.read()


def slugify_list(input_list: List[str], fin_size: int=32) -> str:
    """Converts a list of strings (e.g. Cyrillic) into 
    a single string of ASCII characters. This function 
    was created to generate file names of the input search 
    queries.
    ['привет', 'пока'] -> 'privet_poka'
    """
    if fin_size <= 1:
        return 'output'
    else:
        output = '_'.join([unidecode(word).replace(' ','_') for word in input_list])
        out_len = min(len(output), fin_size)
        return output[:out_len]