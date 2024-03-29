"""Argument parsing"""

import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, FileType
from error import StatusCode, exit_program


class Parser(ArgumentParser):
    """Argument parser with custom error handling"""

    def error(self, message):
        exit_program(StatusCode.MISSING_PARAM, message)


class Arguments():
    """Argument parser"""

    def __init__(self):
        self.source = None
        self.input = None

    def parse(self):
        """Parse arguments"""

        # Setup argument parser
        parser = Parser(conflict_handler="resolve")
        parser.add_argument("-s", "--source", type=FileType("r"),
                            help="input file with XML representation of source code")
        parser.add_argument("-i", "--input", type=FileType("r"),
                            help=("file with inputs for the actual"
                                  "interpretation of the specified source code"))
        parser.add_argument("-h", "--help", action="store_true", dest="help",
                            help="show this help message and exit")
        args = parser.parse_args()

        # Print help if requested and no other arguments are specified
        if args.help:
            if (args.source is None and args.input is None):
                parser.print_help()
                exit(StatusCode.OK.value)
            else:
                exit_program(StatusCode.MISSING_PARAM,
                             "Help requested with other arguments")

        # Source or input has to be specified
        if (args.source is None and args.input is None):
            exit_program(StatusCode.MISSING_PARAM,
                         "Missing source or input file")
        # Replace second file with stdin if one of them is not specified
        if args.source is None:
            args.source = sys.stdin
        if args.input is None:
            args.input = sys.stdin
        # Read source file
        try:
            xml = args.source.read()
        except OSError:
            exit_program(StatusCode.INPUT_ERROR, "Input error")
        # Parse XML
        try:
            parsed = ET.fromstring(xml)
        except ET.ParseError:
            exit_program(StatusCode.MALLFORMED, "XML error")

        self.source = parsed
        self.input = args.input
