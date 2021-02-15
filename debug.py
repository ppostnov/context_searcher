def debug_candidate_parser():
    """Calls a web address and prints out the result"""
    from request_searcher import RequestSearcher
    parser = RequestSearcher()
    address='https://www.youtube.com/'
    parsed = parser.parse_candidate(address)
    print(parsed['title'])
    sampled = parsed['description'].split(' ')[:50]
    joined = ' '.join(sampled)
    print(joined)
    #print(joined, joined.encode('windows-1252').decode('utf-8'))


def debug_request_definer():
    from request_searcher.request_definer import RequestDefiner
    request_definer = RequestDefiner()

    print(request_definer.data_object(
            req_list=[
                ["Сталь","Медь", "Алюминий"],
                'Насос',
                ["Вода", "Масло", "Пропан"],
                ["Крым", "Норильск"]
            ],
            req_len=45
            )
        )

def debug_candidates_searcher():
    """
    """
    from request_searcher import candidates_searcher
    cs = candidates_searcher.CandidatesSearcher(
        "9B865C39F952484AAE51D0283C79C735"
    )
    print(cs.request("разработка прототипа вагона в нии"))    

def debug_business_logic():
    from request_searcher import RequestSearcher
    searcher = RequestSearcher()
    searcher.search(['Сталь', 'Медь'], 2)

def debug_dict_to_csv():
    from tools.var_tools import list_of_dicts_to_csv
    testdict = [{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
    list_of_dicts_to_csv(testdict)

def debug_read_text():
    from tools.var_tools import read_text_file
    text = read_text_file(r'metadata\ignore_hosts.txt')
    print(text, type(text))


def main():
    """
    Insert a funtion to debug.
    The function must be pre-configured within itself.
    """
    # debug_candidate_parser()
    # debug_request_definer()
    # debug_candidates_searcher()
    # debug_dict_to_csv()
    # debug_business_logic()
    debug_read_text()

if __name__ == '__main__':
    main()

