#####################################    CREDITS    #########################################################
#This is an UNATTACHED fork from the shbisson/OverPutney (https://github.com/shbisson/OverPutney) repository#
#modified with the amazing help of Scott Ladewig (https://github.com/ladewig)                               #
#############################################################################################################
import sys


def error(fmt, *args):
    sys.stdout.flush()
    sys.stderr.write((fmt % args) + '\n')
