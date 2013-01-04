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
        print "Running tests instead!"
        runTests()

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
        isLyricsLine = not isChordLine and line.strip()
        if isChordLine and not lastIsChordLine:
            lastLine = line
            lastMatches = matches
            lastPositions = positions
        elif lastIsChordLine and isLyricsLine:
            newLine = insertInLine(line, lastMatches, lastPositions)
            lineToWrite += newLine.encode('utf-8')
            lastLine = lastMatches = lastPositions = None
        elif lastIsChordLine and not isLyricsLine:
            newLine = insertInLine("", lastMatches, lastPositions)
            lineToWrite += newLine
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
    additions = "(?:1|2|3|4|5|6|7|8|9|10|11)?"
    chordFormPattern = notes + accidentals + chords + additions
    fullPattern = chordFormPattern + "(?:/%s)?\s" % (notes + accidentals)
    matches = [removeWhitespaces(x) for x in re.findall(fullPattern, line)]
    positions = [x.start() for x in re.finditer(fullPattern, line)]

    return matches, positions

def runTests():
    """
    Runs a set of unit tests that are expected to pass.
    """
    # 1. Test simple chords and a chord that ends after the lyrics line
    line1 = "G                  Em              A\n"
    line2 = "...Jag är den som aldrig säger nej\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "[G]...Jag är den som a[Em]ldrig säger nej [A]\n"
    assert actualLine == expectedLine, "'%s' doesn't match '%s'" % (actualLine, expectedLine)

    # 2. Test more advanced chords and alternate bass note
    line1 = "  Am          Am/G        D7/F#                 Fmaj7\n"
    line2 = "I look at you all see the love there that's sleeping\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "I [Am]look at you [Am/G]all see the [D7/F#]love there that's slee[Fmaj7]ping\n"
    assert actualLine == expectedLine, "'%s' doesn't match '%s'" % (actualLine, expectedLine)

    # 3. Test simple line with only chords and no lyrics.
    line1 = "G                  Em              A\n"
    line2 = "\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "[G]                   [Em]                [A]\n"
    assert actualLine == expectedLine, "'%s' doesn't match '%s'" % (actualLine, expectedLine)

    # 4. Test simple line with no chords
    line1 = "Chorus:\n"
    line2 = "\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = line1 + "\n"
    assert actualLine == expectedLine, "'%s' doesn't match '%s'" % (actualLine, expectedLine)

    # 5. Test line with minor eleventh chord.
    line1 = "G                  E#m11              A\n"
    line2 = "...Jag är den som aldrig säger nej\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "[G]...Jag är den som a[E#m11]ldrig säger nej    [A]\n"
    assert actualLine == expectedLine, "'%s' doesn't match '%s'" % (actualLine, expectedLine)

    # 6. Test chord lines where no lyrics follow
    line1 = "solo:\n"
    line2 = "C  G  C  G  C  G Em  D  Em\n"
    line3 = "C     G     C      G      C     G Em  D    Em\n"
    actualLine = getChordProLines((line1, line2, line3))
    expectedLine = line1 + "[C]  [G]  [C]  [G]  [C]  [G] [Em]  [D]  [Em]\n" + "[C]     [G]     [C]      [G]      [C]     [G] [Em]  [D]    [Em]\n"
    assert actualLine == expectedLine, "'%s' doesn't match '%s'" % (actualLine, expectedLine)

if __name__ == "__main__":
    main()