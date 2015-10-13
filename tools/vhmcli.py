
import sys

from vhmlib.config import Config
from vhmlib.manager import manager


class Api:

    def __init__(self):
        self.manage = manager()

    def list(self):
        pass


def main(*argv):
    api = Api()

    parser = OptionParser()
    parser.add_option(
        "-l",
        "--list",
        dest="list",
        help="Print state of all apps",
        action="store_true")

    (options, args) = parser.parse_args()

    if options.start:
        api.start(int(options.start))
    elif options.list:
        api.list()

    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv[1:])
