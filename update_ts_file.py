from googletrans import Translator
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


ts_file_path = {
    # locate your ts file and add path here!
    "de": "translation/de/main_de.ts",
    "fr": "translation/fr/main_fr.ts",
    "nl": "translation/nl/main_nl.ts",
    "it": "translation/it/main_it.ts",
}

bad_strings_for_translation = {
    # For e.g. It will translate according to 'Home Menu' not with 'Home'
    "Home": "Home Menu",
    "About": "About App",
    "Play Now": "Play Video",
    "Resolution": "Video Resolution",
}

ignore_translation = [
    # if you want to ignore any string
    "Facebook",
    "Instagram",
    "Select Format",
    "Relevance",
    "Rating",
    "High",
    "Low",
]


tags_to_add = [
    # To add new <source> tag in .ts file
    {
        "filename": "../main_ui.py",  # main ui file path (you can check in .ts file and paste it here)
        "line": "1",  # you can give any
        "source": "About App",  # input text for translation
        "translation": "",  # will be autofill
    },
    {
        "filename": "../main_ui.py",
        "line": "2",
        "source": "Play Video",
        "translation": "",
    },
]


def prettify_xml(elem):
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


def remove_existing_message(context, source_text):
    for message in context.findall("message"):
        source = message.find("source")
        if source is not None and source.text == source_text:
            context.remove(message)
            return


def add_or_overwrite_message_tags(lang, translator, xml_file, new_messages):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    context = root.find("context")

    if context is not None:
        for message in new_messages:
            remove_existing_message(context, message["source"])
            new_message = ET.SubElement(context, "message")
            location = ET.SubElement(new_message, "location")
            location.set("filename", message["filename"])
            location.set("line", message["line"])

            source = ET.SubElement(new_message, "source")
            source.text = message["source"]
            translation = ET.SubElement(new_message, "translation")

            input_str = message["source"].strip()

            if input_str in bad_strings_for_translation:
                input_str = bad_strings_for_translation[input_str]

            if input_str in ignore_translation:
                translated_text = input_str
            else:
                translated_text = translator.translate(input_str, dest=lang).text

            translation.text = translated_text

        pretty_xml_as_string = prettify_xml(root)
        pretty_xml_as_string = "\n".join(
            [line for line in pretty_xml_as_string.splitlines() if line.strip()]
        )
        with open(xml_file, "w", encoding="utf-8") as f:
            f.write(pretty_xml_as_string)


def add_tags_to_ts_file():
    translator = Translator()
    for lang, path in ts_file_path.items():
        add_or_overwrite_message_tags(lang, translator, path, tags_to_add)
        print(lang, ": Added & translated input tag")


if __name__ == "__main__":
    add_tags_to_ts_file()
