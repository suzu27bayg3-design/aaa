"""Oboe solo phrase in the lyrical style of 'Liz and the Blue Bird' -> MIDI with vibrato/rubato.
Dependency-free SMF writer. Run: python3 oboe_phrase.py"""
import math, struct

PPQ = 480
N = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def midi(n):                       # 'E5' -> 76
    return 12*(int(n[-1])+1) + N[n[0]]

# (note|None, beats). A minor, 4/4, three 4-bar phrases (question / answer / release).
MELODY = [
 ('E5',2),('A5',1.5),('G5',.5),   ('F5',1),('E5',1),('D5',2),
 ('C5',1.5),('D5',.5),('E5',1),('A4',1),   ('B4',3),(None,1),
 ('E5',1),('G5',1),('A5',1.5),('B5',.5),   ('C6',2),('B5',1),('A5',1),
 ('G5',1.5),('F5',.5),('E5',1),('D5',1),   ('E5',3),(None,1),
 ('A5',1),('G5',.5),('F5',.5),('E5',1),('D5',1),  ('C5',1.5),('B4',.5),('A4',2),
 ('C5',1),('E5',1),('D5',.5),('C5',.5),('B4',1),  ('A4',5),
]
BASE_BPM = 66
# phrase-ending ritardando: (start beat, bpm) -- bars 4, 8, 11-12
TEMPO = [(0,66),(14,60),(15,54),(16,66),(30,60),(31,54),(32,66),(42,58),(44,52),(46,46)]

def vlq(n):
    b=[n&0x7f]; n>>=7
    while n: b.append((n&0x7f)|0x80); n>>=7
    return bytes(reversed(b))

ev = []                              # (tick, order, bytes)
def add(t, data, o=1): ev.append((int(t), o, data))
CH = 0
def cc(t,c,v): add(t, bytes([0xB0|CH, c, max(0,min(127,int(v)))]))
def bend(t, cents):
    v = max(0, min(16383, 8192 + int(cents/200*8192)))   # +-2 semitones range
    add(t, bytes([0xE0|CH, v&0x7f, v>>7]))

add(0, b'\xff\x58\x04\x04\x02\x18\x08', 0)
for beat,bpm in TEMPO:
    add(beat*PPQ, b'\xff\x51\x03'+int(60_000_000/bpm).to_bytes(3,'big'), 0)
add(0, bytes([0xC0|CH, 68]), 0)                               # GM Oboe
for c,v in ((101,0),(100,0),(6,2),(38,0)): cc(0,c,v)         # pitch-bend range 2 st
cc(0,91,75); cc(0,7,110)                                      # reverb, volume

# --- slur groups: a group = notes joined legato (broken by rests and at the mid-phrase marks) ---
SLUR_BREAK_AFTER = {5, 18, 32}
groups = []; cur = []; t = 0
for i,(name,beats) in enumerate(MELODY):
    dur = int(beats*PPQ)
    if name is None:
        if cur: groups.append(cur); cur = []
    else:
        cur.append((i, midi(name), t, dur))
        if i in SLUR_BREAK_AFTER: groups.append(cur); cur = []
    t += dur
if cur: groups.append(cur)

OVER = 36      # ticks the next note starts before the previous one ends (legato overlap)
for g in groups:
    g0 = g[0][2]; gend = g[-1][2] + g[-1][3] - 40   # last note of a group breathes out
    glen = gend - g0
    # one continuous expression + pitch-bend curve for the whole slur (no per-note dips)
    for tt in range(0, glen, 12):
        x = tt/glen
        e = 76 + 32*math.sin(math.pi*x/0.6/2) if x < .6 else 108 - 30*((x-.6)/.4)
        cc(g0+tt, 11, e)
        scoop = -45*max(0, 1-tt/70)                     # scoop only into the slur's first note
        depth = 0 if tt < 160 else min(1, (tt-160)/260)*17
        vib = depth*math.sin(2*math.pi*tt/96)           # phase continues across note changes
        bend(g0+tt, scoop+vib)
    bend(gend-2, 0)
    for k,(i,p,ts,d) in enumerate(g):
        last = k == len(g)-1
        te = gend if last else ts + d + OVER              # overlap into the next note
        add(ts, bytes([0x90|CH, p, 82 if k == 0 else 52]))  # soft re-attack inside a slur
        add(te, bytes([0x80|CH, p, 0]), 0)
t = sum(int(b*PPQ) for _,b in MELODY)
add(t+PPQ*2, b'\xff\x2f\x00', 2)

ev.sort(key=lambda e:(e[0],e[1]))
tr = b''; last = 0
for tk,_,d in ev:
    tr += vlq(tk-last)+d; last = tk
out = b'MThd'+struct.pack('>IHHH',6,0,1,PPQ)+b'MTrk'+struct.pack('>I',len(tr))+tr
open('oboe_liz_style.mid','wb').write(out)
print('bytes', len(out), 'beats', t/PPQ)
