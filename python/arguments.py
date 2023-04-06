"""Argument parsing"""

import sys
import xml.etree.ElementTree as ET
from argparse import ArgumentParser, FileType
from error import StatusCode, exit_program


class Arguments():
    """Argument parser"""
    __instance = None

    @staticmethod
    def get_instance():
        if Arguments.__instance is None:
            Arguments()
        return Arguments.__instance

    def __init__(self):
        self.source = None
        self.input = None

        if Arguments.__instance is not None:
            raise Exception("This class is a singleton, use get_instance()")
        else:
            Arguments.__instance = self

    def parse(self):
        """Parse arguments"""

        # Setup argument parser
        parser = ArgumentParser()
        parser.add_argument("-s", "--source", type=FileType("r"),
                            help="input file with XML representation of source code")
        parser.add_argument("-i", "--input", type=FileType("r"),
                            help=("file with inputs for the actual"
                                  "interpretation of the specified source code"))
        args = parser.parse_args()

        # Source or input has to be specified
        if (args.source is None and args.input is None):
            exit_program(StatusCode.MISSING_PARAM,
                         "Missing source or input file")
        # Replace second file with stdin if one of them is not specified
        if args.source is None:
            args.source = sys.stdin
        if args.input is None:
            args.input = sys.stdin

        try:
            xml = args.source.read()
        except:
            exit_program(StatusCode.INPUT_ERROR, "Input error")

        try:
            parsed = ET.fromstring(xml)
        except:
            exit_program(StatusCode.MALLFORMED, "XML error")

        self.source = parsed
        self.input = args.input
