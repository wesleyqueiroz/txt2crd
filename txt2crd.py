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
    lastLine = lastMatches = lastPositions = None
    for l in inputFileStream:
        line = unicode(l, encoding='utf-8')
        matches, positions = getChordMatches(line)
        isChordLine = matches and positions and (removeWhitespaces(line) == ''.join(matches))
        if isChordLine:
            lastLine = line
            lastMatches = matches
            lastPositions = positions
        elif lastMatches and lastPositions and lastLine and line.strip():
            newLine = insertInLine(line, lastMatches, lastPositions)
            outputFileStream.write(newLine.encode('utf-8'))
            lastLine = lastMatches = lastPositions = None
        else:
            if lastLine:
                outputFileStream.write(lastLine.encode('utf-8'))
                lastLine = lastMatches = lastPositions = None
            outputFileStream.write(line.encode('utf-8'))

    inputFileStream.close()
    outputFileStream.close()

def removeWhitespaces(line):
    return line.replace(' ', '').replace('\n', '')
        
def insertInLine(line, matches, positions):
    def insert(original, new, pos):
        return original[:pos] + new + original[pos:]
    i = 0
    insertOffset = 1
    newLine = line
    while i < len(matches):
        newLine = insert(newLine, "[%s]" % matches[i], positions[i] + insertOffset - 1)
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
    fullPattern = chordFormPattern + "(?:/%s)?\s" % (notes + accidentals)
    matches = [removeWhitespaces(x) for x in re.findall(fullPattern, line)]
    positions = [x.start() for x in re.finditer(fullPattern, line)]

    return matches, positions

if __name__ == "__main__":
    main()