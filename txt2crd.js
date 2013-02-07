function markSubstring(markStart, markEnd) {
    "use strict";
    var textArea, start, end, length, replace;
    textArea = document.getElementById('textArea');
    start = textArea.selectionStart;
    end = textArea.selectionEnd;
    if (start < end) {
        length = textArea.value.length;
        replace = markStart + textArea.value.substring(start, end) + markEnd;
        textArea.value = textArea.value.substring(0, start) + replace + textArea.value.substring(end, length);
    }
}

function markAsTab() {
    "use strict";
    markSubstring("{start_of_tab}\n", "\n{end_of_tab}");
}

function markAsChorus() {
    "use strict";
    markSubstring("{start_of_chorus}\n", "\n{end_of_chorus}");
}

String.prototype.trim = function () {
    "use strict";
    return String(this).replace(/^\s+|\s+$/g, '');
};

function getChordMatches(line) {
    "use strict";
    var match, pattern, chords, chordLength, positions, i;
    pattern = /(?:^|\s)[A-G](?:##?|bb?)?(?:min|m)?(?:Maj|maj|Add|add|Sus|sus|Aug|aug|Dim|dim)?[0-9]*(?:\/[A-G](?:##?|bb?)?)?(?!\S)/g;
    chords = line.match(pattern);
    chordLength = -1;
    positions = [];
    while ((match = pattern.exec(line)) !== null) {
        positions.push(match.index);
    }

    for (i = 0; chords && i < chords.length; i += 1) {
        chordLength = chords[i].length;
        chords[i] = chords[i].trim();
        positions[i] -= chords[i].length - chordLength;
    }

    return {
        "chords": chords,
        "positions": positions
    };
}

function isChordsOnly(line, chords) {
    "use strict";
    return (line.replace(/\s+/g, '') === chords.join(""));
}

String.prototype.repeat = function (num) {
    "use strict";
    var tmpArray = [];
    tmpArray[num] = undefined;
    return tmpArray.join(this);
};

String.prototype.insert = function (index, string) {
    "use strict";
    if (index > 0) {
        return this.substring(0, index) + string + this.substring(index, this.length);
    }
    return string + this;
};

function getLineWithInsertedChords(line, chords, positions) {
    "use strict";
    var i, insertOffset, newLine;
    i = 0;
    insertOffset = 0;
    newLine = line.replace("\n", "");
    if (newLine.length < positions[positions.length - 1]) {
        newLine = newLine + " ".repeat(positions[positions.length - 1] - newLine.length);
    }
    while (i < chords.length) {
        newLine = newLine.insert(positions[i] + insertOffset, "[" + chords[i] + "]");
        insertOffset += chords[i].length + 2;
        i += 1;
    }

    return newLine + "\n";
}

function getLineWithBracketsAroundChords(line, chords) {
    "use strict";
    var newLine, chord, i;
    newLine = line;
    if (chords) {
        for (i = 0; i < chords.length; i += 1) {
            chord = chords[i];
            newLine = newLine.replace(chord + " ", "[" + chord + "] ");
            newLine = newLine.replace(" " + chord, " [" + chord + "]");
            newLine = newLine.replace(" " + chord + " ", " [" + chord + "] ");
        }
    }

    return newLine + "\n";
}

function convert(textAreaValue) {
    "use strict";
    var chordProLine, matches, line, chords, positions, lastLine, lastChords, lastPositions, isChordLine, isTabLine, isLyricsLine, lastIsChordLine, textArea, lines, i;
    chordProLine = "";
    matches = line = chords = positions = lastLine = lastChords = lastPositions = null;
    isChordLine = isLyricsLine = lastIsChordLine = isTabLine = false;
    lines = textAreaValue.split("\n");
    for (i = 0; i < lines.length; i += 1) {
        line = lines[i].replace(/\t/g, '        ');
        matches = getChordMatches(line);
        chords = matches.chords;
        positions = matches.positions;
        isTabLine = ((isTabLine === true) || (line.indexOf("{start_of_tab}") !== -1)) && (line.indexOf("{end_of_tab}") === -1);
        isChordLine = (isTabLine === false) && (chords !== null) && (positions !== null) && isChordsOnly(line, chords);
        lastIsChordLine = (lastChords !== null) && (lastPositions !== null);
        isLyricsLine = (isTabLine === false) && (isChordLine === false) && (line.trim() !== "");
        if (isChordLine && !lastIsChordLine) {
            lastLine = line;
            lastChords = chords;
            lastPositions = positions;
        } else if (lastIsChordLine && isLyricsLine) {
            chordProLine += getLineWithInsertedChords(line, lastChords, lastPositions);
            lastLine = lastChords = lastPositions = null;
        } else if (isTabLine) {
            chordProLine += line + "\n";
        } else {
            if (lastLine) {
                chordProLine += getLineWithBracketsAroundChords(lastLine, lastChords);
                lastLine = lastChords = lastPositions = null;
            }
            chordProLine += getLineWithBracketsAroundChords(line, chords);
        }
    }

    return chordProLine;
}

function convertToChordpro() {
    "use strict";
    var textArea = document.getElementById('textArea');
    textArea.value = convert(textArea.value);
}
