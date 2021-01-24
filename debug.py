
def debug_candidate_parser():
    """Calls a web address and prints out the result"""
    from request_searcher import parser
    address = 'http://www.stalekom.ru'
    print(parser.parse(address))


def main():
    """
    Insert a funtion to debug.
    The function must be pre-configured within itself.
    """
    debug_candidate_parser()

if __name__ == '__main__':
    main()

