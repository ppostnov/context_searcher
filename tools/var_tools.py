import csv
import os

def list_of_dicts_to_csv(dictionary: dict, path: str=r'output', 
                                filename: str='output.csv'):
    """Writes a list of dicts into a  csv file"""
    rootfolder = os.path.join(os.getcwd(), path)
    fullpath = os.path.join(rootfolder, filename)
    keys = dictionary[0].keys()
    with open(fullpath, 'w') as f:
        w = csv.DictWriter(f, keys)
        w.writeheader()
        w.writerows(dictionary)