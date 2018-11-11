import sys, httracklib

class CbClass:

    pass

callback = CbClass()
httracklib.httrack(callback, sys.argv)