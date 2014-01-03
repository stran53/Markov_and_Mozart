from __future__ import division
from music21 import *
from scipy import stats
import numpy as np

def pairwise2(iterable):
  return zip(iterable, iterable[1:]) + [(iterable[-1], iterable[0])]

if __name__ == '__main__':

	sc = scale.MajorScale('c')

	# C, D, E, F, G, A, B, rest 
	PitchMatrix = [[.0000001 for x in xrange(8)] for x in xrange(8)]

	# quarter lenghts
	# 0, .25, .5, .75, 1, 1.25, 1.5, 1.75, 2, 2.25, 2.5, 2.75, 3, 3.25, 3.5, 3.75, 4
	DurationMatrix = [[.0000001 for x in xrange(17)] for x in xrange(17)]

	mozart = converter.parseFile('C:\Users\Steven\Documents\Twinkle.xml')
	melody = mozart[2].flat
	#melody = mozart.parts[0].flat
	for pair in pairwise2(melody.notesAndRests):
		firstDuration = int(pair[0].quarterLength * 4)
		if pair[0].isChord:
			topNote = note.Note(pair[0].pitches[len(pair[0]) - 1])
			firstdegree = sc.getScaleDegreeFromPitch(topNote)
		elif pair[0].isRest:
			firstdegree = 8
		else:
			firstdegree = sc.getScaleDegreeFromPitch(pair[0])

		secondDuration = int(pair[1].quarterLength * 4)
		if pair[1].isChord:
			topNote = note.Note(pair[1].pitches[len(pair[1]) - 1])
			seconddegree = sc.getScaleDegreeFromPitch(topNote)
		elif pair[1].isRest:
			seconddegree = 8
		else:
			seconddegree = sc.getScaleDegreeFromPitch(pair[1])

		if firstdegree and seconddegree:
			PitchMatrix[firstdegree - 1][seconddegree - 1] = PitchMatrix[firstdegree - 1][seconddegree - 1] + 1
			DurationMatrix[firstDuration][secondDuration] = DurationMatrix[firstDuration][secondDuration] + 1

	#normalize
	for row in PitchMatrix:
		total = sum(row)
		for i in xrange(len(row)):
   			row[i] = row[i]/float(total)
	for row in DurationMatrix:
		total2 = sum(row)
		for i in xrange(len(row)):
			row[i] = row[i]/float(total2)

	xk = np.arange(8)
	xk2 = np.arange(17)

	distPitch = [0 for x in xrange(8)]
	for x in xrange(8):
		distPitch[x] = stats.rv_discrete(name='distPitch', values=(xk, PitchMatrix[x]))

	distDuration = [0 for x in xrange(17)]
	for x in xrange(17):
		distDuration[x] = stats.rv_discrete(name='distDuration', values=(xk2, DurationMatrix[x]))

	compose = stream.Stream()
	n1 = note.Note('c4')
	compose.append(n1)

	for x in range(0, 40):
		indexDuration = int(n1.quarterLength * 4)
		if n1.isRest:
			index = 7
		else:
			index = sc.getScaleDegreeFromPitch(n1.pitch)
		R = distPitch[index - 1].rvs(size=1) + 1
		R2 = int(distDuration[indexDuration].rvs(size=1))
		pitch = sc.pitchesFromScaleDegrees(R)[0]
		if R == 8:
			n2 = note.Rest(quarterLength = R2/4.0)
		else:
			n2 = note.Note(pitch, quarterLength = (R2/4.0))
		compose.append(n2)
		n1 = n2

	compose.show('musicxml')
