"""Entry point"""

from argparse import ArgumentParser, FileType
import sys
import xml.etree.ElementTree as ET
from error import StatusCode, exit_program
from runner import Runner
from arguments import Arguments

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-s", "--source", type=FileType("r"),
                        help="input file with XML representation of source code")
    parser.add_argument("-i", "--input", type=FileType("r"),
                        help=("file with inputs for the actual"
                              "interpretation of the specified source code"))
    args = parser.parse_args()

    # Source or input has to be specified
    if (args.source is None and args.input is None):
        exit_program(StatusCode.MISSING_PARAM, "Missing source or input file")
    # Replace second file with stdin if one of them is not specified
    if args.source is None:
        args.source = sys.stdin
    if args.input is None:
        args.input = sys.stdin

    try:
        xml = args.source.read()
    except:
        pass

    try:
        parsed = ET.fromstring(xml)
    except:
        pass

    args1 = Arguments()
    args1.parser = "HAha"
    args2 = Arguments()
    print(args2.parser)

    runner = Runner(parsed)
    runner.run()
