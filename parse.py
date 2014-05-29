#Author: Erik Kierstead
#Class:  Computation of Harmony and Form in Rock and Pop Music
#
#Purpose:  To read in the annotation file using Sonic Analyzer and the
#Chordino Vamp Plugin with the Chord Estimation Algorithm with other
#annotation files (initially, mirex) to compare chord progression results.

import sys
import re

def ChordinoFileInput(filename):
	
	chordlist = []
	
	#Regex Strings:
	regex_newline = re.compile("\n|\r")
	regex_chordtones = re.compile("maj|6|7") #"[maj]|6|7"
	
	#Tries to Open File Else Exits:
	try:
		openFile = open(filename, 'r')
	
	except:
		print
		print("Cannot Open File " + filename)
		print
		print("Quitting..")
		sys.exit(1)
	
	#Reads File By Lines, Removes New Line Chars, Splits by Tab,
	#Rounds Time, Simplifies Chord, Pushes Results to Chordlist:
	for line in openFile.readlines():
		
		split_line = regex_newline.sub("", line).split("\t")
		split_line[0] = round(float(split_line[0]), 2)
		split_line[1] = regex_chordtones.sub("", split_line[1])

		chordlist.append(split_line)
		
    #for chord in chordlist: print(chord)

	return chordlist

def MirexFileInput(filename):

    #Gives Bogus Initial Value (to prevent out of bounds on init check):	
	chordlist = [[0,0,"init"]]
	chordlist_index = 1
	
	#Regex Strings:
	regex_newline = re.compile("\n|\r")
	regex_chordtones = re.compile("maj|[:in]|6|7|sus4") #"[maj]|6|7"
	regex_spacing = re.compile("\w+|\t")

	#Tries to Open File Else Exits:
	try:
		openFile = open(filename, 'r')
	
	except:
		print
		print("Cannot Open File " + filename)
		print
		print("Quitting..")
		sys.exit(1)
	
    #Reads File By Lines, Removes New Line Chars, Splits by Tab/WhiteSP,
	#Rounds Start Time, Throws Away End Time, Simplifies Chord, 
	#Throws Away if Chord Already Exists, Iterates chordlist index:
	for line in openFile.readlines():
	
		split_line = re.split(" +|\t", regex_newline.sub("", line))
		if(len(split_line) > 1 ):
	
			split_line[0] = round(float(split_line[0]), 2)
			split_line[2] = regex_chordtones.sub("", split_line[2])
			
			if(chordlist[chordlist_index - 1][1] != split_line[2]):
				chordlist.append([split_line[0], split_line[2]])
				chordlist_index += 1
			
	#for chord in chordlist: print(chord)
	chordlist.pop(0)
		
	return chordlist

def MissedChord(miss, i, j):
	
	miss += 1
	i += 1
	j += 1
	
	return miss, i, j
	
def MatchedChord(match, i, j):
	
	match += 1
	i += 1
	j += 1
	
	return match, i, j


#Proof of Concept Comparison, Needs Rewrite:
def Compare(chordlist_1, chordlist_2):
	
	#Acceptable Difference in Seconds Between Chords:
	dx = 1
	
	#Holds Score:
	failed_matches = []
	miss = 0
	match = 0
	
	#i and j are list1 and 2's respective index values:
	i= 0
	j = 0
	
	#Length of Each Chordlist:
	chd1_length = len(chordlist_1)
	chd2_length = len(chordlist_2)
	
	exit = False
	
	#Algorithm Description:
	#1)  Computes the difference between two chords
	#2)  If the time is too great, then it looks at +/- sign to figure
	#    out which list will require examining the next element.
	#    (This accounts for time-alignment discrepencies)
	#3)  If the time is approximately synched, then compares chord type.
	#    If chords match, then increase match count!
	#    If chords do not match, increase miss count!
	#4)  When indexes match / exceed the length of one of the chord lists
	#    then compute the chords left (if any), add those to the missed
	#    chord score, then exit == True calls it a day.
	
	while(exit == False):
	
	    #Computes Time Difference Between Chords:	
		diff = chordlist_1[i][0] - chordlist_2[j][0]
		
		#print(str(chordlist_1[i][0]) + " " + chordlist_1[i][1]  + " vs " + str(chordlist_2[j][0]) + " " + chordlist_2[j][1])
		#print("i: " + str(i) + " j: " + str(j))
		
		if(abs(diff) > dx):
			failed_matches.append([chordlist_1[i], chordlist_2[j]])
			if(diff > 0): j += 1
			else: i += 1
			miss += 1
		
		elif("/" in chordlist_1[i][1]):
			chord1, chord2 = chordlist_1[i][1].split("/")
			
			if(chord1 in chordlist_2[j][1] or chord2 in chordlist_2[j][1]):
			    match, i, j = MatchedChord(match, i, j)
			
			else:
				failed_matches.append([chordlist_1[i], chordlist_2[j]])
				miss, i, j = MissedChord(miss, i, j)	
		
		elif(chordlist_1[i][1] == chordlist_2[j][1]):
			match, i, j = MatchedChord(match, i, j)		
			
		else:
			failed_matches.append([chordlist_1[i], chordlist_2[j]])
			miss, i, j = MissedChord(miss, i, j)
		
		if(chd1_length <= i and chd2_length <= j): exit = True
		
		elif(chd1_length <= i):
			miss += chd2_length - j
			for k in range(j, chd2_length): failed_matches.append(["List 1 Ended", "N"], chordlist_2[k])
			exit = True
			
		elif(chd2_length <= j):
			miss += chd1_length - i
			for k in range(i, chd1_length): failed_matches.append([chordlist_1[k],["List 2 Ended", "N"]])
			exit = True
		
	#Outputs Mismatched Chords:
	print("\nMismatched Chords: " + str(len(failed_matches)))
	for chord in failed_matches: print(chord)
	
	#Computes Match / Miss Score:
	print("\nScore:")
	print("Matches: " + str(match))
	print("Misses: " + str(miss))
	print
	print("Match/Miss Ratio: " + str(round(float(match)/float(match+miss),2)))
	print
		
	return

#Error Message if Wrong Command Line Arguments Used:
def usage():
	print
	print("Proper Use:")
	print("python parser.py chordino_file.txt mirex_file.txt")
	print
	print("Quitting..")
	print
	sys.exit(1)

#Main Script:

if(len(sys.argv) != 3): usage()

#Gets Chord Names from Command Line Arguments:
chordino_filename = sys.argv[1]
mirex_filename = sys.argv[2]

#Parses File into Python List (where each element is a list of time/chord):
chordino_chordlist = ChordinoFileInput(chordino_filename)
#mirex_chordlist = ChordinoFileInput(mirex_filename)
mirex_chordlist = MirexFileInput(mirex_filename)


#Compares and Computes Score:
Compare(chordino_chordlist, mirex_chordlist)
