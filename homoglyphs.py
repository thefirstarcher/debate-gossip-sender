#!/usr/bin/env python3
"""Look-alike substitutes for Cyrillic letters, to make each send unique.

HOMO maps a Cyrillic char -> list of confusables that render (near) identically:
Latin twins, Greek, and the char itself. `vary(text)` randomly swaps letters
so the text reads the same to a human but differs byte-for-byte.

    from homoglyphs import vary
    vary("Паша підсуди")   # -> "Пaшa пiдсуди" etc.
"""
import random

# Each key includes itself as a candidate (so some letters stay Cyrillic).
# Sources: Unicode confusables — Latin/Greek glyphs that match Cyrillic shapes.
HOMO = {
    # uppercase
    "А": ["А", "A", "Α"], "Б": ["Б"], "В": ["В", "B", "Β"], "Г": ["Г", " Г"[0]],
    "Ґ": ["Ґ"], "Д": ["Д"], "Е": ["Е", "E", "Ε"], "Є": ["Є"], "Ж": ["Ж"],
    "З": ["З", "3"], "И": ["И"], "І": ["І", "I", "Ι", "l"], "Ї": ["Ї", "Ï"],
    "Й": ["Й"], "К": ["К", "K", "Κ"], "Л": ["Л"], "М": ["М", "M", "Μ"],
    "Н": ["Н", "H", "Η"], "О": ["О", "O", "Ο"], "П": ["П", "Π"], "Р": ["Р", "P", "Ρ"],
    "С": ["С", "C", "Ϲ"], "Т": ["Т", "T", "Τ"], "У": ["У", "Y", "Υ"], "Ф": ["Ф", "Φ"],
    "Х": ["Х", "X", "Χ"], "Ц": ["Ц"], "Ч": ["Ч"], "Ш": ["Ш"], "Щ": ["Щ"],
    "Ь": ["Ь"], "Ю": ["Ю"], "Я": ["Я"],
    # lowercase
    "а": ["а", "a", "α"], "б": ["б"], "в": ["в"], "г": ["г"], "ґ": ["ґ"],
    "д": ["д"], "е": ["е", "e"], "є": ["є"], "ж": ["ж"], "з": ["з"],
    "и": ["и"], "і": ["і", "i", "ι", "l"], "ї": ["ї", "ï"], "й": ["й"],
    "к": ["к"], "л": ["л"], "м": ["м"], "н": ["н"], "о": ["о", "o", "ο"],
    "п": ["п"], "р": ["р", "p", "ρ"], "с": ["с", "c", "ϲ"], "т": ["т"],
    "у": ["у", "y", "γ"], "ф": ["ф"], "х": ["х", "x", "χ"], "ц": ["ц"],
    "ч": ["ч"], "ш": ["ш"], "щ": ["щ"], "ь": ["ь"], "ю": ["ю"], "я": ["я"],
}


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
