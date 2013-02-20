test("Test markSubstring.", function() {
    var actualLine = " ".repeat(4);
    var expectedLine = "    ";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test string repeat.", function() {
    var actualLine = " ".repeat(4);
    var expectedLine = "    ";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test string trim.", function() {
    var actualLine = "  Hi there !    ".trim();
    var expectedLine = "Hi there !";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test string insert.", function() {
    var actualLine = "What a world!".insert(7, "beautiful ");
    var expectedLine = "What a beautiful world!";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);

    actualLine = "what a world!".insert(0, "Beautiful, ");
    expectedLine = "Beautiful, what a world!";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test isChordsOnly().", function() {
    ok(isChordsOnly("    Am      G     E ", ["Am", "G", "E"]) === true, "Failed!");
    ok(isChordsOnly("A B C, easy as one, two, three ...", ["A", "B", "C"]) === false, "Failed!");
});

test("Test simple chords and a chord that ends after the lyrics line.", function() {
    var line1 = "G                  Em              A\n";
    var line2 = "...Jag är den som aldrig säger nej";
    var actualLine = convert(line1 + line2);
    var expectedLine = "[G]...Jag är den som a[Em]ldrig säger nej [A]\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test more advanced chords and alternate bass note.", function() {
    var line1 = "  Am          Am/G        D7/F#                 Fmaj7\n";
    var line2 = "I look at you all see the love there that's sleeping";
    var actualLine = convert(line1 + line2);
    var expectedLine = "I [Am]look at you [Am/G]all see the [D7/F#]love there that's slee[Fmaj7]ping\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test simple line with only chords and no lyrics.", function() {
    var line1 = "G                  Em              A\n";
    var line2 = "";
    var actualLine = convert(line1 + line2);
    var expectedLine = "[G]                  [Em]              [A]\n\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test simple line with no chords.", function() {
    var line1 = "Chorus:\n";
    var line2 = "";
    var actualLine = convert(line1 + line2);
    var expectedLine = "Chorus:\n\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test line with minor eleventh chord.", function() {
    var line1 = "G                  E#m11              A\n";
    var line2 = "...Jag är den som aldrig säger nej";
    var actualLine = convert(line1 + line2);
    var expectedLine = "[G]...Jag är den som a[E#m11]ldrig säger nej    [A]\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test line with chords injected in regular text.", function() {
    var line1 = "Interlude: Dm | F | C | Gm | Dm | <-- Played twice\n";
    var line2 = "";
    var actualLine = convert(line1 + line2);
    var expectedLine = "Interlude: [Dm] | [F] | [C] | [Gm] | [Dm] | <-- Played twice\n\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test chord lines where no lyrics follow.", function() {
    var line1 = "solo:\n";
    var line2 = "C  G  C  G  C  G Em  D  Em\n";
    var line3 = "C     G     C      G      C     G Em  D    Em";
    var actualLine = convert(line1 + line2 + line3);
    var expectedLine = line1 + "[C]  [G]  [C]  [G]  [C]  [G] [Em]  [D]  [Em]\n" +
                               "[C]     [G]     [C]      [G]      [C]     [G] [Em]  [D]    [Em]\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test chord lines where no lyrics follow.", function() {
    var line1 = "\n";
    var line2 = "CAPO ON 3RD FRET!\n";
    var line3 = "";
    var actualLine = convert(line1 + line2 + line3);
    var expectedLine = line1 + line2 + line3 + "\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test chord line with Emadd9.", function() {
    var line1 = "                And so Happy Christmas\n";
    var line2 = "                    D            Em     Emadd9     Esus4      Em \n";
    var line3 = "                We hope you have fun";
    var actualLine = convert(line1 + line2 + line3);
    var expectedLine = line1 + "                We h[D]ope you have [Em]fun    [Emadd9]           [Esus4]           [Em]\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test chord line with Aminmaj7.", function() {
    var line1 = "                I hope you have fun\n";
    var line2 = "                    D            Em     Aminmaj7     Esus4      Em \n";
    var line3 = "                We hope you have fun";
    var actualLine = convert(line1 + line2 + line3);
    var expectedLine = line1 + "                We h[D]ope you have [Em]fun    [Aminmaj7]             [Esus4]           [Em]\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test chord line with AmMaj7.", function() {
    var line1 = "                I hope you have fun\n";
    var line2 = "                    D            Em     AmMaj7     Esus4      Em \n";
    var line3 = "                We hope you have fun";
    var actualLine = convert(line1 + line2 + line3);
    var expectedLine = line1 + "                We h[D]ope you have [Em]fun    [AmMaj7]           [Esus4]           [Em]\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test parts marked as tab", function() {
    var line1 = "{start_of_tab}\n";
    var line2 = "D            Em     AmMaj7     Esus4      Em \n";
    var line3 = "A lot of people like to sing and play!\n"
    var line4 = "{end_of_tab}";
    var actualLine = convert(line1 + line2 + line3 + line4);
    var expectedLine = line1 + line2 + line3 + line4 + "\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test G followed by Gmaj7.", function() {
    var line1 = " G      Gmaj7  Em     Em     \n";
    var line2 = "";
    var actualLine = convert(line1 + line2);
    var expectedLine = " [G]      [Gmaj7]  [Em]     [Em]     \n\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});

test("Test AM7", function() {
    var line1 = " AM7 \n";
    var line2 = "";
    var actualLine = convert(line1 + line2);
    var expectedLine = " [AM7] \n\n";
    ok(actualLine === expectedLine, "\nA:" + actualLine + "\nE:" + expectedLine);
});
