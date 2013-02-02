function markAsTab() {
    var textContent = document.getElementById('textContent');
    if (textContent.selectionStart < textContent.selectionEnd) {
        textContent.selectedText = textContent.value.substring(textContent.selectionStart, textContent.selectionEnd);
        alert("Selection Start==> " + textContent.selectionStart + "\n" +
              "Selection End  ==> " + textContent.selectionEnd + "\n" +
              "Selected Text  ==> " + textContent.selectedText + "\n" +
              "TextArea Value ==> " + textContent.value);
    }
}

function markAsChorus() {

}

function convertToChordpro() {
    var lines = document.getElementById('textContent').value.split("\n");
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
