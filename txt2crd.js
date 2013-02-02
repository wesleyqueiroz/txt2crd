function markAsTab() {
    var textArea = document.getElementById('textArea');
    var start = textArea.selectionStart;
    var end = textArea.selectionEnd;
    if (start < end) {
        var length = textArea.value.length;
        var replace = "{start_of_tab}" + textArea.value.substring(start, end) + "{end_of_tab}";
        textArea.value = textArea.value.substring(0, start) + replace + textArea.value.substring(end, length);
    }
}

function markAsChorus() {

}

function convertToChordpro() {
    var lines = document.getElementById('textArea').value.split("\n");
    for (var i = 0; i < lines.length; i++) {
        alert(getChordMatches(lines[i]));
    }
}

function getChordMatches(line) {
    var notes = "[ABCDEFG]";
    var accidentals = "(?:#|##|b|bb)?";
    var chordType = "(?:Min|min|m)?(?:maj|Maj|add|Add|sus|Sus|aug|Aug|dim|Dim)?";
    var additions = "(?:1|2|3|4|5|6|7|8|9|10|11|12|13)?";
    var bassNote = notes + accidentals;
    var chordFormPattern = bassNote + chordType + additions;
    var fullPattern = chordFormPattern + "(?:/" + bassNote + ")?\s";

    return line.search(fullPattern);
}
