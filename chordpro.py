#! /usr/bin/env python
'''
Convert a text file from chords over the lyric line
to brackedted chords within the lyric line.
The byte location is maintained, so minimal preprocessing
of the original file may be required to move the chords
in the original file where you want them in the output.
Ultimate Guitar has pretty good chord placements but 
I find the chord-within-line more compact, requiring
less scrolling on the part of the performer.

Example python chordpro.py song.txt

A companion shell script, convert.sh converts all the 
*.tex files in the orig directory to a converted directory.
As I convert more files I sometime discover "gotchas", so 
this code may have to be revisited.
'''
import sys
import os
from operator import itemgetter
import re as re

def buildChords():
    '''
    return an enhanced list of possible chords 
    suffix are maj', sharps and flats
    mod are m,7,2,sus
    '''
    chords = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    suffix = ['','#', 'maj', 'b', 'sus']
    mod = ['', 'm', '7', '2', '4', '6']

    # Important to add to a new variable name
    # to avoid an infinite loop.
    chord_plus = []
    for c in chords:
        for s in suffix: # The '' suffix maintains the one sylable chords
            chord_plus.append(c+s)
    #print(chord_plus)

    chord_plus_plus = []
    for c in chord_plus:
        for m in mod:
            chord_plus_plus.append(c+m)

    return chord_plus_plus

def isChordLine(line,chords):
    '''
    returns True if a line consists of only chords.
    otherwise False
    '''
    ChordLine = True
    data = line.split()
    for str in data:
        if str not in chords:
            # Check to see that valid chords are on either
            # side of the '/'. This is a more general solution
            # than the quick fix of just adding G6/D to chords.
            if '/' in str:
                # looking for pattern such as G6/D
                srch = str.split('/')
                for t in srch:
                    if t not in chords:
                        # no chord with this '/'
                        return False
            else:
                # A non-chord was found so classify line as "non-chord"
                # Most likely it's just a lyric line.
                # Occasionally an unexpected chord shows up like
                # that G6/D from Spanish Pipedream. James Taylor
                # uses a lot of those modified chord patterns...
                # so do check the output. Adjust this code as needed.
                return False
    #print(data)
    
    return ChordLine

def printChords(a,line):
    '''
    Occasionally, a chord line may be followed by another chord line
    or by a blank line. This is meant to convey an intro, outro, or
    instrumental interlude. In those cases, this function will simply 
    print out the chords with square brackets around them. 
    '''
    line = ''
    for item in a:
        c = item[0]
        loc = item[1]
        whitespace = ''
        if loc > len(line):
            whitespace = (loc-len(line))*' '
        l = line.rstrip()+whitespace
        r = '' # put newline back on the line
        line = l+'['+c+']'+r  # insert 

    print(line)
    a = []
    return

def main():

    '''
    read in the text file listed on the command line and convert
    the format from chord-over-lyric to chord-inside-lyric.
    '''
    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
  
    a = [] # list to contain tuples of byte location and chords
    chords = buildChords()
    #print(chords)
    with open(filepath) as fp:
        for line in fp:
            #print('raw: ', line.rstrip(), len(line))
            chordLine = isChordLine(line,chords)
            if line.rstrip().isspace() or len(line.rstrip()) < 1:
                if a != []:
                    printChords(a,line) 
                else:
                    print()
                a = []
                continue
            if isChordLine(line,chords):
                #print(line.rstrip(), ' is chordline: ', a)
                if a != []: # handle successive chord lines 
                    printChords(a,line)
                    a = []

                key = r'\S+' # any non whitespace
                iter = re.finditer(key, line)
                res = line.split()
                indices = [m.start(0) for m in iter]
                for i,loc in enumerate(indices): # loc is the byte location
                    a.append((res[i],loc))
                #print('chords found = ',a)
            else: # insert any saved chords into lyric line
                #print(line.rstrip(), ' is not chordline: ', a)
                # add chordsfrom the end to front so locations make sense
                a.sort(key=itemgetter(1),reverse=True) # reverse sort by loc
                #print(a)
                for item in a:
                    c = item[0]
                    loc = item[1]
                    if loc < len(line): 
                        # split the line into left and right halves
                        l,r = line[:loc],line[loc:] 
                    else: # handle chords extending beyond end of lyric line
                        #print('len(line) = ', len(line), 'item = ', item)
                        whitespace = (loc-len(line))*' '
                        l = line.rstrip()+whitespace
                        r = '\n' # put newline back on the line

                    line = l+'['+c+']'+r  # insert a chord into the lyric line                   
                print(line,end='')
                a = []  # done with that batch of chords 


if __name__ == '__main__':
    main()

