import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sfx'))
from music import Song
from mix import Desk
s = Song('funk', key='E', minor=True, seed=42).form([('intro', 1), ('build', 1), ('drop', 4), ('break', 1)])
st = s.render(); d = Desk(15.2); d.add_stems(st); d.duck('music', s.kick_times, .25, .02, .1); d.room('music', 'hall', .12); print(d.master(sys.argv[1]))
