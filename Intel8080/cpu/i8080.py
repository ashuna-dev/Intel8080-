from argparse import ArgumentParser
import logging
from Kernel import IntelKernel


def main():
    arg_parser = ArgumentParser()
    arg_parser.add_argument('--filename', help='ROM file')
    arg_parser.add_argument('--test', nargs='?', default=True, help='Run test suite')
    args = arg_parser.parse_args()

    filename = args.filename

    logging.basicConfig(level=logging.INFO, filename='i8080.py.log', filemode='w')

    if filename:
        system = IntelKernel(filename)
        system.boot()
    elif args.test:
        system = IntelKernel(None)
        system.run_tests()


if __name__ == '__main__':
    main()