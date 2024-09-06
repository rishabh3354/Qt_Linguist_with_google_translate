import json
from googletrans import Translator


languages = {
    # languages for translation, add more in this list!
    "de": "German",
    "fr": "French",
    "nl": "Dutch",
}

text_to_translate = {
    # input text for translation of your app
    "Hide Menu": {
        "en": "Hide Menu",
    },
    "Settings": {
        "en": "Settings",
    },
    "Home": {
        "en": "Home",
    },
}


bad_strings_for_translation = {
    # For e.g. It will translate according to 'Home Menu' not with 'Home'
    "Home": "Home Menu",
    "About": "About App",
    "Play Now": "Play Video",
    "Resolution": "Video Resolution",
}


def translate_from_json(filename):
    try:
        translator = Translator()
        result = text_to_translate.copy()
        total = len(text_to_translate.keys())
        for lang in languages:
            count = 1
            for string in text_to_translate:
                if string in bad_strings_for_translation:
                    new_string = bad_strings_for_translation[string]
                    trans_text = translator.translate(
                        text=new_string, dest=lang, src="en"
                    ).text
                else:
                    trans_text = translator.translate(
                        text=string, dest=lang, src="en"
                    ).text

                result[string][lang] = trans_text.strip()
                print(count, "/", total, ": ", lang, ": ", string, "-->", trans_text)
                count += 1

        with open(filename, "w") as file:
            json.dump(result, file, indent=4)
        print(f"Data successfully saved to {filename}")

        with open(filename, "r") as file:
            data = json.load(file)
        print(f"Data successfully loaded from {filename}")
        print(data)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    translate_from_json("translate_from_json.json")
