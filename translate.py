import html
import json
import subprocess
from googletrans import Translator

from constant import APP_LANGUAGE_FILE
from translation.translate_constant import (bad_strings, ignore_strings,
                                            html_content_for_youtube_settings,
                                            html_content_for_bulk_videos, html_content_for_main, tags_to_add)
from translation.lang import APP_LANGUAGES_JSON
from translation.message import APP_MESSAGE_JSON
import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


# ==========================================for translating lang.py file

to_convert = list(APP_LANGUAGE_FILE.keys())

bad_strings_lang_json = {
    "Home": "Home Menu",
    "About": "About App",
    "Play Now": "Play Video",
    "Resolution": "Video Resolution",
    "Play": "Play Video",
}


def translate_app_language_json():
    try:
        translator = Translator()
        result = APP_LANGUAGES_JSON.copy()
        total = len(APP_LANGUAGES_JSON.keys())
        for lang in to_convert:
            count = 1
            for string in APP_LANGUAGES_JSON:
                if string in bad_strings_lang_json:
                    new_string = bad_strings_lang_json[string]
                    trans_text = translator.translate(text=new_string, dest=lang, src="en").text
                else:
                    trans_text = translator.translate(text=string, dest=lang, src="en").text

                result[string][lang] = trans_text.strip()
                print(count, "/", total, ": ", lang, ": ", string, "-->", trans_text)
                count += 1

        filename = "translate_app_language.json"
        with open(filename, 'w') as file:
            json.dump(result, file, indent=4)
        print(f"Data successfully saved to {filename}")

        with open(filename, 'r') as file:
            data = json.load(file)
        print(f"Data successfully loaded from {filename}")
        print(data)

    except Exception as e:
        print(e)


# =========================================for translating message.py file
def translate_app_message_json():
    try:
        translator = Translator()
        result = APP_MESSAGE_JSON.copy()
        total = len(APP_MESSAGE_JSON.keys())
        for lang in to_convert:
            count = 1
            for key, value in APP_MESSAGE_JSON.items():
                trans_text = translator.translate(text=value["en"], dest=lang, src="en").text
                result[key][lang] = trans_text.strip()
                print(count, "/", total, ": ", lang, ": ", value, "-->", trans_text)
                count += 1

        filename = "translate_app_message.json"
        with open(filename, 'w') as file:
            json.dump(result, file, indent=4)
        print(f"Data successfully saved to {filename}")

        with open(filename, 'r') as file:
            data = json.load(file)
            print(data)
        print(f"Data successfully loaded from {filename}")

    except Exception as e:
        print(e)


# ===================for translating xml file (.ts file) including (main.ts, tip.ts, bulk_video.ts, youtube_settings.ts)

def update_translation_tags(file_path, target_language):
    with open(file_path, 'r+', encoding='utf-8') as file:
        content = file.read()
        pattern = re.compile(r'(<source>(.*?)</source>\s*<translation>)(.*?)(</translation>)', re.DOTALL)

        def replace_translation(match):
            translated_text = ""
            source_text = match.group(2)
            input_str = source_text.strip()

            if input_str in bad_strings:
                input_str = bad_strings[input_str]

            if input_str not in ignore_strings and "&lt;html&gt;" not in input_str:
                translated_text = translate_text(input_str, target_language)

            return f"{match.group(1)}{translated_text}{match.group(4)}"

        updated_content = pattern.sub(replace_translation, content)
        file.seek(0)
        file.write(updated_content)
        file.truncate()


def translate_text(text, target_language):
    translator = Translator()
    trans_text = translator.translate(text=text, dest=target_language, src="en").text
    print(target_language, ": ", text, "-->", trans_text)
    return trans_text


def run_xml_file_skip_html():
    for lang, f_path in APP_LANGUAGE_FILE.items():
        main = f_path.get("main").replace(":/lang/translation/", "").replace(".qm", ".ts")
        bulk_video = f_path.get("bulk_video").replace(":/lang/translation/", "").replace(".qm", ".ts")
        youtube_settings = f_path.get("youtube_settings").replace(":/lang/translation/", "").replace(".qm", ".ts")
        tip = f_path.get("tip").replace(":/lang/translation/", "").replace(".qm", ".ts")
        print("Running for: ", lang, " File: ", main)
        update_translation_tags(main, lang)
        update_translation_tags(bulk_video, lang)
        update_translation_tags(youtube_settings, lang)
        update_translation_tags(tip, lang)

    print("All file done!")


def convert_to_qm(path):
    cmd = ["lrelease", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr)


def convert_all_ts_to_qt_resource():

    for key, path in APP_LANGUAGE_FILE.items():
        if key != "en":
            main = path.get("main").split(":/lang/translation/")[-1].replace(".qm", ".ts")
            convert_to_qm(main)

            bulk_video = path.get("bulk_video").split(":/lang/translation/")[-1].replace(".qm", ".ts")
            convert_to_qm(bulk_video)

            youtube_settings = path.get("youtube_settings").split(":/lang/translation/")[-1].replace(".qm", ".ts")
            convert_to_qm(youtube_settings)

            tip = path.get("tip").split(":/lang/translation/")[-1].replace(".qm", ".ts")
            convert_to_qm(tip)

    print("All converted to .qm files!")
    convert_qm_to_qt_resources()


def convert_qm_to_qt_resources():
    cmd = ["pyrcc5", "../qrc/_ts.qrc", "-o", "../_ts_rc.py"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr)

    print("All compiled to QT resource!")


# ==============================================================html solution in ts file================================
def html_translation(content):
    result = {}

    def translate_json(input_lang, input_string):
        try:
            translator = Translator()
            trans_text = translator.translate(text=input_string, dest=input_lang, src="en").text
            print(trans_text)
            print(input_lang, ": ", "-->", trans_text)

            return trans_text

        except Exception as e:
            print(e)

    for lang in to_convert:
        temp = dict()
        for title, raw_html in content.items():
            t_data = translate_json(lang, title)
            data_list = str(t_data).split("\n")
            if data_list != 0:
                for count, val in enumerate(data_list, 1):
                    raw_html = raw_html.replace(f"[{count}]", val)
            else:
                raw_html = raw_html.replace(f"[1]", data_list[-1])
            temp[title] = raw_html
        result[lang] = temp

    print("final result =========>", result)
    return result


def run_xml_file_with_html():
    main_result = html_translation(html_content_for_main)  # for each app this constant is different! Change it
    bulk_videos_result = html_translation(html_content_for_bulk_videos)
    youtube_settings_result = html_translation(html_content_for_youtube_settings)

    print("Result is passing through next function for find and replace string in file")

    replace_xml_file_with_html(main_result, "main")
    replace_xml_file_with_html(bulk_videos_result, "bulk_video")
    replace_xml_file_with_html(youtube_settings_result, "youtube_settings")
    convert_qm_to_qt_resources()


def replace_xml_file_with_html(html_translation_result, file_type):

    def replace_translation_for_source(file_path, search_term, new_translation):
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
            pattern = re.compile(
                r'(<message>.*?<source>.*?{}.*?</source>\s*<translation>)(.*?)(</translation>.*?</message>)'.format(
                    re.escape(search_term)),
                re.DOTALL
            )

            def replace_translation(match):
                return f"{match.group(1)}{new_translation}{match.group(3)}"

            updated_content = pattern.sub(replace_translation, content)
            file.seek(0)
            file.write(updated_content)
            file.truncate()

    for lang, term_with_html in html_translation_result.items():
        for term, new_translation in term_with_html.items():
            search_term = term.split("\n")[0]

            if search_term == "ABOUT APP:":
                search_term = "ABOUT :"
            elif search_term == "Designed & Developed by:":
                search_term = "Designed"
            elif search_term.startswith("Congratulations, you are using"):
                search_term = "Congratulations, you are using"

            if file_type == "main":
                file_path = APP_LANGUAGE_FILE.get(lang).get("main").replace(":/lang/translation/", "").replace(".qm", ".ts")
            elif file_type == "bulk_video":
                file_path = APP_LANGUAGE_FILE.get(lang).get("bulk_video").replace(":/lang/translation/", "").replace(".qm", ".ts")
            elif file_type == "youtube_settings":
                file_path = APP_LANGUAGE_FILE.get(lang).get("youtube_settings").replace(":/lang/translation/", "").replace(".qm", ".ts")

            print(lang, ": Running : ", file_path)
            replace_translation_for_source(file_path, search_term, html.escape(new_translation))
        convert_to_qm(file_path)
        print(lang, ": Converting to qm..")
        print(lang, ": Done!")


# =====================add <source> tag to xml file====================================================================


bad_strings_tags = {
    "Home": "Home Menu",
    "Batch Files (New)": "Batch (New)",
    "About": "About App",
    "System Monitor": "CPU Monitor",
}
ignore_strings_tags = []


def prettify_xml(elem):
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="    ")


def remove_existing_message(context, source_text):
    for message in context.findall('message'):
        source = message.find('source')
        if source is not None and source.text == source_text:
            context.remove(message)
            return


def add_or_overwrite_message_tags(lang, translator, xml_file, new_messages):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    context = root.find('context')

    if context is not None:
        for message in new_messages:
            remove_existing_message(context, message['source'])
            new_message = ET.SubElement(context, 'message')
            location = ET.SubElement(new_message, 'location')
            location.set('filename', message['filename'])
            location.set('line', message['line'])

            source = ET.SubElement(new_message, 'source')
            source.text = message['source']
            translation = ET.SubElement(new_message, 'translation')

            input_str = message['source'].strip()

            if input_str in bad_strings_tags:
                input_str = bad_strings_tags[input_str]

            if input_str in ignore_strings_tags:
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

    for key, path in APP_LANGUAGE_FILE.items():
        if key != "en":
            main = path.get("main").split(":/lang/translation/")[-1].replace(".qm", ".ts")
            add_or_overwrite_message_tags(key, translator, main, tags_to_add)
            print(key, ": Added & translated tag")
            convert_to_qm(main)
    convert_qm_to_qt_resources()

# ================================================run from here================================


# translate_app_language_json()
# translate_app_message_json()
# run_xml_file_skip_html()
# run_xml_file_with_html()
# convert_all_ts_to_qt_resource()  # for converting all ts to qs then qt resource
# add_tags_to_ts_file()  # for adding <source> tag to ts file, also get translated tag
