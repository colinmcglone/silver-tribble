import sys, os
INTERP = os.path.join(os.environ['HOME'], 'colinmcglone.ca', 'bin', 'python')
if sys.executable != INTERP:
	os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())

sys.path.append('photos')
from photos import app as application