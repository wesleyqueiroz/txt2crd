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
    var lines = document.getElementById('textArea').value.split("\n");
    for (var i = 0; i < lines.length; i++) {
        var matches = getChordMatches(lines[i]);
        var chords = matches.chords;
        var positions = matches.positions;
    }
}

function getChordMatches(line) {
    var pattern = /[ABCDEFG](?:#|##|b|bb)?(?:min|m)?(?:maj|add|sus|aug|dim)?[0-9]*(?:\/[ABCDEFG](?:#|##|b|bb)?)?/gi;
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
