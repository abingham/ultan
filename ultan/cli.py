import sys
from .get_names import get_names


def main(argv):
    for name in get_names(sys.argv[1]):
        print(name)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
