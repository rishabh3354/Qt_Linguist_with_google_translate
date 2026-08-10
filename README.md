# Qt Linguist with Google Translate

**Auto-translate Qt Linguist `.ts` files with Google Translate, then compile them to `.qm`.**

Localising a Qt or PyQt app means filling in hundreds of `<translation>` tags by hand, per language. These scripts fill them automatically, so you start from a complete translation set and refine it instead of starting from an empty file.

Built while shipping desktop apps in **35+ languages** — the context and ignore lists below exist because naive machine translation kept getting the same things wrong.

## Scripts

| Script | What it does |
|---|---|
| **`translate_from_ts_file.py`** | Reads each `<source>` string in a `.ts` file, translates it, and writes the result into the matching `<translation>` tag |
| **`update_ts_file.py`** | Adds new `<source>` strings to an existing `.ts` file and translates them — for when your UI has grown since the last pass |
| **`ts_to_qm.py`** | Compiles `.ts` files to the binary `.qm` files Qt loads at runtime, via `lrelease` |
| **`translate_from_json.py`** | Translates a plain dictionary of strings and writes JSON — useful when your strings do not live in a `.ts` file |

## Two things that make the output usable

Machine translation on short UI strings fails in predictable ways, so each script takes two lists:

**`bad_strings_for_translation`** — supply more context for ambiguous words. "Home" alone often translates as a dwelling; translated as "Home Menu" it comes back right, and the extra word is dropped:

```python
bad_strings_for_translation = {
    "Home": "Home Menu",
    "Play": "Play Video",
    "Resolution": "Video Resolution",
}
```

**`ignore_translation`** — strings that must stay in English, like brand and format names:

```python
ignore_translation = ["Facebook", "Instagram", "Select Format", "Rating"]
```

## Usage

```bash
pip install googletrans
```

`ts_to_qm.py` also needs `lrelease` from the Qt tools:

```bash
sudo apt install qttools5-dev-tools
```

Then set your languages and `.ts` paths at the top of the script you want:

```python
languages = {
    "de": "German",
    "fr": "French",
    "nl": "Dutch",
}

ts_file_path = {
    "de": "translation/de/main_de.ts",
    "fr": "translation/fr/main_fr.ts",
    "nl": "translation/nl/main_nl.ts",
}
```

and run it:

```bash
python3 translate_from_ts_file.py
python3 ts_to_qm.py
```

Working `.ts` files for German, French and Dutch are in [`Examples/`](Examples), alongside the `main_ui.py` they were generated from.

## Typical workflow

1. Generate or update `.ts` files from your source with `pylupdate5` / `lupdate`
2. Run `translate_from_ts_file.py` to fill in the translations
3. Review the output — machine translation is a starting point, not a shipping artifact
4. Run `ts_to_qm.py` to produce the `.qm` files your app loads
5. When the UI changes, run `update_ts_file.py` to translate only what's new

## Notes

- Translation uses the [`googletrans`](https://pypi.org/project/googletrans/) package, which talks to Google's free translate endpoint. It is rate-limited and occasionally breaks when the endpoint changes — fine for bootstrapping a language set, not something to put in CI.
- Always have a native speaker review strings that appear in destructive actions or error messages.

## Related

Built by the author of [4KTUBE](https://github.com/rishabh3354/4KTUBE), [FormatLab](https://github.com/rishabh3354/FORMAT_LAB) and [DL-YouTube](https://github.com/rishabh3354/YOUTUBE-DL-PRO) — PyQt5 desktop apps shipping in 35+ languages.
