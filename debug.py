
def debug_candidate_parser():
    """Calls a web address and prints out the result"""
    from request_searcher import parser
    address = 'http://www.stalekom.ru'
    print(parser.parse(address))


def debug_request_definer():
    from request_searcher import request_definer

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


def main():
    """
    Insert a funtion to debug.
    The function must be pre-configured within itself.
    """
    # debug_candidate_parser()
    debug_request_definer()
    # debug_candidates_searcher()

if __name__ == '__main__':
    main()

