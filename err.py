import sys
import colors

nl = '\n'


def err(msg=""):
        sys.stderr.write(colors.red + str(msg) + colors.nc + nl)
        sys.exit(1)


def warn(msg=""):
        pass
        #sys.stderr.write(colors.yellow + str(msg) + colors.nc + nl)


def log(msg=""):
        pass
        #sys.stderr.write(colors.blue + str(msg) + colors.nc + nl)
