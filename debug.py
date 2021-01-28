
def debug_candidate_parser():
    """Calls a web address and prints out the result"""
    from request_searcher import parser
    address = 'http://www.stalekom.ru'
    print(parser.parse(address))


def debug_request_definer():
    from request_searcher import request_definer

    print(request_definer.data_object(req_list=
                                      [["Сталь","Медь", "Алюминий"],
                                       'Насос',
                                       ["Вода", "Масло", "Пропан"],
                                       ["Крым", "Норильск"]]
                                      )
          )


def main():
    """
    Insert a funtion to debug.
    The function must be pre-configured within itself.
    """
    #debug_candidate_parser()
    debug_request_definer()

if __name__ == '__main__':
    main()

