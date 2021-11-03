#!/bin/python3

# sequencer.py: some fun with numpy arrays to create musical sequences
# usage: at the moment load everything then render a lilypond output 

import abjad as aj 
import numpy as np

# Broadcasting
a = np.array([1, 2, 3, 4])
print(a.ndim)

b = np.array([[2, 1, 2], [3, 2, 3], [4, 3, 4]])
print(b.ndim)

c = np.array([[[1, 2, 3], [2, 3, 4], [3, 4, 5]],
              [[1, 2, 4], [2, 3, 5], [3, 4, 5]]])
print(c.ndim)

# Some fancy business with slicing 


# Rhythmic structure
# The structure is based around a repeating pattern  
# rows represent cycle groupings
# an index value represents a meter signature 
# base units are quarter notes
basis = np.array([[7,2,7], [6,2,6], [5,2,5]])

# function to sum metric groupings
sum = lambda a, b, c: a + b + c

rowtotal = ([sum(x[0], x[1], x[2]) for x in basis])
phraselength = rowtotal[0] + rowtotal[1] + rowtotal[2]

# eigth notes form the basis of the sequence (x 2)
# the whole sequence is repeated twice       (x 2)
sequencer = np.array([aj.Note("e''8")] * (phraselength * 2) * 2)
assert len(sequencer) == 168, f"len not {len(sequencer)}"

def assert_phrase_length_is_168():
    try:
        row1 = [sequencer[:14], sequencer[14:18], sequencer[18:32]]
        assert len(row1[0]) == 14, f"len not {len(row1[0])}"
        assert len(row1[1]) == 4, f"len not{len(row1[1])}"
        assert len(row1[2]) == 14, f"len not {len(row1[2])}"

        lenrow1 = sum(len(row1[0]), len(row1[1]), len(row1[2])) 
        assert lenrow1 == 32, f"len not {lenrow1}"

        row2 = [sequencer[32:44], sequencer[44:48], sequencer[48:60]]
        assert len(row2[0] == 12), f"len not {len(row2[0])}"
        assert len(row2[1] == 4), f"len not {len(row2[1])}"
        assert len(row2[2] == 12), f"len not {len(row2[2])}"

        lenrow2 = sum(len(row2[0]), len(row2[1]), len(row2[2])) 
        assert lenrow2 == 28, f"len not {lenrow2}"

        row3 = [sequencer[60:70], sequencer[70:74], sequencer[74:84]]
        assert len(row3[0] == 10), f"len not {len(row3[0])}" 
        assert len(row3[1] == 4), f"len not {len(row3[1])}" 
        assert len(row3[2] == 10), f"len not {len(row3[2])}" 

        lenrow3 = sum(len(row3[0]), len(row3[1]), len(row3[2])) 
        assert lenrow3 == 24, f"len not {lenrow3}"

        seqlen = sum(lenrow1, lenrow2, lenrow3) * 2
        assert seqlen == 42 * 4, f"length is {seqlen}" 
    except AssertionError as error:
        print(error)

assert_phrase_length_is_168()


#
# Harmony
#
# spans are tuples that reference the ranges of the sequence that are formally
# related e.g.: they feature a harmonic repetition
# Each row references one family of relations
# integer values in the tuples can be used to reference the eigth note values
# in the sequence.

# Harmonies occur across spans of time. 
def getspans():
    initspans = np.array([[(1, 14), (32, 44), (60, 70)],
                      [(14, 18), (44, 48), (70, 74)],
                      [(18, 32), (48, 60), (74, 84)]])
    secondspans = initspans + 84 
    return np.concatenate((initspans, secondspans))

SPANS = getspans()

def makesliceargs(slargs):
    return slice(slargs)

# Takes a single note as an argument and places it into the span according
# to the slice 
def placenote(note, sequencer, indexes):
    for i in indexes:
        sequencer[i] = note

def placenotes(notes, seq, idxs):
    for (n, i) in zip(notes, idxs):
        placenote(n, seq, i)

# Given a span array and a tuple of slice arguments, 
# the function creates a list of indexes that can be used to access steps
def getselection(span, slargs):
    assert len(span) == 2, "Error: SPANS can only contain two indexes"
    assert (span[0] >= 0) and \
           (span[0] <= span[1]), "Error: span must be positive"
    lst = []
    for i in range(span[0], span[1]):
        lst.append(i)
    try:
        islice = slice(slargs[0], slargs[1], slargs[2])
        indexes = lst[islice]
        return indexes
    except Exception as error:
        print(error)

# put bass voice on the offbeats the first time the harmony turns up in the sequence
OFFBEATSLICE = (1, None, 2)
AJ_OFFBEATINDEXES = (getselection(SPANS[0][0], OFFBEATSLICE), 
                     getselection(SPANS[1][0], OFFBEATSLICE),
                     getselection(SPANS[2][0], OFFBEATSLICE),
                     getselection(SPANS[3][0], OFFBEATSLICE),
                     getselection(SPANS[4][0], OFFBEATSLICE),
                     getselection(SPANS[5][0], OFFBEATSLICE))
FJ_OFFBEATINDEXES = (getselection(SPANS[0][1], OFFBEATSLICE),
                     getselection(SPANS[1][1], OFFBEATSLICE),
                     getselection(SPANS[2][1], OFFBEATSLICE),
                     getselection(SPANS[3][1], OFFBEATSLICE),
                     getselection(SPANS[4][1], OFFBEATSLICE),
                     getselection(SPANS[5][1], OFFBEATSLICE))
CJ_OFFBEATINDEXES = (getselection(SPANS[0][2], OFFBEATSLICE),
                     getselection(SPANS[1][2], OFFBEATSLICE),
                     getselection(SPANS[2][2], OFFBEATSLICE),
                     getselection(SPANS[3][2], OFFBEATSLICE),
                     getselection(SPANS[4][2], OFFBEATSLICE),
                     getselection(SPANS[5][2], OFFBEATSLICE))

# containers default to quarter notes
# use SATB conventions to refer to the specific tones




# Harmonies 
harmonies = 
AMAJ7_CS = aj.Container("cs''8 e''8 gs''8  a''8")
FMAJ7_C = aj.Container("c''8 e''8 f''8 a''8")
CMAJ7 = aj.Container("c''8 e''8 g''8 b''8") 

from enum import Enum
class Mode(Enum):
    AIONIAN_2ND_OCTAVE     = 0
    CIONIAN_2ND_OCTAVE     = 1
    CMIXOLYDIAN_2ND_OCTAVE = 2 

class Chord(Enum):
    AMAJ7_CS_2ND_OCTAVE = 0
    CMAJ7_2ND_OCTAVE   = 1
    FMAJ7_C_2ND_OCTAVE = 2

# Modes
pitch_sets = {
        Mode.AIONIAN_2ND_OCTAVE     : aj.PitchSet("a'' b'' cs'' ds'' e'' fs'' gs'' a'' b''"),
        Mode.CIONIAN_2ND_OCTAVE     : aj.PitchSet("c'' d'' e'' f'' g'' a'' gs'' a'' b''"),
        Mode.CMIXOLYDIAN_2ND_OCTAVE : aj.PitchSet("c'' d'' e'' f'' g'' a'' bf'' c'''"),
        Chord.AMAJ7_CS_2ND_OCTAVE   : aj.Container("cs''8 e''8 gs''8  a''8"),
        Chord.CMAJ7_2ND_OCTAVE      : aj.Container("c''8 e''8 g''8 b''8"), 
        Chord.FMAJ7_C_2ND_OCTAVE    : aj.Container("c''8 e''8 f''8 a''8"),
        }



from collections import namedtuple

Suspension = namedtuple('Suspension', ['didx', 'uidx', 'pitchset'])

def getnumberedpitches(harmony):
    numberedpitches = []
    for h in harmony:
        numberedpitches.append(aj.NamedPitch(h).number)
    numberedpitches.sort()
    return numberedpitches

def makepitchset(candidates):
    namedpitches = []
    for p in candidates:
        namedpitches.append(aj.NamedPitch(p))
    return aj.PitchSet(namedpitches)

def getmodalintersection(mode, suscandidates):
    assert isinstance(suscandidates, aj.PitchSet), "Error: not a pitchset"
    try:
        intersection = mode.intersection(suscandidates) 
        return intersection
    except Exception as error:
        print("Error while creating modal intersection: \n", error)

def getsuspensions(downbeatharmony, upbeatharmony, mode):
    # takes two harmonies and returns all possible sus / res paths
    # mode is a set of the tones that can be walked to from a suspended tone 
    dbnumpitches = getnumberedpitches(downbeatharmony)
    ubnumpitches = getnumberedpitches(upbeatharmony)
    suspensions = []
    suspensions = []
    assert isinstance(mode, aj.PitchSet), "Error: mode not a pitchset"
    try:
        for didx, d in enumerate(dbnumpitches):
            suscandidates = []
            for uidx, u in enumerate(ubnumpitches):
                if (d == u):
                    break
                elif (d > u):
                    suscandidates.append(d)
                    d -= 1
                elif (d < u):
                    break
            suscan_pitchset = makepitchset(suscandidates)
            modal_intersection = getmodalintersection(mode, suscan_pitchset)
            suspensions.append(Suspension(didx, uidx, modal_intersection))
        return suspensions
    except Exception as error:
        print("Uknown state: \n", error)


SUSPENSIONS = {
        "ATOF" : getsuspensions(pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE],
                                pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE],
                                pitch_sets[Mode.CMIXOLYDIAN_2ND_OCTAVE]),
        "FTOC" : getsuspensions(pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE],
                                pitch_sets[Chord.CMAJ7_2ND_OCTAVE],
                                pitch_sets[Mode.CMIXOLYDIAN_2ND_OCTAVE]),
        "CTOA" : getsuspensions(pitch_sets[Chord.CMAJ7_2ND_OCTAVE],
                                pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE],
                                pitch_sets[Mode.AIONIAN_2ND_OCTAVE])
        }

notes = np.array([
    [pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE][0], pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE][0], pitch_sets[Chord.CMAJ7_2ND_OCTAVE][0]], 
    [pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE][1], pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE][1], pitch_sets[Chord.CMAJ7_2ND_OCTAVE][1]],
    [pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE][2], pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE][2], pitch_sets[Chord.CMAJ7_2ND_OCTAVE][2]],
    [pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE][3], pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE][3], pitch_sets[Chord.CMAJ7_2ND_OCTAVE][3]],
    [pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE][0], pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE][0], pitch_sets[Chord.CMAJ7_2ND_OCTAVE][0]], 
    [pitch_sets[Chord.AMAJ7_CS_2ND_OCTAVE][0], pitch_sets[Chord.FMAJ7_C_2ND_OCTAVE][0], pitch_sets[Chord.CMAJ7_2ND_OCTAVE][0]], 
                  ])



# suspensions / resolutions (9 -> 8, 7 -> 6, 4 -> 3)
# amaj7_cs[0] -> (fmaj7_cs[0] or cmaj7[0]) [ ^5 -> 5, b2 -> 1 ]
# amaj7

# Locates the harmonies within the rhythmic structure
NOTELOCS = { 
        "AJS_OFFBEATS" : ((notes[0][0], notes[1][0], notes[2][0],
                           notes[3][0], notes[4][0], notes[5][0]), AJ_OFFBEATINDEXES),
        "FJS_OFFBEATS" : ((notes[0][1], notes[1][1], notes[2][1],
                           notes[3][1], notes[4][1], notes[5][1]), FJ_OFFBEATINDEXES),
        "CJS_OFFBEATS" : ((notes[0][2], notes[1][2], notes[2][2],
                           notes[3][2], notes[4][2], notes[5][2]), CJ_OFFBEATINDEXES),
        }

placenotes(NOTELOCS["AJS_OFFBEATS"][0], sequencer, NOTELOCS["AJS_OFFBEATS"][1])
placenotes(NOTELOCS["FJS_OFFBEATS"][0], sequencer, NOTELOCS["FJS_OFFBEATS"][1])
placenotes(NOTELOCS["CJS_OFFBEATS"][0], sequencer, NOTELOCS["CJS_OFFBEATS"][1])

# Construct the notation 
fstring = ""
for s in sequencer:
    fstring += f"{s} "

voice = aj.Voice(fstring, "mysequence")
staff = aj.Staff([voice])

aj.show(staff)

