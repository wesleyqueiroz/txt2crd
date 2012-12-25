# -*- coding: utf-8 -*-

def main():
    import sys

    validInput = len(sys.argv) > 1
    if validInput:
        filePath = sys.argv[1]
        convert2Chordpro(filePath)
    else:
        print "Invalid file path. Correct usage is:"
        print "e.g.python txt2crd.py input_file.txt"
        sys.exit(2)

def convert2Chordpro(filePath):
    inputFileStream = open(filePath, 'r')
    outputFileName = filePath.split("/")[-1][:-4] + ".crd"
    outputFileStream = open(outputFileName, 'w')
    
    matches = positions = []
    for line in inputFileStream:
        decodedLine = unicode(line, encoding='utf-8')
        if decodedLine.strip():
            matches, positions = getChordMatches(decodedLine)
            if matches and positions:
                lastLine = decodedLine
                lastMatches = matches
                lastPositions = positions
            else:
                newLine = insertInLine(decodedLine, lastMatches, lastPositions)
                outputFileStream.write(newLine.encode('utf-8'))
        else:
            outputFileStream.write('\n')

    inputFileStream.close()
    outputFileStream.close()

def insert(original, new, pos):
    return original[:pos] + new + original[pos:]
        
def insertInLine(line, matches, positions):
    i = 0
    insertOffset = 1
    newLine = line
    while i < len(matches):
        newLine = insert(newLine, "[%s]" % matches[i], positions[i] + insertOffset)
        insertOffset += len(matches[i]) + 2
        i += 1

    return newLine

def getChordMatches(line):
    import re

    notes = "[ABCDEFG]";
    accidentals = "(?:#|##|b|bb)?";
    chords = "(?:maj|min|m|sus|aug|dim)?"
    additions = "[0-9]?"
    chordFormPattern = notes + accidentals + chords + additions
    fullPattern = chordFormPattern + "(?:/%s)?\s" % chordFormPattern
    matches = [x.replace(' ', '').replace('\n', '') for x in re.findall(fullPattern, line)]
    positions = [x.start() for x in re.finditer(fullPattern, line)]

    return matches, positions

if __name__ == "__main__":
    main()