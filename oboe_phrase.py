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

t = 0; prev = None
for i,(name,beats) in enumerate(MELODY):
    dur = int(beats*PPQ)
    if name is None:
        t += dur; prev = None; continue
    p = midi(name)
    # legato join: tiny gap; last note of a phrase breathes
    end = t + dur - (10 if (i+1<len(MELODY) and MELODY[i+1][0]) else 40)
    # scoop into upward leaps / phrase starts (cents below target -> 0)
    scoop = prev is None or (prev is not None and p-prev >= 4)
    cc(t,11,70)
    bend(t, -45 if scoop else 0)
    add(t, bytes([0x90|CH, p, 78 if scoop else 70]))
    step = 12
    for tt in range(0, end-t, step):
        x = tt/(end-t)
        # expression swell: crescendo to 55% of note, then ease off
        e = 78 + 30*math.sin(math.pi*min(1,x/0.55)/2) if x<.55 else 108 - 22*((x-.55)/.45)
        cc(t+tt, 11, e)
        # vibrato: delayed onset (~1/3 beat), ramps in, ~5.5 Hz, +-18 cents
        depth = 0 if tt < 160 else min(1,(tt-160)/260)*18
        if beats < 1: depth = 0
        sc = -45*max(0, 1-tt/70) if scoop else 0
        vib = depth*math.sin(2*math.pi*tt/96)
        bend(t+tt, sc+vib)
    bend(end-2, 0)
    add(end, bytes([0x80|CH, p, 0]), 0)
    prev = p; t += dur
add(t+PPQ*2, b'\xff\x2f\x00', 2)

ev.sort(key=lambda e:(e[0],e[1]))
tr = b''; last = 0
for tk,_,d in ev:
    tr += vlq(tk-last)+d; last = tk
out = b'MThd'+struct.pack('>IHHH',6,0,1,PPQ)+b'MTrk'+struct.pack('>I',len(tr))+tr
open('oboe_liz_style.mid','wb').write(out)
print('bytes', len(out), 'beats', t/PPQ)
