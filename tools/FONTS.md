# Fonts in the illustrations

The SVGs in [`assets/`](../assets/) draw their text as vector outlines, because GitHub serves SVGs as images that cannot load web fonts. [`glyphs.json`](glyphs.json) holds those outlines, extracted by [`extract_glyphs.py`](extract_glyphs.py) from three typefaces released under the SIL Open Font License, Version 1.1:

| Style in `glyphs.json` | Typeface | Copyright |
| --- | --- | --- |
| `display`, `display-italic` | Fraunces Medium and Italic (via npm `@fontsource/fraunces`) | © 2020 The Fraunces Project Authors (github.com/undercasetype/Fraunces) |
| `mono`, `mono-medium` | JetBrains Mono Regular and Medium | © 2020 The JetBrains Mono Project Authors (github.com/JetBrains/JetBrainsMono) |
| `sans`, `sans-medium` | Inter Regular and Medium | © 2016 The Inter Project Authors (github.com/rsms/inter) |

The license text is at <https://openfontlicense.org>. The outlines are used to render text in this profile's illustrations; the fonts themselves are not redistributed here. The same type families appear across the Vers3Dynamics sites, which keeps the profile's graphics in the lab's existing visual identity.
