function markAsTab() {
    markSubstring("{start_of_tab}", "{end_of_tab}");
}

function markAsChorus() {
    markSubstring("{start_of_chorus}", "{end_of_chorus}");
}

function markSubstring(markStart, markEnd) {
    var textArea = document.getElementById('textArea');
    var start = textArea.selectionStart;
    var end = textArea.selectionEnd;
    if (start < end) {
        var length = textArea.value.length;
        var replace = markStart + textArea.value.substring(start, end) + markEnd;
        textArea.value = textArea.value.substring(0, start) + replace + textArea.value.substring(end, length);
    }
}

function convertToChordpro() {
    var chordProLine = "";
    var matches = line = null;
    var chords = positions = lastLine = lastChords = lastPositions = null;
    var isChordLine = isLyricsLine = lastIsChordLine = false;
    var textArea = document.getElementById('textArea');
    var lines = textArea.value.split("\n");
    for (var i = 0; i < lines.length; i++) {
        line = lines[i];
        matches = getChordMatches(line);
        chords = matches.chords;
        positions = matches.positions;
        isChordLine = (chords != null) && (positions != null) && isChordsOnly(line, chords);
        lastIsChordLine = (lastChords != null) && (lastPositions != null);
        isLyricsLine = (isChordLine == false) && (line.trim != "");
        if (isChordLine && !lastIsChordLine) {
            lastLine = line;
            lastChords = chords;
            lastPositions = positions;
        } 
        else if (lastIsChordLine && isLyricsLine) {
            chordProLine += getLineWithInsertedChords(line, lastChords, lastPositions);
            lastLine = lastChords = lastPositions = null;
        } 
        else {
            if (lastLine) {
                chordProLine += getLineWithBracketsAroundChords(lastLine, lastChords);
                lastLine = lastChords = lastPositions = null;
            }
            chordProLine += getLineWithBracketsAroundChords(line, chords);
        }
    }

    textArea.value = chordProLine;
}

function getLineWithBracketsAroundChords(line, chords) {
    var newLine = line;
    if (chords) {
        for (var i = 0; i < chords.length; i++) {
            chord = chords[i];
            newLine = newLine.replace(chord + " ", "[" + chord + "] ");
            newLine = newLine.replace(" " + chord, " [" + chord + "]");
            newLine = newLine.replace(" " + chord + " ", " [" + chord + "] ");
        }
    };

    return newLine + "\n";
}

function isChordsOnly(line, chords) {
    return (line.replace(/\s+/g, '') == chords.join(""));
}

String.prototype.repeat = function(num) {
    return new Array(num + 1).join(this);
};

String.prototype.trim = function() {
    return String(this).replace(/^\s+|\s+$/g, '');
};

String.prototype.insert = function (index, string) {
  if (index > 0)
    return this.substring(0, index) + string + this.substring(index, this.length);
  else
    return string + this;
};

function getLineWithInsertedChords(line, chords, positions) {
    var i = 0;
    var insertOffset = 0;
    var newLine = line.replace("\n", "");

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

function getChordMatches(line) {
    var pattern = /[ABCDEFG](?:#|##|b|bb)?(?:min|m)?(?:maj|add|sus|aug|dim)?[0-9]*(?:\/[ABCDEFG](?:#|##|b|bb)?)?/g;
    var chords = line.match(pattern);
    var positions = [];
    while ((match = pattern.exec(line)) != null) {
        positions.push(match.index);
    }

    return {
        "chords":chords,
        "positions":positions
    };
}
