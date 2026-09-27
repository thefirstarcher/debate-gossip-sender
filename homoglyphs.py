#!/usr/bin/env python3
"""Look-alike substitutes for Cyrillic letters, to make each send unique.

HOMO maps a Cyrillic char -> list of confusables that render (near) identically:
Latin twins, Greek, and the char itself. `vary(text)` randomly swaps letters
so the text reads the same to a human but differs byte-for-byte.

    from homoglyphs import vary
    vary("Паша підсуди")   # -> "Пaшa пiдсуди" etc.
"""
import random
import unicodedata

# Base confusables — self + Greek/digit twins that render (near) identically.
HOMO = {
    "А": ["А", "A", "Α"], "Б": ["Б"], "В": ["В", "B", "Β"], "Г": ["Г", "Γ"],
    "Ґ": ["Ґ"], "Д": ["Д"], "Е": ["Е", "E", "Ε"], "Є": ["Є"], "Ж": ["Ж"],
    "З": ["З", "3"], "И": ["И"], "І": ["І", "I", "Ι", "l"], "Ї": ["Ї", "Ï"],
    "Й": ["Й"], "К": ["К", "K", "Κ"], "Л": ["Л", "Λ"], "М": ["М", "M", "Μ"],
    "Н": ["Н", "H", "Η"], "О": ["О", "O", "Ο"], "П": ["П", "Π"], "Р": ["Р", "P", "Ρ"],
    "С": ["С", "C", "Ϲ"], "Т": ["Т", "T", "Τ"], "У": ["У", "Y", "Υ"], "Ф": ["Ф", "Φ"],
    "Х": ["Х", "X", "Χ"], "Ц": ["Ц"], "Ч": ["Ч"], "Ш": ["Ш"], "Щ": ["Щ"],
    "Ь": ["Ь"], "Ю": ["Ю"], "Я": ["Я"],
    "а": ["а", "a", "α"], "б": ["б"], "в": ["в"], "г": ["г"], "ґ": ["ґ"],
    "д": ["д"], "е": ["е", "e"], "є": ["є"], "ж": ["ж"], "з": ["з"],
    "и": ["и"], "і": ["і", "i", "ι", "l"], "ї": ["ї", "ï"], "й": ["й"],
    "к": ["к"], "л": ["л"], "м": ["м"], "н": ["н"], "о": ["о", "o", "ο"],
    "п": ["п"], "р": ["р", "p", "ρ"], "с": ["с", "c", "ϲ"], "т": ["т"],
    "у": ["у", "y", "γ"], "ф": ["ф"], "х": ["х", "x", "χ"], "ц": ["ц"],
    "ч": ["ч"], "ш": ["ш"], "щ": ["щ"], "ь": ["ь"], "ю": ["ю"], "я": ["я"],
}

# Which Latin letter each Cyrillic char looks like — lets us pull that letter's
# whole Mathematical-Alphanumeric family (bold/italic/sans/script/…) + fullwidth.
LATIN_TWIN = {
    "А": "A", "В": "B", "Е": "E", "І": "I", "К": "K", "М": "M", "Н": "H",
    "О": "O", "Р": "P", "С": "C", "Т": "T", "У": "Y", "Х": "X",
    "а": "a", "е": "e", "і": "i", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x",
}

# Start codepoints of each 26-letter Mathematical Alphanumeric style block.
_MATH_UP = [0x1D400, 0x1D434, 0x1D468, 0x1D49C, 0x1D4D0, 0x1D504, 0x1D538,
            0x1D56C, 0x1D5A0, 0x1D5D4, 0x1D608, 0x1D63C, 0x1D670]
_MATH_LO = [0x1D41A, 0x1D44E, 0x1D482, 0x1D4B6, 0x1D4EA, 0x1D51E, 0x1D552,
            0x1D586, 0x1D5BA, 0x1D5EE, 0x1D622, 0x1D656, 0x1D68A]


def _math_family(letter):
    """All wide-glyph variants of an ASCII letter: math styles + fullwidth.
    Skips reserved holes (script B, fraktur C, …) via the Cn category check."""
    a, base = ("A", _MATH_UP) if letter.isupper() else ("a", _MATH_LO)
    off = ord(letter) - ord(a)
    out = [chr(0xFF21 if letter.isupper() else 0xFF41 + 0)]  # placeholder, fixed below
    out = [chr((0xFF21 if letter.isupper() else 0xFF41) + off)]  # fullwidth
    for start in base:
        ch = chr(start + off)
        if unicodedata.category(ch) != "Cn":  # skip undefined reserved slots
            out.append(ch)
    return out


# Cyrillic letters whose only twin is Greek — pull the Mathematical-Greek family.
GREEK_TWIN = {"Г": "Γ", "Л": "Λ", "П": "Π", "Ф": "Φ"}
_GREEK_UP = [0x1D6A8, 0x1D6E2, 0x1D71C, 0x1D756, 0x1D790]  # bold, italic, bolditalic, sans-bold, sans-bolditalic
_GREEK_ORDER = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΘΣΤΥΦΧΨΩ"  # ΘΣΤ… positions per math-Greek block


def _greek_family(letter):
    off = _GREEK_ORDER.index(letter)
    out = []
    for start in _GREEK_UP:
        ch = chr(start + off)
        if unicodedata.category(ch) != "Cn":
            out.append(ch)
    return out


for _cyr, _lat in LATIN_TWIN.items():
    HOMO[_cyr].extend(_math_family(_lat))
for _cyr, _gr in GREEK_TWIN.items():
    HOMO[_cyr].extend(_greek_family(_gr))
for _cyr in HOMO:
    HOMO[_cyr] = list(dict.fromkeys(HOMO[_cyr]))  # dedupe, keep order


# Invisible characters — render as nothing but change the bytes.
ZW = ["​", "‌", "‍", "⁠", "﻿"]  # ZWSP ZWNJ ZWJ WJ BOM


def sprinkle(text, n=2):
    """Insert n random invisible chars at random positions (not at the very end,
    where Telegram may trim them)."""
    chars = list(text)
    for _ in range(n):
        i = random.randint(0, max(0, len(chars) - 1))
        chars.insert(i, random.choice(ZW))
    return "".join(chars)


def vary(text, p=0.6, zw=2):
    """Look-alike variant: swap letters for twins (p each) + zw invisible chars."""
    swapped = "".join(random.choice(HOMO[ch]) if ch in HOMO and random.random() < p else ch
                      for ch in text)
    return sprinkle(swapped, zw)


def unique(text, seen, p=0.6, tries=40):
    """A variant not already in `seen`. Bumps invisible-char count if it ever
    struggles, so it never gets stuck."""
    for k in range(tries):
        v = vary(text, p, zw=2 + k // 8)  # add more invisibles the harder it gets
        if v not in seen:
            seen.add(v)
            return v
    v = vary(text, p, zw=len(seen) % 20 + 3)  # ponytail: always wins
    seen.add(v)
    return v


def visible(s):
    """Strip invisibles — what a human actually sees."""
    for z in ZW:
        s = s.replace(z, "")
    return s


if __name__ == "__main__":
    src = "Паша підсуди"
    seen = set()
    for _ in range(5000):
        v = unique(src, seen)
        assert len(visible(v)) == len(src), "visible length changed"
    assert len(seen) == 5000, "unique() returned a duplicate"
    for s in list(seen)[:5]:
        print(repr(s))
    print("ok, 5000 unique variants, all visually identical")
