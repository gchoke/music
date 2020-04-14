#! /usr/bin/env python
import sys
import os
from operator import itemgetter
import re as re


def buildChords():
    '''
    return an enhanced list of possible chords 
    suffix are maj, sharps and flats
    mod are m,7,2,sus
    '''
    chords = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    suffix = ['','#', 'maj', 'b']
    mod = ['', 'm', 'sus', '7', '2']

    # important to add to a new variable
    # to avoid an infinite loop.
    chord_plus = []
    for c in chords:
        for s in suffix:
            chord_plus.append(c+s)
    #print(chord_plus)

    chord_plus_plus = []
    for c in chord_plus:
        for m in mod:
            chord_plus_plus.append(c+m)
    #print(chord_plus_plus)
    '''
    chord_lower_case = []
    for c in chord_plus_plus:
        chord_lower_case.append(c.lower())
    print(chord_lower_case)
    '''
    return chord_plus_plus

def isChordLine(line,chords):
    '''
    returns True if and only if a line consists of chords.
    otherwise False
    '''
    ChordLine = True
    data = line.split()
    for str in data:
        if str not in chords:
            ChordLine = False
            break
    #print(data)
    '''
    for c in chords:
        key = r"\b%s\b"%(c)
        iter = re.finditer(key, line, re.IGNORECASE)
        indices = [m.start(0) for m in iter]
        if indices != None:
            ChordLine = False
            print('key = %s indices = '%(key), indices)
            break
    '''
    return ChordLine

def main():

    filepath = sys.argv[1]

    if not os.path.isfile(filepath):
        print("File path {} does not exist. Exiting...".format(filepath))
        sys.exit()
  
    a = []
    chords = buildChords()
    #print(chords)
    with open(filepath) as fp:
        for line in fp:
            if isChordLine(line,chords):
                for c in chords:
                    #print(c)
                    key = r"\b%s\b"%(c)
                    iter = re.finditer(key, line, re.IGNORECASE)
                    indices = [m.start(0) for m in iter]
                    for loc in indices:
                            a.append((c,loc))

                #print('chords found = ',a)
            else: # insert the chords into the line
                a.sort(key=itemgetter(1),reverse=True)
                #print(a)
                for item in a:
                    c = item[0]
                    loc = item[1]
                    if loc < len(line): 
                        # split the line into l and r
                        l,r = line[:loc],line[loc:] 
                    else: # handle chords extending beyond line
                        #print('len(line) = ', len(line), 'item = ', item)
                        whitespace = (loc-len(line))*' '
                        l = line.rstrip()+whitespace
                        r = '\n' # replace newline

                    line = l+'['+c+']'+r                     
                print(line,end='')
                a = [] 


if __name__ == '__main__':
    main()

