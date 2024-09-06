from googletrans import Translator
import re


languages = {
    # languages for translation, add more in this list!
    "de": "German",
    "fr": "French",
    "nl": "Dutch",
}

ts_file_path = {
    # Replace your .ts path accordingly
    "de": "Examples/de/main_de.ts",
    "fr": "Examples/fr/main_fr.ts",
    "nl": "Examples/nl/main_nl.ts",
}

bad_strings_for_translation = {
    # For e.g. It will translate according to 'Home Menu' not with 'Home'
    "Home": "Home Menu",
    "About": "About App",
    "Play Now": "Play Video",
    "Resolution": "Video Resolution",
    "Play": "Play Video",
}

ignore_translation = [
    # these strings will be ignored for translation
    "Facebook",
    "Instagram",
    "Select Format",
    "Relevance",
    "Rating",
    "High",
    "Low",
]


def translate_text(text, target_language):
    translator = Translator()
    trans_text = translator.translate(text=text, dest=target_language, src="en").text
    print(target_language, ": ", text, "-->", trans_text)
    return trans_text


def translate_ts_file(file_path, target_language):
    with open(file_path, "r+", encoding="utf-8") as file:
        content = file.read()
        pattern = re.compile(
            r"(<source>(.*?)</source>\s*<translation>)(.*?)(</translation>)", re.DOTALL
        )

        def replace_translation(match):
            translated_text = ""
            source_text = match.group(2)
            input_str = source_text.strip()

            if input_str in bad_strings_for_translation:
                input_str = bad_strings_for_translation[input_str]

            if input_str not in ignore_translation and "&lt;html&gt;" not in input_str:
                translated_text = translate_text(input_str, target_language)

            return f"{match.group(1)}{translated_text}{match.group(4)}"

        updated_content = pattern.sub(replace_translation, content)
        file.seek(0)
        file.write(updated_content)
        file.truncate()


def run_for_all_lang():
    for lang, f_path in ts_file_path.items():
        print("Running for: ", lang, " File: ", f_path)
        translate_ts_file(f_path, lang)
    print("All files are done!")


if __name__ == "__main__":
    run_for_all_lang()
