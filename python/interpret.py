"""Entry point"""

import sys
from runner import Runner
from arguments import Arguments

if __name__ == "__main__":
    # Parse arguments
    args = Arguments.get_instance()
    args.parse()

    # Run the program
    runner = Runner(args.source)
    with args.input as sys.stdin:
        runner.run()
