import subprocess


ts_file_path = {
    # Replace your .ts path accordingly
    "de": "translation/de/main_de.ts",
    "fr": "translation/fr/main_fr.ts",
    "nl": "translation/nl/main_nl.ts",
    "it": "translation/it/main_it.ts",
}


def convert_to_qm(lang, path):
    cmd = ["lrelease", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stderr:
        print(result.stderr)
    print(f"{lang}: Successfully converted to qm")


def convert_ts_to_qm():
    for lang, path in ts_file_path.items():
        convert_to_qm(lang, path)
    print("All files are converted to .qm")


if __name__ == "__main__":
    convert_ts_to_qm()
