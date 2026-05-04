import sys

from cli.base import ProcessCMD


def main():
    args = sys.argv[1:]
    cli = ProcessCMD()
    cli.run(args)


if __name__ == "__main__":
    main()
