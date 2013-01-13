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

def convert2Chordpro(filePath):
    """
    Opens and closes the input and output files.

    @param filePath: Path to opened input file.
    @type filePath: string.
    """
    inputFileStream = open(filePath, 'r')
    lineToWrite = getChordProLines(inputFileStream)
    inputFileStream.close()

    outputFileName = filePath.split("/")[-1][:-4] + ".crd"
    outputFileStream = open(outputFileName, 'w')
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
        isChordLine = matches and positions and (getLineWithoutWhitespaces(line) == ''.join(matches))
        lastIsChordLine = lastMatches and lastPositions and lastLine
        isLyricsLine = not isChordLine and line.strip()
        if isChordLine and not lastIsChordLine:
            lastLine = line
            lastMatches = matches
            lastPositions = positions
        elif lastIsChordLine and isLyricsLine:
            lineToWrite += getLineWithInsertedChords(line, lastMatches, lastPositions)
            lastLine = lastMatches = lastPositions = None
        else:
            if lastLine:
                lineToWrite += getLineWithBracketsAroundChords(lastLine, lastMatches)
                lastLine = lastMatches = lastPositions = None
            lineToWrite += getLineWithBracketsAroundChords(line, matches)

    return lineToWrite.encode('utf-8')

def getLineWithBracketsAroundChords(line, chords):
    """
    Puts square brackets around all chords in line

    @param line: Line containing chords
    @type line: string
    @param chords: List of chords
    @type line: [string]
    """
    newLine = line
    for chord in chords:
        newLine = newLine.replace("%s " % chord, "[%s] " % chord, 1)
        newLine = newLine.replace(" %s" % chord, " [%s]" % chord, 1)
        newLine = newLine.replace(" %s " % chord, " [%s] " % chord, 1)

    return newLine

def getLineWithoutWhitespaces(line):
    """
    Replaces whitespaces in line with empty string.

    @param line: Line to remove white spaces in.
    @type line: string

    @return: Line without whitespaces.
    @returntype: string
    """
    return line.replace(' ', '').replace('\n', '')
        
def getLineWithInsertedChords(line, matches, positions):
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

    notes = "[ABCDEFG]"
    accidentals = "(?:#|##|b|bb)?"
    chordType = "(?:Min|min|m)?(?:maj|Maj|add|Add|sus|Sus|aug|Aug|dim|Dim)?"
    additions = "(?:1|2|3|4|5|6|7|8|9|10|11|12|13)?"
    bassNote = notes + accidentals
    chordFormPattern = bassNote + chordType + additions
    fullPattern = "%s(?:/%s)?\s" % (chordFormPattern, bassNote)
    matches = [getLineWithoutWhitespaces(x) for x in re.findall(fullPattern, line)]
    positions = [x.start() for x in re.finditer(fullPattern, line)]

    return matches, positions

if __name__ == "__main__":
    main()