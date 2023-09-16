from transformers import pipeline
import re

#question_answerer = pipeline("question-answering", model='distilbert-base-cased-distilled-squad')
ner = pipeline("ner", aggregation_strategy="simple")

def checkNer(resNer):
    for item in resNer:
        if item['entity_group'] == 'PER':
            return True
        if item['entity_group'] == 'ORG':
            return True
    return False

def classify(file_content):
    #
    # direct sensitive data
    #
    
    # RSA private key
    hasRSA = file_content.find('-----BEGIN RSA PRIVATE KEY-----') != -1
    if hasRSA:
        return True
    
    # email regex
    email_regex = r"[\w\.-]+@[\w\.-]+"
    isDirect = bool(re.search(email_regex, file_content))

    # full name and company NER

    if not isDirect:
        resNer = ner(file_content)
        return checkNer(resNer)

    
    # IBAN regex
    iban_regex = r"[A-Z]{2}[0-9]{2}(?:[ ]?[0-9]{4}){4}(?!(?:[ ]?[0-9]){3})(?:[ ]?[0-9]{1,2})"
    isIndirect = bool(re.search(iban_regex, file_content))

    if not isIndirect:
        # Phone number regex
        phone_number_regex = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
        isIndirect = bool(re.search(phone_number_regex, file_content))

    if isDirect and isIndirect:
        return 'True'
    return 'False'
