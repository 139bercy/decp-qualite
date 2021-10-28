import argparse

def get_parser():
    """
    Creates a new argument parser.
    """
    parser = argparse.ArgumentParser()
    return parser

def main(args=None):
    """ Main entry point.
    
    Args:
        args : list of arguments as if they were input in the command line.
    """
    parser = get_parser()
    args = parser.parse_args(args)

if __name__ == '__main__':
    main()