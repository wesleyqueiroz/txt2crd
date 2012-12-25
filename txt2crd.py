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
    
    for line in inputFileStream:
        chordMatches = getChordMatches(line)
        

def getChordMatches(line):
    import re
    notes = "[ABCDEFG]";
    accidentals = "(?:#|##|b|bb)?";
    chords = "(?:maj|min|m|sus|aug|dim)?"
    additions = "[0-9]?"
    chordFormPattern = notes + accidentals + chords + additions
    fullPattern = chordFormPattern + "(?:/%s)?\s" % chordFormPattern
    matches = [x.replace(' ', '').replace('\n', '') for x in re.findall(fullPattern, line)]
    print "Line: " + line + "Matches: " + str(matches) + '\n'
    return matches

if __name__ == "__main__":
    main()