import sys
import colors

nl = '\n'


def err(msg=""):
        sys.stderr.write(colors.t_red + str(msg) + colors.t_nc + nl)
        sys.exit(1)


def warn(msg=""):
        sys.stderr.write(colors.t_yellow + str(msg) + colors.t_nc + nl)


def log(msg=""):
        sys.stderr.write(colors.t_blue + str(msg) + colors.t_nc + nl)
