def classify(file_content):
    if file_content.find("Name") != -1:
        return "True"
    else:
        return "False"
