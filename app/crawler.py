"""
This is a simple crawler that you can use as a boilerplate for your own
implementation. The crawler labels `.txt` files that contain the word
"hello" as "true", `.txt` files without "hello" as "false" and every other
item as "review". Try to modify this simple implementation so that it finds
some sensitive data and then expand your crawler from there.

You can change the code however you want, just make sure that following
things are satisfied:

- Grab the files from the directory "../files" relative to this script
- If you use Python packages, add a "requirements.txt" to your submission
- If you need to download larger files, e.g. NLP models, don't add them to
  the `app` folder. Instead, download them when the Docker image is build by
  changing the Docker file.
- Save your labels as a pickled dictionary in the `../results` directory.
  Use the filename as the key and the label as the value for each file.
- Your code cannot the internet during evaluation. Design accordingly.
"""

import os
from pathlib import Path
import pickle
import text_crawler
import file_converter
import chardet
import evaluation
import datetime

def textContent(file_path):
    try:
        with open(file_path) as f:
            file_content = f.read()
            return classify(file_content)
    except:
        return "review"

def save_dict_as_pickle(labels, filename):
    with open(filename, "wb") as handle:
        pickle.dump(labels, handle, protocol=pickle.HIGHEST_PROTOCOL)

def classifier(file_path):
    try:
        match(file_path.suffix):
            case '.mp3':
                return 'False'
            case '.pem':
                return 'True'

        file_content = file_converter.convert(file_path)
        return classify(file_content)
    except:
        try:
            blob = open(file_path, 'rb').read()
            encoding = chardet.detect(blob)
            if encoding['encoding'] is None:
                return 'review'
            file_content = open(file_path, encoding=encoding['encoding'], errors="ignore").read()
            return classify(file_content)
        except:
            return 'review'

def classify(file_content):
    return text_crawler.classify(file_content)

def main():
    # Get the path of the directory where this script is in
    script_dir_path = Path(os.path.realpath(__file__)).parents[1]
    # Get the path containing the files that we want to label
    file_dir_path = script_dir_path / "files"

    if os.path.exists(file_dir_path):
        # Initialize the label dictionary
        labels = {}
        # Loop over all items in the file directory
        for file_name in os.listdir(file_dir_path):
            file_path = file_dir_path / file_name
            a = datetime.datetime.now()
            labels[file_name] = classifier(file_path)
            b = datetime.datetime.now()
            c = b - a
            print(file_path.suffix, c.microseconds)

        # Save the label dictionary as a Pickle file
        save_dict_as_pickle(labels, script_dir_path / 'results' / 'crawler_labels.pkl')

        # Evaluate the labels
        evaluation.evaluate(labels)
    else:
        print("Please place the files in the corresponding folder")


if __name__ == "__main__":
    main()
