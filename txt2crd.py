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
    """
    Runs through the opened file and converts it line by line to chordpro format.

    @param filePath: Path to opened input file.
    @type filePath: string.
    """
    inputFileStream = open(filePath, 'r')
    outputFileName = filePath.split("/")[-1][:-4] + ".crd"
    outputFileStream = open(outputFileName, 'w')
    
    lineToWrite = getChordProLines(inputFileStream)

    inputFileStream.close()
    outputFileStream.write(lineToWrite)
    outputFileStream.close()

def getChordProLines(fileStream):
    """
    Runs through the opened file and converts it line by line to chordpro format.

    @param fileStream: Stream to text file to convert.

    @return: Converted lines.
    @returntype: string
    """
    lineToWrite = ""
    matches = positions = []
    lastLine = lastMatches = lastPositions = None
    for l in fileStream:
        line = unicode(l, encoding='utf-8').replace(u"\u00A0", " ") # replace non breaking space with regular space
        matches, positions = getChordMatches(line)
        isChordLine = matches and positions and (removeWhitespaces(line) == ''.join(matches))
        lastIsChordLine = lastMatches and lastPositions and lastLine
        if isChordLine and not lastIsChordLine:
            lastLine = line
            lastMatches = matches
            lastPositions = positions
        elif not isChordLine and lastIsChordLine and line.strip():
            newLine = insertInLine(line, lastMatches, lastPositions)
            lineToWrite += newLine.encode('utf-8')
            lastLine = lastMatches = lastPositions = None
        else:
            if lastLine:
                lineToWrite += lastLine.encode('utf-8')
                lastLine = lastMatches = lastPositions = None
            lineToWrite += line.encode('utf-8')

    return lineToWrite

def removeWhitespaces(line):
    """
    Replaces whitespaces in line with empty string.

    @param line: Line to remove white spaces in.
    @type line: string

    @return: Line without whitespaces.
    @returntype: string
    """
    return line.replace(' ', '').replace('\n', '')
        
def insertInLine(line, matches, positions):
    """
    Inserts chords into line according to specified positions.
    E.g. if there's supposed to be a C in the line at position 10 and a 
    Am at position 21 then this will inject "[C]" and "[Am]" into the correct place.

    @param line: Text line to inject chords into.
    @type line: string

    @param matches: List of chords to inject.
    @type matches: [string]

    @param position: List of positions that matches the list of chords.
    @type position: [int]

    @return: Line with chords injected in it.
    @returntype: string
    """
    def insert(original, new, pos):
        return original[:pos] + new + original[pos:]
    def getLineWithTrailingSpaces(line, numberOfSpaces):
        return line + numberOfSpaces * ' '
    i = 0
    insertOffset = 1
    newLine = line.replace('\n', '')

    if len(newLine) < positions[-1]:
        newLine = getLineWithTrailingSpaces(newLine, positions[-1] - len(newLine))

    while i < len(matches):
        newLine = insert(newLine, "[%s]" % matches[i], positions[i] + insertOffset - 1)
        insertOffset += len(matches[i]) + 2
        i += 1

    return newLine + '\n'

def getChordMatches(line):
    """
    Checks line for occurrences of chords.

    @param line: Text line to check for chords.
    @type line: string

    @return: A list of chords and a list of chord positions
    @returntype: [string], [int]
    """
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