"""
IPPcode23 interpreter

@Author: Josef Kuchař <xkucha28@stud.fit.vutbr.cz>
"""

import sys
from runner import Runner
from arguments import Arguments

if __name__ == "__main__":
    # Parse arguments
    args = Arguments()
    args.parse()

    # Run the program
    runner = Runner(args.source)
    with args.input as sys.stdin:
        runner.run()
