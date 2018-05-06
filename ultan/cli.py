import sys
from .name_index import NameIndex


def main(argv):
    index = NameIndex()
    for (name, module_name) in index.get_names(sys.argv[1]):
        print('{} [in {}]'.format(name, module_name))


if __name__ == '__main__':
    sys.exit(main(sys.argv))
