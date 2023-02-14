"""Entry point"""

from runner import Runner
from arguments import Arguments

if __name__ == "__main__":
    args = Arguments.get_instance()
    args.parse()
    runner = Runner(args.source)
    runner.run()
