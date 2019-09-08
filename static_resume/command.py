import argparse
import os

import static_resume
from static_resume import generator


def is_file(fname):
    if not os.path.exists(fname):
        raise argparse.ArgumentTypeError('{} is not a file'.format(fname))

    return fname


def main():
    # arguments parser
    parser = argparse.ArgumentParser(description=static_resume.__doc__)

    parser.add_argument('-v', '--version', action='version', version='%(prog)s v' + static_resume.__version__)
    parser.add_argument('config', action='store', type=is_file)

    args = parser.parse_args()

    # perform generation
    gen = generator.Generator()

    try:
        gen.generate(conf_file=args.config)
    except generator.GenError as e:
        print('! Error while generating: {}'.format(e))


if __name__ == '__main__':
    main()
