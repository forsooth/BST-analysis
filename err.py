import sys


red = '\033[38;5;203m'
yellow = '\033[38;5;222m'
blue = '\033[38;5;12m'
nc = '\033[00m'
nl = '\n'


def err(msg=""):
        sys.stderr.write(red + str(msg) + nc + nl)
        sys.exit(1)


def warn(msg=""):
        sys.stderr.write(yellow + str(msg) + nc + nl)


def log(msg=""):
        sys.stderr.write(blue + str(msg) + nc + nl)
