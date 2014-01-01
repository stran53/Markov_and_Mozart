from __future__ import division
from music21 import *
from scipy import stats
import numpy as np
import pprint

def pairwise2(iterable):
  return zip(iterable, iterable[1:]) + [(iterable[-1], note.Rest())]

if __name__ == '__main__':

	sc = scale.MajorScale('c')

	# C, D, E, F, G, A, B, rest 
	Matrix = [[0 for x in xrange(8)] for x in xrange(8)]

	mozart = converter.parseFile('1_1.krn')
	melody = mozart.parts[0]
	for measure in melody.getElementsByClass('Measure'):
		for pair in pairwise2(measure.notesAndRests):
			if pair[0].isChord:
			 	topNote = note.Note(pair[0].pitches[len(pair[0]) - 1])
				firstdegree = sc.getScaleDegreeFromPitch(topNote)
			elif pair[0].isRest:
				firstdegree = 8
			else:
				firstdegree = sc.getScaleDegreeFromPitch(pair[0])
			#print firstdegree

			if pair[1].isChord:
			 	topNote = note.Note(pair[1].pitches[len(pair[1]) - 1])
				seconddegree = sc.getScaleDegreeFromPitch(topNote)
			elif pair[1].isRest:
				seconddegree = 8
			else:
				seconddegree = sc.getScaleDegreeFromPitch(pair[1])
			#print seconddegree

			if firstdegree and seconddegree:
				Matrix[firstdegree - 1][seconddegree - 1] = Matrix[firstdegree - 1][seconddegree - 1] + 1
	#pprint.pprint(Matrix)

	#normalize
	for row in Matrix:
		total = sum(row)
		for i in xrange(len(row)):
   			row[i] = row[i]/float(total)
	#pprint.pprint(Matrix)


	xk = np.arange(8)

	custm = [0 for x in xrange(8)]
	for x in xrange(8):
		custm[x] = stats.rv_discrete(name='custm', values=(xk, Matrix[x]))

	compose = stream.Stream()
	n1 = note.Note('c5')
	compose.append(n1)

	for x in range(0, 100):
		if n1.isRest:
			index = 7
		else:
			index = sc.getScaleDegreeFromPitch(n1.pitch)
		R = custm[index - 1].rvs(size=1) + 1
		pitch = sc.pitchesFromScaleDegrees(R)[0]
		if R == 8:
			n2 = note.Rest(quarterLength = 1)
		else:
			n2 = note.Note(pitch, quarterLength = .5)
		compose.append(n2)
		n1 = n2

	compose.show('musicxml')
