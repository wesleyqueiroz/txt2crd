# -*- coding: utf-8 -*-

def runTests():
    """
    Runs a set of unit tests that are expected to pass.
    """
    from txt2crd import getChordProLines

    def assertEqual(actual, expected):
        if actual != expected:
            print "-= FAIL! =-\n"
            print "Actual:\n%s" % actual
            print "Expected:\n%s" % expected

    # 1. Test simple chords and a chord that ends after the lyrics line
    line1 = "G                  Em              A\n"
    line2 = "...Jag är den som aldrig säger nej\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "[G]...Jag är den som a[Em]ldrig säger nej [A]\n"
    assertEqual(actualLine, expectedLine)

    # 2. Test more advanced chords and alternate bass note
    line1 = "  Am          Am/G        D7/F#                 Fmaj7\n"
    line2 = "I look at you all see the love there that's sleeping\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "I [Am]look at you [Am/G]all see the [D7/F#]love there that's slee[Fmaj7]ping\n"
    assertEqual(actualLine, expectedLine)

    # 3. Test simple line with only chords and no lyrics.
    line1 = "G                  Em              A\n"
    line2 = "\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "[G]                  [Em]              [A]\n" + line2
    assertEqual(actualLine, expectedLine)

    # 4. Test simple line with no chords
    line1 = "Chorus:\n"
    line2 = "\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = line1 + "\n"
    assertEqual(actualLine, expectedLine)

    # 5. Test line with minor eleventh chord.
    line1 = "G                  E#m11              A\n"
    line2 = "...Jag är den som aldrig säger nej\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "[G]...Jag är den som a[E#m11]ldrig säger nej    [A]\n"
    assertEqual(actualLine, expectedLine)

    # 6. Test line with chords injected in regular text.
    line1 = "Interlude: Dm | F | C | Gm | Dm | <-- Played twice\n"
    line2 = "\n"
    actualLine = getChordProLines((line1, line2))
    expectedLine = "Interlude: [Dm] | [F] | [C] | [Gm] | [Dm] | <-- Played twice\n\n"
    assertEqual(actualLine, expectedLine)

    # 7. Test chord lines where no lyrics follow
    line1 = "solo:\n"
    line2 = "C  G  C  G  C  G Em  D  Em\n"
    line3 = "C     G     C      G      C     G Em  D    Em\n"
    actualLine = getChordProLines((line1, line2, line3))
    expectedLine = line1 + "[C]  [G]  [C]  [G]  [C]  [G] [Em]  [D]  [Em]\n" + \
                           "[C]     [G]     [C]      [G]      [C]     [G] [Em]  [D]    [Em]\n"
    assertEqual(actualLine, expectedLine)

    # 8. Test chord lines where no lyrics follow
    line1 = "\n"
    line2 = "CAPO ON 3RD FRET!\n"
    line3 = "\n"
    actualLine = getChordProLines((line1, line2, line3))
    expectedLine = line1 + line2 + line3
    assertEqual(actualLine, expectedLine)

    # 9. Test chord line with Emadd9
    line1 = "                And so Happy Christmas\n"
    line2 = "                    D            Em     Emadd9     Esus4      Em \n"
    line3 = "                We hope you have fun\n"
    actualLine = getChordProLines((line1, line2, line3))
    expectedLine = line1 + "                We h[D]ope you have [Em]fun    [Emadd9]           [Esus4]           [Em]\n"
    assertEqual(actualLine, expectedLine)

    # 10. Test chord line with Aminmaj7
    line1 = "                I hope you have fun\n"
    line2 = "                    D            Em     Aminmaj7     Esus4      Em \n"
    line3 = "                We hope you have fun\n"
    actualLine = getChordProLines((line1, line2, line3))
    expectedLine = line1 + "                We h[D]ope you have [Em]fun    [Aminmaj7]             [Esus4]           [Em]\n"
    assertEqual(actualLine, expectedLine)

if __name__ == "__main__":
    runTests()